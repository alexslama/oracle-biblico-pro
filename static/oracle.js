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
                html += `<button class="voice-btn" onclick="if(audioManager) audioManager.speakAnalysis('${layerTitle}', '${formatLayerContent(layerData).replace(/'/g, "\\'")}')" title="Ouvir com voz celestial">🔊</button>`;
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

// ═══════════════════════════════════════════════════════
// 🔮 DIVINE AUDIO & CELESTIAL VOICE SYSTEM
// ═══════════════════════════════════════════════════════

class DivineAudioManager {
    constructor() {
        this.ambientAudio = null;
        this.isPlaying = false;
        this.ttsVoice = null;
        this.initializeAudio();
    }

    initializeAudio() {
        // Carregar áudio ambiente (será gerado pelo script Python)
        this.ambientAudio = new Audio('/static/audio/divine_blend.wav');
        this.ambientAudio.loop = true;
        this.ambientAudio.volume = 0.15; // Volume baixo e ambiente
        
        // Inicializar Text-to-Speech
        this.initializeTTS();
    }

    initializeTTS() {
        if ('speechSynthesis' in window) {
            // Aguardar vozes carregarem
            window.speechSynthesis.onvoiceschanged = () => {
                const voices = window.speechSynthesis.getVoices();
                // Procurar voz feminina em português (mais celestial)
                this.ttsVoice = voices.find(v => 
                    v.lang.startsWith('pt') && v.name.includes('Female')
                ) || voices.find(v => v.lang.startsWith('pt')) || voices[0];
                
                console.log('🎵 Voz celestial selecionada:', this.ttsVoice?.name);
            };
        }
    }

    playAmbient() {
        if (!this.ambientAudio || this.isPlaying) return;
        
        this.ambientAudio.play().then(() => {
            this.isPlaying = true;
            console.log('🎵 Áudio divino iniciado (432Hz + 528Hz)');
        }).catch(err => {
            console.log('⚠️ Áudio não disponível (executar: python3 scripts/generate_divine_audio.py)');
        });
    }

    stopAmbient() {
        if (this.ambientAudio && this.isPlaying) {
            this.ambientAudio.pause();
            this.ambientAudio.currentTime = 0;
            this.isPlaying = false;
        }
    }

    speak(text, options = {}) {
        if (!('speechSynthesis' in window)) {
            console.warn('⚠️ Text-to-Speech não suportado neste navegador');
            return;
        }

        // Cancelar falas anteriores
        window.speechSynthesis.cancel();

        const utterance = new SpeechSynthesisUtterance(text);
        utterance.voice = this.ttsVoice;
        utterance.rate = options.rate || 0.85;  // Mais devagar, celestial
        utterance.pitch = options.pitch || 1.1;  // Pitch ligeiramente mais alto
        utterance.volume = options.volume || 0.9;

        // Efeitos especiais
        utterance.onstart = () => {
            console.log('🔊 Voz celestial falando...');
        };

        utterance.onend = () => {
            console.log('✨ Revelação concluída');
        };

        window.speechSynthesis.speak(utterance);
    }

    speakAnalysis(layerTitle, content) {
        // Remove HTML tags e formata para fala
        const cleanContent = content
            .replace(/<[^>]*>/g, '')  // Remove HTML
            .replace(/&nbsp;/g, ' ')   // Substitui &nbsp;
            .replace(/\s+/g, ' ')      // Remove espaços extras
            .trim();

        const text = `${layerTitle}. ${cleanContent}`;
        this.speak(text);
    }
}

// Instância global
let audioManager = null;

// Inicializar no carregamento da página
document.addEventListener('DOMContentLoaded', function() {
    audioManager = new DivineAudioManager();
    
    // Tocar áudio ambiente após primeira interação (requisito dos navegadores)
    document.body.addEventListener('click', function initAudio() {
        if (audioManager && !audioManager.isPlaying) {
            audioManager.playAmbient();
        }
        document.body.removeEventListener('click', initAudio);
    }, { once: true });
});


// ═══════════════════════════════════════════════════════
// 🌟 BINARY CODE ANIMATION (Matrix Effect)
// ═══════════════════════════════════════════════════════

function animateBinaryCode() {
    const binaryElement = document.querySelector('.binary-code');
    if (!binaryElement) return;

    setInterval(() => {
        const length = 80; // Largura da tela em caracteres
        let binary = '';
        for (let i = 0; i < length; i++) {
            binary += Math.random() > 0.5 ? '1' : '0';
        }
        binaryElement.textContent = binary;
    }, 150);  // Atualiza a cada 150ms
}

// Iniciar animação binária
document.addEventListener('DOMContentLoaded', animateBinaryCode);
}
