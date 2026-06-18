from datetime import datetime, timedelta, timezone
import jwt
from passlib.context import CryptContext



#configurando o passlib
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#configurando a chave secreta e o tempo de expiração
#Em produção, isso deve vir de variáveis de ambiente (.env)
SECRET_KEY = "sua_chave_secreta_super_segura_do_flamengo"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    
    # Define o momento exato em que o token vai expirar
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Atualiza o payload com a data de expiração
    to_encode.update({"exp": expire})
    
    # Gera o token assinado com a nossa SECRET_KEY
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt