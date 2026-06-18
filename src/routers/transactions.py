from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src import models, schemas
from src.database import get_db
from src.dependencies import get_current_user
from sqlalchemy.future import select


# criada a rota de transição
router = APIRouter(prefix="/transactions", tags=["Transações"])

@router.post("/deposit", response_model=schemas.TransactionResponse, status_code=status.HTTP_201_CREATED)
async def deposit(
    transaction_in: schemas.TransactionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: models.UserModel = Depends(get_current_user)
):
    # Atualiza o saldo do usuário logado somando o valor do depósito
    current_user.balance += transaction_in.amount
    
    #Cria o registro da transação no banco de dados
    new_transaction = models.TransactionModel(
        user_id=current_user.id,
        type=transaction_in.type,
        amount=transaction_in.amount
    )
    
    #Salva tudo de forma assíncrona
    db.add(new_transaction)
    await db.commit()
    await db.refresh(new_transaction)
    
    return new_transaction


@router.post("/withdraw", response_model=schemas.TransactionResponse, status_code=status.HTTP_201_CREATED)
async def withdraw(
    transaction_in: schemas.TransactionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: models.UserModel = Depends(get_current_user)
):
    #Validação de Regra de Negócio: Verifica se o usuário tem saldo suficiente
    if current_user.balance < transaction_in.amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Saldo insuficiente para realizar esta operação."
        )
    
    #Atualiza o saldo do usuário subtraindo o valor do saque
    current_user.balance -= transaction_in.amount
    
    #Registra a transação com o tipo que veio na requisição (WITHDRAW)
    new_transaction = models.TransactionModel(
        user_id=current_user.id,
        type=transaction_in.type,
        amount=transaction_in.amount
    )
    
    # persiste as mudanças no banco de dados
    db.add(new_transaction)
    await db.commit()
    await db.refresh(new_transaction)
    
    return new_transaction

@router.get("/statement", response_model=list[schemas.TransactionResponse])
async def get_statement(
    db: AsyncSession = Depends(get_db),
    current_user: models.UserModel = Depends(get_current_user)
):
    #  Cria a query para buscar todas as transações do usuário logado
    # Usamos o order_by para que as mais recentes apareçam primeiro ou na ordem correta
    query = select(models.TransactionModel).where(
        models.TransactionModel.user_id == current_user.id
    ).order_by(models.TransactionModel.created_at.desc())
    
    # Executa a busca de forma assíncrona
    result = await db.execute(query)
    transactions = result.scalars().all()
    
    # Retorna a lista de transações (o FastAPI joga no list[schemas.TransactionResponse])
    return transactions

@router.get("/balance", response_model=schemas.BalanceResponse)
async def get_balance(current_user: models.UserModel = Depends(get_current_user)):
    # Retorna o saldo direto do objeto do usuário que a dependência já buscou
    return {"balance": current_user.balance}