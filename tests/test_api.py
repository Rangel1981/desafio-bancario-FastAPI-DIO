import pytest
import random
from httpx import AsyncClient, ASGITransport
from src.main import app

pytestmark = pytest.mark.asyncio

@pytest.mark.asyncio
async def test_user_flow_register_and_login():
    """Testa o fluxo completo do usuário: Cadastro seguido de Login imediato"""
    suffix = random.randint(1000, 9999)
    user_data = {
        "name": "Arthur Teste",
        "email": f"arthur_{suffix}@test.com",
        "password": "SenhaSegura123"
    }
    
    transport = ASGITransport(app=app)
    
    # Abrimos o cliente apenas uma vez para todo o fluxo do teste
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        
        # 1. Executa o Cadastro
        register_resp = await ac.post("/auth/register", json=user_data)
        assert register_resp.status_code == 201
        
        register_json = register_resp.json()
        assert "id" in register_json
        assert float(register_json["balance"]) == 0
        
        # 2. Executa o Login imediatamente na mesma conexão
        login_resp = await ac.post(
            "/auth/login",
            data={
                "username": user_data["email"],
                "password": user_data["password"]
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        assert login_resp.status_code == 200
        login_json = login_resp.json()
        assert "access_token" in login_json
        assert login_json["token_type"] == "bearer"