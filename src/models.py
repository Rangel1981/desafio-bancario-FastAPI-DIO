from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import List
from sqlalchemy import ForeignKey, String, Numeric, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base


#definido o Enum e o tipo de transição
class TransactionType(str, Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"

#tabela de usuário e conta corrente
class UserModel(Base):
    __tablename__ = "Users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)

    # Abordagem Persistida: O saldo fica guardado aqui. 
    # Usar Numeric(10, 2) para dinheiro, NUNCA usar Float para valores monetários!
    balance: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal("0.00"))

    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())

    # Relacionamento de 1 para N
    # Um usuário pode ter várias transições
    transactions: Mapped[List["TransactionModel"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

class TransactionModel(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("Users.id", ondelete="CASCADE"), nullable=False)
    
    # Tipo da transação DEPOSIT ou WITHDRAW
    type: Mapped[TransactionType] = mapped_column(String(20), nullable=False)
    
    # Valor da transação
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # Relacionamento: A transação pertence a um usuário
    user: Mapped["UserModel"] = relationship(back_populates="transactions")