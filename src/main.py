from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.database import engine, Base
from src import models  
from src.routers import auth as auth_router
from src.routers import transactions as transactions_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # STARTUP
    print("Iniciando a API Bancária e criando tabelas...")
    async with engine.begin() as conn:
        # Cria as tabelas no banco de dados se não existirem
        await conn.run_sync(Base.metadata.create_all)
    
    yield  # A API fica rodando aqui enquanto este yield estiver ativo
    
    # SHUTDOWN
    print("Desligando a API Bancária e limpando recursos...")
  


# Passamos o lifespan na criação da instância do FastAPI
app = FastAPI(
    title="API Bancária Assíncrona",
    lifespan=lifespan,
    summary="Uma atividade da DIO"
)

app.include_router(auth_router.router)
app.include_router(transactions_router.router)


@app.get("/")
def read_root():
    return {"message": "API Bancária Online, Conectada e usando Lifespan!"}