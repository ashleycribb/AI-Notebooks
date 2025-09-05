"""
Web interface for AI-Notebooks with enhanced features.

This Flask application provides a web-based interface for:
- Interactive model playground
- Notebook management
- AI assistant integration
"""

import os
import json
import asyncio
from datetime import datetime
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_socketio import SocketIO, emit
import nbformat
from nbconvert import HTMLExporter
import openai
import anthropic
import google.generativeai as genai


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'ai-notebooks-secret-key')
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize AI clients
ai_clients = {}

def setup_ai_clients():
    """Initialize AI clients based on available API keys."""
    global ai_clients
    
    if os.getenv('OPENAI_API_KEY'):
        ai_clients['openai'] = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    if os.getenv('ANTHROPIC_API_KEY'):
        ai_clients['anthropic'] = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
    
    if os.getenv('GOOGLE_API_KEY'):
        genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
        ai_clients['gemini'] = genai.GenerativeModel('gemini-pro')


@app.route('/')
def index():
    """Main dashboard page."""
    notebooks = get_notebook_list()
    return render_template('index.html', notebooks=notebooks)


@app.route('/playground')
def playground():
    """Model playground page."""
    available_models = list(ai_clients.keys())
    return render_template('playground.html', models=available_models)


@app.route('/notebook/<path:notebook_path>')
def view_notebook(notebook_path):
    """View a notebook in HTML format."""
    try:
        notebook_file = Path('notebooks') / notebook_path
        if not notebook_file.exists():
            return "Notebook not found", 404
        
        with open(notebook_file, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)
        
        html_exporter = HTMLExporter()
        html_exporter.template_name = 'classic'
        
        (body, resources) = html_exporter.from_notebook_node(nb)
        
        return render_template('notebook_viewer.html', 
                             notebook_html=body, 
                             notebook_path=notebook_path)
    
    except Exception as e:
        return f"Error loading notebook: {str(e)}", 500


@app.route('/api/models')
def api_models():
    """Get available AI models."""
    return jsonify({
        'models': list(ai_clients.keys()),
        'status': 'success'
    })


@app.route('/api/chat', methods=['POST'])
def api_chat():
    """Chat with AI models."""
    data = request.json
    prompt = data.get('prompt', '')
    model = data.get('model', 'auto')
    temperature = data.get('temperature', 0.7)
    
    if not prompt:
        return jsonify({'error': 'No prompt provided'}), 400
    
    if model == 'auto' and ai_clients:
        model = list(ai_clients.keys())[0]
    
    if model not in ai_clients:
        return jsonify({'error': f'Model {model} not available'}), 400
    
    try:
        response = get_ai_response(model, prompt, temperature)
        return jsonify({
            'response': response,
            'model': model,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/compare', methods=['POST'])
def api_compare():
    """Compare responses from multiple models."""
    data = request.json
    prompt = data.get('prompt', '')
    models = data.get('models', [])
    temperature = data.get('temperature', 0.7)
    
    if not prompt or not models:
        return jsonify({'error': 'Prompt and models required'}), 400
    
    results = []
    for model in models:
        if model in ai_clients:
            try:
                start_time = datetime.now()
                response = get_ai_response(model, prompt, temperature)
                end_time = datetime.now()
                
                results.append({
                    'model': model,
                    'response': response,
                    'response_time': (end_time - start_time).total_seconds(),
                    'timestamp': start_time.isoformat()
                })
            
            except Exception as e:
                results.append({
                    'model': model,
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                })
    
    return jsonify({'results': results})


@app.route('/api/notebooks')
def api_notebooks():
    """Get list of available notebooks."""
    notebooks = get_notebook_list()
    return jsonify({'notebooks': notebooks})


@app.route('/api/notebook/<path:notebook_path>/metadata')
def api_notebook_metadata(notebook_path):
    """Get notebook metadata."""
    try:
        notebook_file = Path('notebooks') / notebook_path
        if not notebook_file.exists():
            return jsonify({'error': 'Notebook not found'}), 404
        
        with open(notebook_file, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)
        
        metadata = {
            'title': nb.metadata.get('title', notebook_path),
            'cells': len(nb.cells),
            'code_cells': len([cell for cell in nb.cells if cell.cell_type == 'code']),
            'markdown_cells': len([cell for cell in nb.cells if cell.cell_type == 'markdown']),
            'last_modified': datetime.fromtimestamp(notebook_file.stat().st_mtime).isoformat()
        }
        
        return jsonify(metadata)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@socketio.on('connect')
def handle_connect():
    """Handle client connection."""
    emit('status', {'message': 'Connected to AI-Notebooks server'})


@socketio.on('run_model')
def handle_run_model(data):
    """Handle real-time model execution."""
    prompt = data.get('prompt', '')
    model = data.get('model', 'auto')
    temperature = data.get('temperature', 0.7)
    
    if model == 'auto' and ai_clients:
        model = list(ai_clients.keys())[0]
    
    if model not in ai_clients:
        emit('model_error', {'error': f'Model {model} not available'})
        return
    
    try:
        emit('model_start', {'model': model})
        response = get_ai_response(model, prompt, temperature)
        emit('model_response', {
            'model': model,
            'response': response,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        emit('model_error', {'error': str(e), 'model': model})


def get_ai_response(model: str, prompt: str, temperature: float = 0.7) -> str:
    """Get response from AI model."""
    if model == 'openai':
        response = ai_clients['openai'].chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=1000
        )
        return response.choices[0].message.content
    
    elif model == 'anthropic':
        response = ai_clients['anthropic'].messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1000,
            temperature=temperature,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    
    elif model == 'gemini':
        response = ai_clients['gemini'].generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=1000
            )
        )
        return response.text
    
    else:
        raise ValueError(f"Unknown model: {model}")


def get_notebook_list():
    """Get list of available notebooks."""
    notebooks = []
    notebooks_dir = Path('notebooks')
    
    if notebooks_dir.exists():
        for notebook_file in notebooks_dir.rglob('*.ipynb'):
            relative_path = notebook_file.relative_to(notebooks_dir)
            notebooks.append({
                'path': str(relative_path),
                'name': notebook_file.stem,
                'category': relative_path.parent.name if relative_path.parent != Path('.') else 'root',
                'size': notebook_file.stat().st_size,
                'modified': datetime.fromtimestamp(notebook_file.stat().st_mtime).isoformat()
            })
    
    return sorted(notebooks, key=lambda x: x['category'])


@app.route('/static/<path:filename>')
def static_files(filename):
    """Serve static files."""
    return send_from_directory('static', filename)


if __name__ == '__main__':
    setup_ai_clients()
    
    # Development server
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    print(f"🚀 Starting AI-Notebooks Web Interface on port {port}")
    print(f"📊 Available AI models: {list(ai_clients.keys())}")
    
    socketio.run(app, host='0.0.0.0', port=port, debug=debug)