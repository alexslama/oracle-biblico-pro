# 🚀 Oracle Biblico PRO - QUICK START

## UM COMANDO PARA DEPLOY COMPLETO

Seu sistema está pronto! Execute isto no Terminal do seu Mac M1 Max:

```bash
bash <(curl -s https://raw.githubusercontent.com/alexslama/oracle-biblico-pro/main/DEPLOY_M1_MAC.sh)
```

OU, se preferir fazer manualmente:

```bash
git clone https://github.com/alexslama/oracle-biblico-pro.git
cd oracle-biblico-pro
bash DEPLOY_M1_MAC.sh
```

## O que vai acontecer?

O script `DEPLOY_M1_MAC.sh` executa automaticamente:

1. ✅ Verifica Python 3.10+
2. ✅ Clona o repositório
3. ✅ Cria ambiente virtual
4. ✅ Instala 30+ dependências
5. ✅ Cria estrutura de diretórios
6. ✅ Ativa otimizações Metal (M1 Max)
7. ✅ Coleta textos bíblicos
8. ✅ Prepara dados de treinamento
9. ✅ Configura fine-tuning Llama3.1
10. ✅ Constrói sistema RAG

**Tempo estimado: 15-20 minutos**

## Após o Deployment

```bash
# Ativar ambiente (sempre que abrir novo terminal)
cd oracle-biblico-pro
source venv/bin/activate

# Executar análise bíblica
python3 scripts/analysis_pipeline.py "Profecia sobre cometa na biblia"

# Ver resultados
cat outputs/analysis_results.json | python3 -m json.tool
```

## Arquivos Principais

| Arquivo | Função |
|---------|--------|
| `DEPLOY_M1_MAC.sh` | Script de deployment automático |
| `setup.sh` | Configuração manual do ambiente |
| `requirements.txt` | Dependências Python (30+ pacotes) |
| `scripts/collect_data.py` | Coleta textos bíblicos |
| `scripts/prepare_training_data.py` | Prepara dados em formato JSONL |
| `scripts/finetune_llama.py` | Configura fine-tuning Llama3.1 |
| `scripts/build_rag.py` | Constrói sistema RAG com FAISS |
| `scripts/analysis_pipeline.py` | Análise de 5 camadas (seu Oracle) |

## Troubleshooting

**Python não encontrado**
```bash
brew install python@3.10
```

**Permissão negada no script**
```bash
chmod +x DEPLOY_M1_MAC.sh
bash DEPLOY_M1_MAC.sh
```

**Llama3.1 não carrega**
```bash
brew install ollama
ollama pull llama3.1
```

## Status do Deployment

✅ **Repositório GitHub**: https://github.com/alexslama/oracle-biblico-pro

✅ **Todos os arquivos**: README + Scripts + Requirements + Deploy Automation

✅ **Otimizado para**: MacBook M1 Max com 64GB RAM

✅ **Funcionalidade**: 5-layer biblical analysis pipeline

---

**Pronto para começar? Execute o comando acima e seu Oracle Biblico PRO estará operacional em 20 minutos! 🎉**
