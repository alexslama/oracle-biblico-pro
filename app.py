#!/usr/bin/env python3
"""
Oracle Biblico PRO - Web Interface with Matrix-like Biblical Theme
Modern API backend with enhanced analysis pipeline
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import json
from pathlib import Path
from typing import Dict, List
import sys
sys.path.insert(0, str(Path(__file__).parent / 'scripts'))

from analysis_pipeline import BiblicalAnalysisPipeline

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

# Initialize pipeline
pipeline = BiblicalAnalysisPipeline()

# Routes
@app.route('/')
def index():
    """Serve main interface"""
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    """API endpoint for biblical analysis"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        # Execute analysis
        result = pipeline.analyze(query)
        
        return jsonify({
            'status': 'success',
            'query': query,
            'analysis': result,
            'layers': result.get('analysis_layers', []),
            'synthesis': result.get('synthesis', {})
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/results')
def get_results():
    """Retrieve last analysis results"""
    try:
        results_file = Path('outputs/analysis_results.json')
        if results_file.exists():
            with open(results_file, 'r', encoding='utf-8') as f:
                results = json.load(f)
            return jsonify({
                'status': 'success',
                'results': results
            }), 200
        else:
            return jsonify({
                'status': 'error',
                'message': 'No results found'
            }), 404
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Oracle Biblico PRO',
        'version': '1.0.0'
    }), 200

if __name__ == '__main__':
    print("")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║  🔮 Oracle Biblico PRO - Web Interface                     ║")
    print("║  Biblical Analysis with Matrix-like Mystique              ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print("")
    print("🌐 Starting server...")
    print("📱 Access interface: http://localhost:5000")
    print("")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
