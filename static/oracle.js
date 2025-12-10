// Oracle Bíblico PRO - JavaScript Functionality

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
  initializeApp();
});

function initializeApp() {
  // Get elements
  const analisarBtn = document.getElementById('analisar-btn');
  const queryInput = document.getElementById('query-input');
  
  if (analisarBtn) {
    analisarBtn.addEventListener('click', handleAnalysis);
  }
  
  if (queryInput) {
    queryInput.addEventListener('keypress', function(e) {
      if (e.key === 'Enter') {
        handleAnalysis();
      }
    });
  }
  
  // Generate binary rain
  generateBinaryRain();
  
  // Add hover effects
  addHoverEffects();
}

// Handle analysis submission
async function handleAnalysis() {
  const query = document.getElementById('query-input')?.value;
  
  if (!query || query.trim() === '') {
    showError('Por favor, digite uma pergunta bíbliCa');
    return;
  }
  
  const resultsDiv = document.getElementById('results');
  const statusDiv = document.getElementById('status');
  
  if (statusDiv) {
    statusDiv.innerHTML = '<span class="status"></span> Processando com Llama 3.1 + RAG...';
  }
  
  if (resultsDiv) {
    resultsDiv.innerHTML = '';
  }
  
  try {
    const response = await fetch('/api/analyze', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query: query })
    });
    
    const data = await response.json();
    
    if (response.ok) {
      displayResults(data);
      if (statusDiv) {
        statusDiv.innerHTML = '<span class="status"></span> Análise concluída';
      }
    } else {
      showError(data.error || 'Erro ao processar a análise');
    }
  } catch (error) {
    showError('Erro de conexão: ' + error.message);
  }
}

// Display results from API
function displayResults(data) {
  const resultsDiv = document.getElementById('results');
  if (!resultsDiv) return;
  
  let html = '<div class="result-item">';
  
  if (data.linguistic_analysis) {
    html += '<div class="result-label">Lingüística</div>';
    html += '<div class="result-value">' + escapeHtml(data.linguistic_analysis) + '</div>';
  }
  
  if (data.hebrew_greek_analysis) {
    html += '<div class="result-label">Hebraico/Grego Antigos</div>';
    html += '<div class="result-value">' + escapeHtml(data.hebrew_greek_analysis) + '</div>';
  }
  
  if (data.numeric_analysis) {
    html += '<div class="result-label">Numérica</div>';
    html += '<div class="result-value">' + escapeHtml(data.numeric_analysis) + '</div>';
  }
  
  if (data.gematria_analysis) {
    html += '<div class="result-label">Gematria com Valores Hebraicos</div>';
    html += '<div class="result-value">' + escapeHtml(data.gematria_analysis) + '</div>';
  }
  
  if (data.historical_analysis) {
    html += '<div class="result-label">Histórica</div>';
    html += '<div class="result-value">' + escapeHtml(data.historical_analysis) + '</div>';
  }
  
  if (data.archaeological_context) {
    html += '<div class="result-label">Contexto Arqueológico</div>';
    html += '<div class="result-value">' + escapeHtml(data.archaeological_context) + '</div>';
  }
  
  if (data.theological_analysis) {
    html += '<div class="result-label">Teológica</div>';
    html += '<div class="result-value">' + escapeHtml(data.theological_analysis) + '</div>';
  }
  
  if (data.divine_concepts) {
    html += '<div class="result-label">Conceitos Divinos</div>';
    html += '<div class="result-value">' + escapeHtml(data.divine_concepts) + '</div>';
  }
  
  if (data.integrated_synthesis) {
    html += '<div class="result-label">Síntese Integrada</div>';
    html += '<div class="result-value">' + escapeHtml(data.integrated_synthesis) + '</div>';
  }
  
  if (data.complete_conclusion) {
    html += '<div class="result-label">Conclusão Completa da Análise</div>';
    html += '<div class="result-value">' + escapeHtml(data.complete_conclusion) + '</div>';
  }
  
  html += '</div>';
  resultsDiv.innerHTML = html;
  
  // Add animation
  resultsDiv.style.opacity = '0';
  setTimeout(() => {
    resultsDiv.style.transition = 'opacity 0.5s ease';
    resultsDiv.style.opacity = '1';
  }, 10);
}

// Show error message
function showError(message) {
  const resultsDiv = document.getElementById('results');
  if (resultsDiv) {
    resultsDiv.innerHTML = '<div class="panel" style="color: #ff6b6b; border-color: #ff6b6b;">' + 
                           '<strong>ERRO:</strong> ' + escapeHtml(message) + '</div>';
  }
  
  const statusDiv = document.getElementById('status');
  if (statusDiv) {
    statusDiv.innerHTML = '<span style="color: #ff6b6b;">Erro na análise</span>';
  }
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
  if (!text) return '';
  const map = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#039;'
  };
  return text.toString().replace(/[&<>"']/g, m => map[m]);
}

// Generate random binary text for the rain effect
function generateBinaryRain() {
  const binaryRain = document.querySelector('.binary-rain');
  if (!binaryRain) return;
  
  const binary = '01'.repeat(100);
  binaryRain.textContent = binary;
}

// Add hover effects to panels
function addHoverEffects() {
  const panels = document.querySelectorAll('.panel');
  panels.forEach(panel => {
    panel.addEventListener('mouseenter', function() {
      this.style.transform = 'translateY(-2px)';
    });
    panel.addEventListener('mouseleave', function() {
      this.style.transform = 'translateY(0)';
    });
  });
}

// Utility function to format timestamp
function formatTimestamp() {
  return new Date().toLocaleString('pt-BR');
}
