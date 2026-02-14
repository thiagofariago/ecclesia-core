#!/bin/bash
# Script para executar o servidor de desenvolvimento

set -e

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Iniciando servidor de desenvolvimento Ecclesia...${NC}"

# Verificar se o venv existe
if [ ! -d "venv" ]; then
    echo -e "${BLUE}Criando ambiente virtual...${NC}"
    python3 -m venv venv
fi

# Ativar venv
source venv/bin/activate

# Instalar dependências
echo -e "${BLUE}Instalando dependências...${NC}"
pip install -q -r requirements.txt

# Verificar se .env existe
if [ ! -f ".env" ]; then
    echo -e "${BLUE}Criando arquivo .env a partir de .env.example...${NC}"
    cp .env.example .env
    echo -e "${GREEN}Arquivo .env criado. Configure as variáveis antes de continuar.${NC}"
fi

# Executar servidor
echo -e "${GREEN}Servidor rodando em http://localhost:8000${NC}"
echo -e "${GREEN}Documentação disponível em http://localhost:8000/docs${NC}"
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
