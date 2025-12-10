# 🔮 Oracle Biblico PRO - Web Interface Guide

## Overview

Web interface moderna e misteriosa inspirada em Matrix para análise bíblica com IA.

### Features

✨ **Interface Mysteriosa**
- Tema dark com símbolos bíblicos
- Animações fluidas e glowing effects
- Layout responsivo (mobile + desktop)
- Real-time analysis updates

🔍 **5-Layer Biblical Analysis**
- Linguistic (Hebraico/Grego/Aramaico)
- Numerical (Gematria Values)
- Historical (Archaeological Context)
- Theological (Divine Concepts)
- Integrated (Complete Synthesis)

⚡ **API Backend**
- Flask REST API
- CORS enabled
- JSON responses
- Health checks

---

## Installation & Setup

### 1. Install Dependencies

```bash
# Add Flask and CORS
pip install flask flask-cors

# Or update requirements.txt
echo 'flask>=2.3.0' >> requirements.txt
echo 'flask-cors>=4.0.0' >> requirements.txt
pip install -r requirements.txt
```

### 2. Create Template Directories

```bash
mkdir -p templates/
mkdir -p static/css/
mkdir -p static/js/
```

### 3. Start the Web Server

```bash
# Ativar ambiente virtual
source venv/bin/activate

# Rodar servidor Flask
python3 app.py

# Será acessível em: http://localhost:5000
```

---

## API Endpoints

### POST /api/analyze
Executa análise bíblica completa

**Request:**
```json
{
  "query": "Profecia sobre cometa na biblia"
}
```

**Response:**
```json
{
  "status": "success",
  "query": "Profecia sobre cometa na biblia",
  "layers": [
    {"language_layer": {...}},
    {"numerical_layer": {...}},
    {"historical_layer": {...}},
    {"theological_layer": {...}}
  ],
  "synthesis": {"integrated_synthesis": {...}}
}
```

### GET /api/results
Retorna últimos resultados de análise

**Response:**
```json
{
  "status": "success",
  "results": {...previous analysis...}
}
```

### GET /api/health
Verifica saúde do servidor

**Response:**
```json
{
  "status": "healthy",
  "service": "Oracle Biblico PRO",
  "version": "1.0.0"
}
```

---

## Interface Components

### Main Elements

1. **Search Bar** - Input para queries bíblicas
2. **Analysis Layers** - Cards mostrando cada camada de análise
3. **Synthesis Panel** - Síntese integrada dos resultados
4. **Console Output** - Real-time analysis updates
5. **Bible References** - Links para passagens bíblicas

### Design Philosophy

- **Dark Theme** com tons verdes/dourados (Matrix + Bíblico)
- **Hebrew/Greek** símbolos como decorações
- **Glow Effects** para destacar elementos importantes
- **Smooth Animations** para transições
- **Sacred Geometry** inspiração visual

---

## Usage Examples

### Via cURL

```bash
# Análise simples
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"query": "Profecia sobre cometa"}'

# Verificar saúde
curl http://localhost:5000/api/health
```

### Via Python

```python
import requests
import json

response = requests.post(
    'http://localhost:5000/api/analyze',
    json={'query': 'Profecia sobre cometa'}
)

results = response.json()
print(json.dumps(results, indent=2, ensure_ascii=False))
```

### Via JavaScript (Fetch)

```javascript
fetch('/api/analyze', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({query: 'Profecia sobre cometa'})
})
.then(r => r.json())
.then(data => console.log(data));
```

---

## Integration com OpenWebUI

### Opção 1: Direct Integration

```bash
# Se OpenWebUI está em localhost:3000
# Conectar análises do Oracle Biblico ao OpenWebUI

curl http://localhost:5000/api/results | \
  curl -X POST http://localhost:3000/api/chat \
    -H "Content-Type: application/json" \
    -d @-
```

### Opção 2: Via API Gateway

Criar endpoint que combina ambos:

```python
@app.route('/api/combined-analysis', methods=['POST'])
def combined():
    # Executar análise local
    local_result = pipeline.analyze(query)
    
    # Enviar para OpenWebUI
    openwebui_result = requests.post(
        'http://localhost:3000/api/chat',
        json={'content': str(local_result)}
    )
    
    return jsonify({
        'oracle': local_result,
        'openwebui': openwebui_result.json()
    })
```

---

## File Structure

```
oracle-biblico-pro/
├── app.py                          # Flask backend
├── templates/
│   └── index.html                 # Interface principal
├── static/
│   ├── css/
│   │   └── style.css              # Estilos Matrix + Bíblico
│   └── js/
│       └── interface.js           # Interatividade
├── scripts/
│   └── analysis_pipeline.py       # Core analysis
├── outputs/
│   └── analysis_results.json      # Últimos resultados
└── requirements.txt               # Dependências Python
```

---

## Troubleshooting

### Port 5000 já em uso

```bash
# Usar porta diferente
python3 app.py --port 8000

# Ou matar processo existente
lsof -ti:5000 | xargs kill -9
```

### CORS Errors

```python
# Adicionar origins customizados
CORS(app, resources={
    r"/api/*": {"origins": ["http://localhost:3000"]}
})
```

### Analysis takes too long

```python
# Adicionar timeout
@app.route('/api/analyze', methods=['POST'])
def analyze():
    # ...
    result = pipeline.analyze(query)  # Aumentar timeout se necessário
```

---

## Performance Tips

1. **Cache Results** - Guardar análises frequentes
2. **Async Processing** - Usar Celery para tasks longas
3. **Database** - SQLite para persistência de resultados
4. **Rate Limiting** - Proteger API de abuso

---

## Next Steps

- [ ] Criar HTML interface (index.html)
- [ ] Estilizar com CSS mystérioso (style.css)
- [ ] Adicionar JavaScript interativo (interface.js)
- [ ] Integrar com banco de dados
- [ ] Adicionar autenticação
- [ ] Deploy em produção (Heroku/AWS)

---

## Support

Para dúvidas ou bugs:
1. Check logs: `tail -f logs/app.log`
2. Test API: `curl http://localhost:5000/api/health`
3. Verify pipeline: `python3 scripts/analysis_pipeline.py 'test query'`

---

**Oracle Biblico PRO** © 2025 | Matrix-like Biblical Analysis with AI
