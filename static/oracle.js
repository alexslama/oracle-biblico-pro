// SHAMIR - Oracle Bíblico - JavaScript Functionality
// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
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
        showError('Por favor, digite uma pergunta para o oráculo');
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
        statusDiv.innerHTML = '⏳ Processando...';
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
                statusDiv.innerHTML = '✅ Análise concluída';
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

    // Get analysis from the response
    const analysis = data.analysis || {};

    // Map of result keys to display labels
    const resultMap = {
        'linguistic_analysis': 'Análise Linguística',
        'hebrew_greek_analysis': 'Análise Hebraico/Grego',
        'numeric_analysis': 'Análise Numérica',
        'gematria_analysis': 'Gematria com Valores Hebraicos',
        'historical_analysis': 'Análise Histórica',
        'archaeological_context': 'Contexto Arqueológico',
        'theological_analysis': 'Análise Teológica',
        'divine_concepts': 'Conceitos Divinos',
        'integrated_synthesis': 'Síntese Integrada',
        'complete_conclusion': 'Conclusão Completa'
    };

    // Build results HTML
    for (const [key, label] of Object.entries(resultMap)) {
        if (analysis[key]) {
            html += `<div class="result-item">`;
            html += `<h3>${label}</h3>`;
            html += `<p>${escapeHtml(analysis[key])}</p>`;
            html += `</div>`;
        }
    }

    if (html === '') {
        // Fallback: display raw analysis if no specific keys found
        html = `<div class="result-item">
                    <h3>Revelação do Oráculo</h3>
                    <p>${escapeHtml(JSON.stringify(analysis, null, 2))}</p>
                </div>`;
    }

    resultsDiv.innerHTML = html;

    // Smooth fade-in effect
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
        statusDiv.innerHTML = '❌ Erro na análise';
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
