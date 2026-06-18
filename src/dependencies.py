import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src import models, auth
from src.database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    # exceção padrão para reutilizar caso dê algo errado
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        #Decodifica o token usando a chave e o algoritmo do auth.py
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        user_id: str = payload.get("sub")
        
        #Se não tiver o 'sub' (ID do usuário) dentro do token, joga erro
        if user_id is None:
            raise credentials_exception
            
    except jwt.InvalidTokenError:
        # Se o token estiver adulterado ou expirado, cai aqui
        raise credentials_exception

    #busca o usuário no banco de dados pelo ID que estava no token
    query = select(models.UserModel).where(models.UserModel.id == int(user_id))
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    #se o usuário foi deletado do banco mas o token ainda era válido, joga erro
    if user is None:
        raise credentials_exception
        
    #retorna o usuário logado com todos os dados dele prontinhos
    return user