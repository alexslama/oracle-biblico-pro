// SHAMIR - Oracle Biblico - JavaScript Functionality
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
        console.log('DEBUG - Received data:', data);

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

    // Process analysis_layers (array of layer objects)
    // FIX: Check length > 0 to avoid treating empty array as truthy
    const layers = (data.analysis?.analysis_layers && data.analysis.analysis_layers.length > 0) 
                   ? data.analysis.analysis_layers 
                   : (data.layers && data.layers.length > 0) 
                     ? data.layers 
                     : [];
                     
    if (layers.length > 0) {
        layers.forEach((layer, index) => {
            // Each layer is an object with one key (e.g., {"language_layer": {...}})
            for (const [layerKey, layerData] of Object.entries(layer)) {
                const layerTitle = formatLayerTitle(layerKey);
                html += `<div class="result-item">`;
                html += `<h3>${layerTitle}</h3>`;
                html += `<p>${formatLayerContent(layerData)}</p>`;
                html += `</div>`;
            }
        });
    }

    // Process synthesis (object)
    const synthesis = data.analysis?.synthesis || data.synthesis || {};
    if (Object.keys(synthesis).length > 0) {
        html += `<div class="result-item">`;
        html += `<h3>🔮 Síntese Integrada</h3>`;
        html += `<p>${formatLayerContent(synthesis)}</p>`;
        html += `</div>`;
    }

    // Fallback: display raw data if no layers found
    if (html === '') {
        html = `<div class="result-item">`;
        html += `<h3>Revelação do Oráculo</h3>`;
        html += `<p>${escapeHtml(JSON.stringify(data, null, 2))}</p>`;
        html += `</div>`;
    }

    resultsDiv.innerHTML = html;

    // Smooth fade-in effect
    resultsDiv.style.opacity = '0';
    setTimeout(() => {
        resultsDiv.style.opacity = '1';
    }, 50);
}

// Helper function to format layer titles
function formatLayerTitle(key) {
    const titles = {
        'language_layer': '📖 Análise Linguística',
        'linguistic_layer': '📖 Análise Linguística',
        'numerical_layer': '🔢 Análise Numérica (Gematria)',
        'historical_layer': '🏛️ Contexto Histórico',
        'theological_layer': '✝️ Análise Teológica',
        'integrated_synthesis': '🔮 Síntese Integrada'
    };
    return titles[key] || key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
}

// Helper function to format layer content
function formatLayerContent(content) {
    if (typeof content === 'string') {
        return escapeHtml(content);
    }
    if (Array.isArray(content)) {
        return content.map(item => escapeHtml(JSON.stringify(item))).join(', ');
    }
    if (typeof content === 'object' && content !== null) {
        let formatted = '';
        for (const [key, value] of Object.entries(content)) {
            const label = key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
            if (Array.isArray(value)) {
                formatted += `<strong>${label}:</strong> ${value.join(', ')}<br>`;
            } else if (typeof value === 'object') {
                formatted += `<strong>${label}:</strong> ${JSON.stringify(value)}<br>`;
            } else {
                formatted += `<strong>${label}:</strong> ${value}<br>`;
            }
        }
        return formatted;
    }
    return escapeHtml(String(content));
}

// Display error message
function showError(message) {
    const resultsSection = document.getElementById('resultsSection');
    const errorSection = document.getElementById('errorSection');
    const errorMessage = document.getElementById('errorMessage');

    if (resultsSection) resultsSection.classList.add('hidden');
    if (errorSection) errorSection.classList.remove('hidden');
    if (errorMessage) errorMessage.innerHTML = '❌ Erro na análise'; 

    const statusDiv = document.getElementById('status');
    if (statusDiv) statusDiv.innerHTML = '❌ ' + escapeHtml(message);
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
