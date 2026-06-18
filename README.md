Sistema Bancário API — Desafio FastAPI (DIO)
Este projeto é uma API robusta para um sistema bancário simplificado, desenvolvido como uma extensão do desafio prático da Digital Innovation One (DIO). A aplicação foi evoluída para incluir autenticação segura, persistência de dados assíncrona, gerenciamento de transações e testes automatizados de ponta a ponta.

🚀 Funcionalidades
Autenticação & Segurança: Registro de usuários e login integrado ao ecossistema Swagger usando OAuth2 (OAuth2PasswordRequestForm) e tokens JWT. Criptografia de senhas com bcrypt.

Transações Bancárias: Endpoints assíncronos para realizar depósitos e saques com validação de saldo em tempo real.

Consultas & Gerenciamento:

Visualização de extrato completo de transações.

Endpoint exclusivo para checagem rápida de saldo atual (GET /transactions/balance).

Exclusão segura de conta com remoção em cascata de histórico de transações (DELETE /auth/me).

Testes Automatizados: Suíte de testes automatizados assíncronos utilizando pytest e httpx.

🛠️ Tecnologias Utilizadas
FastAPI: Framework web moderno, rápido (alta performance) para construir APIs com Python.

SQLAlchemy (Async): ORM SQL para Python utilizando mapeamento de dados totalmente assíncrono.

SQLite / PostgreSQL: Banco de dados para persistência das tabelas de usuários e transações.

Pytest & HTTPX: Ferramentas para automação de testes assíncronos de integração.

Pydantic v2: Validação de dados e gerenciamento de schemas.

📦 Como Executar o Projeto
1. Clonar o repositório
git clone https://github.com/seu-usuario/desafio-bancario-FastAPI-DIO.git
cd desafio-bancario-FastAPI-DIO

2. Configurar o Ambiente Virtual (venv)
Criar o ambiente virtual
python -m venv venv

Ativar o ambiente virtual (Windows - PowerShell)
.\venv\Scripts\Activate.ps1

Ativar o ambiente virtual (Linux/macOS)
source venv/bin/activate

3. Instalar as Dependências
pip install -r requirements.txt

4. Rodar a Aplicação
uvicorn src.main:app --reload

A API estará disponível em http://127.0.0.1:8000. Acesse /docs para abrir a interface interativa do Swagger.

🧪 Como Rodar os Testes Automatizados
A suíte de testes valida o fluxo completo de ponta a ponta (cadastro e autenticação de usuário no banco de dados assíncrono).

Para executar os testes no PowerShell (Windows), utilize:
$env:PYTHONPATH="." ; pytest -v -p no:warnings

No Linux/macOS:
PYTHONPATH=. pytest -v -p no:warnings

Desenvolvido por Arthur como projeto de portfólio para Engenharia de Software.