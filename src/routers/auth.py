from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src import models, schemas, auth
from src.database import get_db



router = APIRouter(prefix="/auth", tags=["Autenticação"])

@router.post("/register", response_model=schemas.UserCreate, status_code=status.HTTP_201_CREATED)
async def register(user_in: schemas.UserResponse, db: AsyncSession = Depends(get_db)):
    
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
async def login(user_in: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    
    #UserCreate temporariamente aqui pelo email/password.
    
    #  Busca o usuário pelo e-mail
    query = select(models.UserModel).where(models.UserModel.email == user_in.email)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    
    #se não achar ou a senha estiver errada, joga erro 401 (Não Autorizado)
    if not user or not auth.verify_password(user_in.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos."
        )
    
    # Gera o Token JWT contendo o ID do usuário
    token_payload = {"sub": str(user.id)}
    token = auth.create_access_token(data=token_payload)
    
    # Retorna o token e o tipo dele (Bearer)
    return {"access_token": token, "token_type": "bearer"}