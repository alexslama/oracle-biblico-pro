# 🔮 Oracle Bíblico PRO

**Sistema de Análise Bíblica Profissional com IA**

Fine-tuning Llama3.1 + RAG especializado em textos hebraicos e bíblicos. Otimizado para MacBook M1/Max e Google Cloud.

---

## 🎯 Capacidades

✅ **Análise em 5 Camadas**
- Lingüística (Hebraico/Grego antigos)
- Numérica (Gematria com valores hebraicos)
- Histórica (Contexto arqueológico)
- Teológica (Conceitos divinos)
- Integrada (Síntese completa)

✅ **Processamento Estruturado**
- 5 templates de análise especializados
- Validação automática de qualidade
- Rastreambiilidade de fontes

✅ **Inteligência Contextual**
- RAG com vector database (Chroma)
- 5+ documentos de contexto por query
- Cross-referencing automático

✅ **Qualidade Garantida**
- Tests unitários completos
- Validação de respostas
- Scoring automático (0-100%)

---

## 🚀 Começar Rápido

### Pré-requisitos
- Python 3.9+
- Ollama (`ollama.ai`)
- 64GB RAM (recomendado para fine-tuning)

### Instalação (MacBook M1/Max)

```bash
# 1. Clonar repo
git clone https://github.com/alexslama/oracle-biblico-pro
cd oracle-biblico-pro

# 2. Criar ambiente virtual (Apple Silicon)
arch -arm64 python3 -m venv venv
source venv/bin/activate

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Executar setup
bash setup.sh
```

---

## 📚 Etapas de Execução

### Etapa 1: Coleta de Dados (2-3 horas)

```bash
python scripts/01_collect_data.py
```

**O que faz:**
- Baixa corpus bíblico de Sefaria.org
- Processa textos hebraicos
- Enriquece com traduções em português

### Etapa 2: Preparar Dados de Treinamento (1 hora)

```bash
python scripts/02_prepare_training_data.py
```

**O que faz:**
- Cria pares instruction-response
- Gera 3 variações de prompts por verso
- Formata para JSONL

### Etapa 3: Fine-tune Llama3.1 (4-8 horas em M1 Max)

```bash
python scripts/03_finetune_llama.py
```

**Configurado para:**
- Apple Silicon acceleration
- 8-bit quantization
- 3 épocas de treinamento
- Validação em tempo real

### Etapa 4: Construir Sistema RAG (1-2 horas)

```bash
python scripts/04_build_rag.py
```

**Cria:**
- Vector database com Chroma
- Índices de busca de similaridade
- Recuperação contextual

### Etapa 5: Pipeline Completo de Análise (Contínuo)

```bash
python scripts/05_analysis_pipeline.py
```

**Executa:**
- Análise de múltiplos versículos
- Cálculo de gematria
- Validação de qualidade

### Etapa 6: Testes e Validação

```bash
python scripts/06_testing_validation.py
```

---

## ☁️ Deploy no Google Cloud

### Setup Inicial

```bash
# 1. Autenticar com Google Cloud
gcloud auth login
gcloud config set project seu-projeto-id

# 2. Criar Compute Engine Instance
gcloud compute instances create oracle-biblico \
    --machine-type=n1-standard-8 \
    --accelerator=type=nvidia-tesla-p100,count=1 \
    --image-family=pytorch-latest-cu121 \
    --image-project=deeplearning-platform-release

# 3. SSH na instância
gcloud compute ssh oracle-biblico

# 4. Clonar e instalar
git clone https://github.com/alexslama/oracle-biblico-pro
cd oracle-biblico-pro
pip install -r requirements.txt
```

### Executar Fine-tune na GPU

```bash
# Com GPU P100, fine-tune leva ~2 horas
python scripts/03_finetune_llama.py --use-gpu
```

---

## 📁 Estrutura do Projeto

```
oracle-biblico-pro/
├── data/
│   ├── raw/                    # Dados brutos
│   │   ├── hebrew/
│   │   ├── greek/
│   │   └── portuguese/
│   ├── processed/              # Dados processados
│   │   ├── training_data/
│   │   ├── rag_corpus/
│   │   └── validation/
│
├── models/
│   ├── checkpoints/            # Checkpoints de treinamento
│   └── final/                  # Modelo fine-tunado final
│
├── scripts/
│   ├── 01_collect_data.py
│   ├── 02_prepare_training_data.py
│   ├── 03_finetune_llama.py
│   ├── 04_build_rag.py
│   ├── 05_analysis_pipeline.py
│   └── 06_testing_validation.py
│
├── notebooks/
│   ├── exploratory_analysis.ipynb
│   └── results_visualization.ipynb
│
├── configs/
│   ├── model_config.yaml
│   ├── training_config.yaml
│   └── rag_config.yaml
│
├── output/
│   ├── analyses/               # Análises geradas
│   ├── logs/                   # Logs de execução
│   └── reports/                # Relatórios de qualidade
│
├── requirements.txt
├── setup.sh
├── README.md
└── LICENSE
```

---

## 🛠️ Tecnologias Utilizadas

- **LLM**: Llama 3.1 (13B ou 70B)
- **RAG**: LangChain + Chroma
- **Embeddings**: Sentence-Transformers (multilingual)
- **Hardware**: MacBook M1/Max ou Google Cloud GPU
- **Framework**: PyTorch + Hugging Face

---

## 📊 Performance Esperada

### MacBook M1 Max (64GB RAM)
- **Coleta de dados**: 2-3 horas
- **Preparação**: 1 hora
- **Fine-tune**: 4-6 horas (3 épocas)
- **RAG**: 1-2 horas
- **Total**: ~8-12 horas para setup completo

### Google Cloud (GPU P100)
- **Fine-tune**: 1-2 horas
- **Total**: ~5-6 horas para setup completo

---

## 📝 Exemplo de Uso

```python
from oracle_biblico import BiblicalOracleSystem

# Inicializar sistema
oracle = BiblicalOracleSystem(model="biblical_llama3.1")

# Analisar verso
result = oracle.analyze(
    reference="Gênesis 1:1",
    analysis_type="comprehensive",
    depth_level=5
)

print(result["analysis"])
print(f"Qualidade: {result['quality_score']:.2%}")
```

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/amazing`)
3. Commit suas mudanças (`git commit -m 'Add amazing feature'`)
4. Push para a branch (`git push origin feature/amazing`)
5. Abra um Pull Request

---

## 📄 Licença

MIT License - veja LICENSE para detalhes

---

## 👤 Autor

**Alex Lama** - alexernestslama@gmail.com

- 🎬 Video Producer @ Unlogice Records
- 🤖 AI/ML Specialist
- 📖 Biblical Text Processing Expert

---

## 📞 Suporte

Problemas ou dúvidas? Abra uma issue no GitHub!

---


## 🚀 Como Usar

### Opção 1: Interface Web (Recomendado)

#### 1. Iniciar o servidor

```bash
# Ativar ambiente virtual
source venv/bin/activate

# Iniciar Flask
python3 app.py
```

O servidor rodará em `http://localhost:5000`

#### 2. Abrir no navegador

- Acesse `http://localhost:5000` no seu navegador
- Interface visual Matrix-style com autenticação
- Análise em tempo real com 5 camadas bíblicas

---

### Opção 2: API REST (Programadores)

#### 2.1. Health Check

```bash
curl http://localhost:5000/api/health
```

**Resposta:**
```json
{"status": "ok", "version": "1.0.0"}
```

#### 2.2. Analisar Texto Bíblico

```bash
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"query": "Profecia sobre cometa na biblia"}'
```

**Resposta (Exemplo):**
```json
{
  "query": "Profecia sobre cometa na biblia",
  "analysis": {
    "linguistica": {"resultado": "..."},
    "numerica": {"resultado": "..."},
    "historica": {"resultado": "..."},
    "teologica": {"resultado": "..."},
    "integrada": {"resultado": "..."}
  },
  "timestamp": "2025-12-10T03:45:22"
}
```

#### 2.3. Obter Resultados Anteriores

```bash
curl http://localhost:5000/api/results
```

---

### Opção 3: CLI - Linha de Comando

```bash
# Ativar ambiente
source venv/bin/activate

# Executar análise
python3 scripts/analysis_pipeline.py "Sua pergunta bíblica aqui"

# Ver resultado em JSON formatado
cat outputs/analysis_results.json | python3 -m json.tool
```

**Exemplo:**

```bash
python3 scripts/analysis_pipeline.py "Significado de Apocalipse 12:1"
```

Resultados salvos em: `outputs/analysis_results.json`

---

### Opção 4: Integração com Open WebUI

#### Se você usa Open WebUI (Ollama):

```bash
# Terminal 1: Iniciar ollama (se necessário)
ollama serve

# Terminal 2: Iniciar Flask API
source venv/bin/activate
python3 app.py

# Terminal 3: Acessar Open WebUI
# http://localhost:3000
```

Configure o modelo customizado para chamar:
```
http://localhost:5000/api/analyze
```

---

## 🔧 Configurações

### Variáveis de Ambiente

Crie um `.env` file (opcional):

```env
FLASK_ENV=development
FLASK_PORT=5000
LLAMA_MODEL=llama2
RAG_ENABLED=true
CHROMA_DB_PATH=./chromadb
```

### Melhorar Performance

**M1/M2 Mac:**
```bash
# Use aceleração GPU
export PYTORCH_ENABLE_MPS_FALLBACK=1
python3 app.py
```

**Google Cloud:**
```bash
# Deploy com gcloud
gcloud app deploy
```

---

## 📊 Exemplos de Queries Bíblicas

```bash
# Análise de passagens
"Qual é o significado de João 1:1?"

# Análise de conceitos
"O que significa 'Logos' no Evangelho de João?"

# Análise de profecias
"Profecia sobre cometa na Bíblia"

# Análise de números
"Significado numerológico de 666 em Apocalipse"

# Análise histórica
"Contexto histórico de Belém no nascimento de Jesus"
```

---

## 🐛 Troubleshooting

### Problema: Porta 5000 já em uso

```bash
# Encontrar processo usando porta
lsof -ti:5000 | xargs kill -9

# Ou usar outra porta
FLASK_PORT=5001 python3 app.py
```

### Problema: ModuleNotFoundError

```bash
# Reinstalar dependências
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

### Problema: Erro de Python 3.15

```bash
# Usar Python 3.12
brew install python@3.12
python3.12 -m venv venv_new
source venv_new/bin/activate
pip install -r requirements.txt
```

---

## 💱 Próximos Passos

- [ ] Deploy em produção (Heroku/AWS/GCP)
- [ ] Adicionar autenticação OAuth2
- [ ] Mobile app (React Native)
- [ ] Dashboard de análises históricas
- [ ] Exportar resultados (PDF/Excel)

**Criado com ❤️ para questão bíblica profunda e análise estruturada**
