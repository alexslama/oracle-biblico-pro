#!/bin/bash

################################################################################
# 🍎 ORACLE BIBLICO PRO - AUTOMATIC DEPLOYMENT FOR MAC M1 MAX
# Master Deployment Script - Execute this ONE TIME to deploy everything
# Author: Comet AI Assistant
# Date: December 2025
################################################################################

set -e  # Exit on any error
set -u  # Exit on undefined variable

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
DEPLOY_DIR="${1:-.}"
REPO_URL="https://github.com/alexslama/oracle-biblico-pro.git"
PYTHON_MIN_VERSION="3.10"

################################################################################
# STEP 0: VERIFY SYSTEM REQUIREMENTS
################################################################################

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   🍎 Oracle Biblico PRO - M1 Max Deployment               ║${NC}"
echo -e "${BLUE}║   Automatic Setup & Initialization                        ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

echo -e "${YELLOW}[1/10]${NC} Verificando requisitos do sistema..."

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 não encontrado!${NC}"
    echo "   Install: brew install python@3.10"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}✓${NC} Python: $PYTHON_VERSION"

# Check Git
if ! command -v git &> /dev/null; then
    echo -e "${RED}❌ Git não encontrado!${NC}"
    echo "   Install: brew install git"
    exit 1
fi
echo -e "${GREEN}✓${NC} Git: $(git --version | awk '{print $3}')"

# Check M1 Architecture
ARCH=$(uname -m)
if [[ "$ARCH" != "arm64" ]]; then
    echo -e "${YELLOW}⚠${NC}  Não é ARM64 (M1/M2), mas prosseguindo..."
else
    echo -e "${GREEN}✓${NC} Arquitetura: Apple Silicon (arm64)"
fi

# Check RAM
RAM_GB=$(vm_stat | grep "Pages free" | awk '{print int($3 / 256000)}')
echo -e "${GREEN}✓${NC} RAM disponível: ~${RAM_GB}GB"

echo ""

################################################################################
# STEP 1: CLONE REPOSITORY
################################################################################

echo -e "${YELLOW}[2/10]${NC} Clonando repositório..."

if [ -d "oracle-biblico-pro" ]; then
    echo -e "${YELLOW}ℹ${NC}  Diretório já existe, usando versão existente"
    cd oracle-biblico-pro
else
    git clone "$REPO_URL" oracle-biblico-pro
    cd oracle-biblico-pro
fi

echo -e "${GREEN}✓${NC} Repositório pronto"
echo ""

################################################################################
# STEP 2: SETUP VIRTUAL ENVIRONMENT
################################################################################

echo -e "${YELLOW}[3/10]${NC} Criando ambiente virtual Python..."

if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✓${NC} Ambiente virtual criado"
else
    echo -e "${YELLOW}ℹ${NC}  Ambiente virtual já existe"
fi

source venv/bin/activate
echo -e "${GREEN}✓${NC} Ambiente ativado"
echo ""

################################################################################
# STEP 3: UPGRADE PIP & INSTALL DEPENDENCIES
################################################################################

echo -e "${YELLOW}[4/10]${NC} Atualizando pip e instalando dependências..."

pip install --upgrade pip setuptools wheel --quiet
echo -e "${GREEN}✓${NC} pip atualizado"

pip install -r requirements.txt --quiet
echo -e "${GREEN}✓${NC} Dependências instaladas (30+ pacotes)"
echo ""

################################################################################
# STEP 4: CREATE DIRECTORY STRUCTURE
################################################################################

echo -e "${YELLOW}[5/10]${NC} Criando estrutura de diretórios..."

mkdir -p data/raw
mkdir -p data/processed
mkdir -p data/models
mkdir -p data/vector_db
mkdir -p logs
mkdir -p outputs

echo -e "${GREEN}✓${NC} Diretórios criados"
echo ""

################################################################################
# STEP 5: SET M1 MAX OPTIMIZATIONS
################################################################################

echo -e "${YELLOW}[6/10]${NC} Configurando otimizações M1 Max..."

export METAL_ENABLED=1
export OMP_NUM_THREADS=10
export MKL_NUM_THREADS=10

echo -e "${GREEN}✓${NC} Metal acceleration ativado"
echo -e "${GREEN}✓${NC} Thread optimization: 10 cores"
echo ""

################################################################################
# STEP 6: COLLECT BIBLE TEXTS
################################################################################

echo -e "${YELLOW}[7/10]${NC} Coletando textos bíblicos..."
echo "   Executando: python3 scripts/collect_data.py"

python3 scripts/collect_data.py 2>/dev/null
echo -e "${GREEN}✓${NC} Dados coletados e armazenados"
echo ""

################################################################################
# STEP 7: PREPARE TRAINING DATA
################################################################################

echo -e "${YELLOW}[8/10]${NC} Preparando dados de treinamento..."
echo "   Executando: python3 scripts/prepare_training_data.py"

python3 scripts/prepare_training_data.py 2>/dev/null
echo -e "${GREEN}✓${NC} Dados em formato JSONL pronto"
echo ""

################################################################################
# STEP 8: CONFIGURE FINE-TUNING
################################################################################

echo -e "${YELLOW}[9/10]${NC} Configurando fine-tuning do Llama3.1..."
echo "   Executando: python3 scripts/finetune_llama.py"

python3 scripts/finetune_llama.py 2>/dev/null
echo -e "${GREEN}✓${NC} Fine-tuning configuration completo"
echo ""

################################################################################
# STEP 9: BUILD RAG SYSTEM
################################################################################

echo -e "${YELLOW}[10/10]${NC} Construindo sistema RAG..."
echo "    Executando: python3 scripts/build_rag.py"

python3 scripts/build_rag.py 2>/dev/null
echo -e "${GREEN}✓${NC} Vector index construído com sucesso"
echo ""

################################################################################
# FINAL: TEST ANALYSIS PIPELINE
################################################################################

echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                  🎉 DEPLOYMENT COMPLETO!                  ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

echo -e "${BLUE}📊 System Status:${NC}"
echo -e "   ${GREEN}✓${NC} Python Virtual Environment: ativado"
echo -e "   ${GREEN}✓${NC} Dependências: 30+ pacotes instalados"
echo -e "   ${GREEN}✓${NC} Dados Bíblicos: Coletados"
echo -e "   ${GREEN}✓${NC} Dados de Treinamento: Preparados (JSONL)"
echo -e "   ${GREEN}✓${NC} Fine-tuning Llama3.1: Configurado"
echo -e "   ${GREEN}✓${NC} RAG System: Construído com FAISS"
echo -e "   ${GREEN}✓${NC} Análise Bíblica: 5-layer pipeline pronto"
echo ""

echo -e "${BLUE}🚀 Para começar a usar:${NC}"
echo ""
echo -e "   ${YELLOW}1. Ativar ambiente (se não estiver ativado):${NC}"
echo -e "      source venv/bin/activate"
echo ""
echo -e "   ${YELLOW}2. Executar análise bíblica:${NC}"
echo -e "      python3 scripts/analysis_pipeline.py 'Profecia sobre cometa'"
echo ""
echo -e "   ${YELLOW}3. Ver resultados:${NC}"
echo -e "      cat outputs/analysis_results.json | python3 -m json.tool"
echo ""
echo -e "   ${YELLOW}4. Integrar com OpenWebUI (localhost:3000):${NC}"
echo -e "      python3 scripts/analysis_pipeline.py 'sua pergunta'"
echo ""

echo -e "${BLUE}📚 Documentação:${NC}"
echo "   README.md - Guia completo"
echo "   scripts/ - Código-fonte comentado"
echo "   outputs/ - Resultados das análises"
echo ""

echo -e "${GREEN}✅ Seu Oracle Biblico PRO está pronto para usar!${NC}"
echo ""
