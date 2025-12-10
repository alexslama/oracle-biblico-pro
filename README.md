# 🔮 SHAMIR - Oráculo Bíblico Profissional

**Sistema Avançado de Análise Bíblica com IA**

SHAMIR é um oráculo bíblico profissional que utiliza Llama 3.1 + RAG (Retrieval-Augmented Generation) especializado em textos hebraicos e bíblicos. Otimizado para MacBook M1/Max e Google Cloud.

---

## 🌟 Capacidades

✅ **Análise em 5 Camadas**
- Linguística (Hebraico/Grego antigos)
- Numérica (Gematria com valores hebraicos)
- Histórica (Contexto arqueológico)
- Teológica (Conceitos divinos)
- Integrada (Síntese completa)

✅ **Processamento Estruturado**
- 5 templates de análise especializados
- Validação automática de qualidade
- Rastreabilidade de fontes

✅ **Inteligência Contextual**
- RAG com vector database (Chroma)
- 5+ documentos de contexto por query
- Cross-referencing automático

✅ **Qualidade Garantida**
- Testes unitários completos
- Validação de respostas
- Scoring automático (0-100%)

---

## 🚀 Início Rápido

### Pré-requisitos
- Python 3.12+
- M1/M2 Mac ou CPU com 8GB+ RAM
- Git

### Instalação

```bash
# Clone o repositório
git clone https://github.com/alexslama/oracle-biblico-pro.git
cd oracle-biblico-pro

# Execute o script de deploy
./DEPLOY_M1_MAC.sh

# Ou manualmente:
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

Acesse: `http://localhost:5000`

---

## 📚 Interface Web

### Tela Principal
- **Logo**: Identidade visual do Oráculo SHAMIR
- **Entrada**: "O que quer perguntar para o Oráculo?"
- **Botão**: CONSULTAR (com efeito hover verde)

### Resultado
- Revelação estruturada em 5 seções
- Cada seção identifica seu tipo de análise
- Navegação intuitiva e rápida

---

## ⚙️ Stack

- **Backend**: Python 3.12, Flask
- **IA**: Llama 3.1, ChromaDB (RAG)
- **Frontend**: HTML5, CSS3, JavaScript
- **Design**: Green (#00d966) + Black theme (Matrix)
- **Deploy**: Docker, M1 Native

---

## 💫 Autor

Criado com ♥ para questão bíblica profunda e análise estruturada.

**SHAMIR Oráculo Bíblico** - Powered by Llama 3.1 + ChromaDB RAG
