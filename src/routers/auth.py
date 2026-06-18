from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src import models, schemas, auth
from src.database import get_db
from src.dependencies import get_current_user


router = APIRouter(prefix="/auth", tags=["Autenticação"])

@router.post("/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_in: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    
    #   Verifica se o email já existe no banco

    query = select(models.UserModel).where(models.UserModel.email == user_in.email)
    result = await db.execute(query)
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este e-mail já está cadastrado."
        )
    
    #Criptografa a senha do usuário
    hashed_password = auth.get_password_hash(user_in.password)
    
    # Cria o modelo do banco com a senha protegida
    new_user = models.UserModel(
        name=user_in.name,
        email=user_in.email,
        password=hashed_password,
        balance=0.00  # Conta nova começa zerada
    )
    
    # Salva no banco de dados de forma assíncrona
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    return new_user


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),  # <-- MUDE AQUI (substituindo o schema antigo)
    db: AsyncSession = Depends(get_db)
):
    # O OAuth2PasswordRequestForm traz os campos como 'form_data.username' e 'form_data.password'
    query = select(models.UserModel).where(models.UserModel.email == form_data.username)
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    # Verifica se o usuário existe e se a senha bate
    if not user or not auth.verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos."
        )

    # Gera o token de acesso usando o ID do usuário (convertido para string)
    access_token = auth.create_access_token(data={"sub": str(user.id)})
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_account(
    db: AsyncSession = Depends(get_db),
    current_user: models.UserModel = Depends(get_current_user)
):
    # Como vamos deletar o usuário, primeiro precisamos apagar as transações dele 
    # para o banco não reclamar de restrição de chave (Foreign Key)
    # (Se você já tiver configurado cascade=['all', 'delete'] no models.py, essa parte das transações é automática)
    from sqlalchemy import delete
    
    # Apaga as transações do usuário
    query_transactions = delete(models.TransactionModel).where(models.TransactionModel.user_id == current_user.id)
    await db.execute(query_transactions)
    
    # Agora deleta o usuário em si
    await db.delete(current_user)
    
    # Salva as alterações no banco de dados
    await db.commit()
    
    # O HTTP_204_NO_CONTENT não retorna nenhum corpo de texto, apenas avisa que foi deletado com sucesso
    return None