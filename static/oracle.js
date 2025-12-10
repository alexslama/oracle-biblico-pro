// Oracle Bíblico PRO - JavaScript Functionality

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
  initializeApp();
});

function initializeApp() {
  // Get form element
  const form = document.getElementById('analysisForm');
  
  if (form) {
    form.addEventListener('submit', function(e) {
      e.preventDefault();
      handleAnalysis();
    });
  }
}

// Handle analysis submission
async function handleAnalysis() {
  const queryInput = document.getElementById('queryInput');
  const query = queryInput?.value;
  
  if (!query || query.trim() === '') {
    showError('Por favor, digite uma pergunta bíblica');
    return;
  }
  
  // Show results section and hide error
  const resultsSection = document.getElementById('resultsSection');
  const errorSection = document.getElementById('errorSection');
  const statusDiv = document.getElementById('status');
  
  if (resultsSection) {
    resultsSection.classList.remove('hidden');
  }
  if (errorSection) {
    errorSection.classList.add('hidden');
  }
  if (statusDiv) {
    statusDiv.innerHTML = '<span class="status-dot"></span> <span>Processando...</span>';
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
        statusDiv.innerHTML = '<span class="status-dot"></span> <span>Análise concluída</span>';
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
  
  let html = '';
  
  // Map of result keys to display labels
  const resultMap = {
    'linguistic_analysis': 'Lingüística',
    'hebrew_greek_analysis': 'Hebráico/Grego Antigos',
    'numeric_analysis': 'Númérica',
    'gematria_analysis': 'Gematria com Valores Hebraicos',
    'historical_analysis': 'Histórica',
    'archaeological_context': 'Contexto Arqueológico',
    'theological_analysis': 'Teológica',
    'divine_concepts': 'Conceitos Divinos',
    'integrated_synthesis': 'Síntese Integrada',
    'complete_conclusion': 'Conclusão Completa da Análise'
  };
  
  // Build results HTML
  for (const [key, label] of Object.entries(resultMap)) {
    if (data[key]) {
      html += '<div class="result-item">';
      html += '<div class="result-label">' + label + '</div>';
      html += '<div class="result-value">' + escapeHtml(data[key]) + '</div>';
      html += '</div>';
    }
  }
  
  resultsDiv.innerHTML = html;
  
  // Smooth fade-in animation
  resultsDiv.style.opacity = '0';
  setTimeout(() => {
    resultsDiv.style.transition = 'opacity 0.3s ease-in';
    resultsDiv.style.opacity = '1';
  }, 10);
}

// Show error message
function showError(message) {
  const resultsSection = document.getElementById('resultsSection');
  const errorSection = document.getElementById('errorSection');
  const errorMessage = document.getElementById('errorMessage');
  
  if (resultsSection) {
    resultsSection.classList.add('hidden');
  }
  if (errorSection) {
    errorSection.classList.remove('hidden');
  }
  if (errorMessage) {
    errorMessage.innerHTML = escapeHtml(message);
  }
  
  const statusDiv = document.getElementById('status');
  if (statusDiv) {
    statusDiv.innerHTML = '<span class="status-dot"></span> <span style="color: #ff6b6b;">Erro na análise</span>';
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
