"""
Interactive Model Playground for AI-Notebooks.

This module provides an interactive interface for experimenting with different
AI models, comparing outputs, and tracking usage costs.
"""

import os
import json
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime
import ipywidgets as widgets
from IPython.display import display, HTML, clear_output
import openai
import anthropic
import google.generativeai as genai


@dataclass
class ModelResponse:
    """Data class for storing model responses."""
    model: str
    prompt: str
    response: str
    timestamp: datetime
    tokens_used: int
    cost_estimate: float
    response_time: float


class ModelPlayground:
    """Interactive playground for testing and comparing AI models."""
    
    # Cost estimates per 1K tokens (approximate)
    COST_ESTIMATES = {
        'gpt-3.5-turbo': {'input': 0.0015, 'output': 0.002},
        'gpt-4': {'input': 0.03, 'output': 0.06},
        'claude-3-haiku': {'input': 0.00025, 'output': 0.00125},
        'claude-3-sonnet': {'input': 0.003, 'output': 0.015},
        'gemini-pro': {'input': 0.0005, 'output': 0.0015}
    }
    
    def __init__(self):
        self.clients = {}
        self.responses: List[ModelResponse] = []
        self.total_cost = 0.0
        self._setup_clients()
        self._create_interface()
    
    def _setup_clients(self):
        """Initialize AI clients based on available API keys."""
        # OpenAI
        if os.getenv('OPENAI_API_KEY'):
            self.clients['openai'] = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # Anthropic
        if os.getenv('ANTHROPIC_API_KEY'):
            self.clients['anthropic'] = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        
        # Google Gemini
        if os.getenv('GOOGLE_API_KEY'):
            genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
            self.clients['gemini'] = genai.GenerativeModel('gemini-pro')
    
    def _create_interface(self):
        """Create the interactive widget interface."""
        # Model selection
        available_models = []
        if 'openai' in self.clients:
            available_models.extend(['gpt-3.5-turbo', 'gpt-4'])
        if 'anthropic' in self.clients:
            available_models.extend(['claude-3-haiku', 'claude-3-sonnet'])
        if 'gemini' in self.clients:
            available_models.append('gemini-pro')
        
        if not available_models:
            self.model_selector = widgets.HTML(
                value='<div style="color: red;">No AI models available. Please configure API keys.</div>'
            )
            return
        
        # UI Components
        self.model_selector = widgets.SelectMultiple(
            options=available_models,
            value=[available_models[0]] if available_models else [],
            description='Models:',
            style={'description_width': 'initial'},
            layout=widgets.Layout(width='300px', height='120px')
        )
        
        self.prompt_input = widgets.Textarea(
            value='Explain the concept of machine learning in simple terms.',
            placeholder='Enter your prompt here...',
            description='Prompt:',
            style={'description_width': 'initial'},
            layout=widgets.Layout(width='100%', height='100px')
        )
        
        self.temperature_slider = widgets.FloatSlider(
            value=0.7,
            min=0.0,
            max=1.0,
            step=0.1,
            description='Temperature:',
            style={'description_width': 'initial'},
            layout=widgets.Layout(width='300px')
        )
        
        self.max_tokens_slider = widgets.IntSlider(
            value=500,
            min=50,
            max=2000,
            step=50,
            description='Max Tokens:',
            style={'description_width': 'initial'},
            layout=widgets.Layout(width='300px')
        )
        
        self.run_button = widgets.Button(
            description='🚀 Run Models',
            button_style='primary',
            layout=widgets.Layout(width='150px')
        )
        
        self.clear_button = widgets.Button(
            description='🗑️ Clear History',
            button_style='warning',
            layout=widgets.Layout(width='150px')
        )
        
        self.compare_button = widgets.Button(
            description='📊 Compare Results',
            button_style='info',
            layout=widgets.Layout(width='150px')
        )
        
        self.output_area = widgets.Output()
        self.cost_display = widgets.HTML(value='<b>Total Cost: $0.00</b>')
        
        # Event handlers
        self.run_button.on_click(self._run_models)
        self.clear_button.on_click(self._clear_history)
        self.compare_button.on_click(self._compare_results)
        
        # Layout
        controls_row1 = widgets.HBox([
            self.model_selector,
            widgets.VBox([self.temperature_slider, self.max_tokens_slider])
        ])
        
        controls_row2 = widgets.HBox([
            self.run_button,
            self.clear_button,
            self.compare_button,
            self.cost_display
        ])
        
        self.interface = widgets.VBox([
            widgets.HTML('<h2>🎮 AI Model Playground</h2>'),
            self.prompt_input,
            controls_row1,
            controls_row2,
            self.output_area
        ])
    
    def display(self):
        """Display the playground interface."""
        display(self.interface)
    
    def _run_models(self, button):
        """Run the selected models with the current prompt."""
        if not self.model_selector.value:
            with self.output_area:
                clear_output()
                print("⚠️ Please select at least one model.")
            return
        
        prompt = self.prompt_input.value.strip()
        if not prompt:
            with self.output_area:
                clear_output()
                print("⚠️ Please enter a prompt.")
            return
        
        with self.output_area:
            clear_output()
            print("🔄 Running models...")
        
        results = []
        for model in self.model_selector.value:
            try:
                start_time = time.time()
                response = self._get_model_response(
                    model, 
                    prompt, 
                    self.temperature_slider.value,
                    self.max_tokens_slider.value
                )
                end_time = time.time()
                
                # Estimate tokens and cost
                tokens_used = len(response.split()) * 1.3  # Rough estimate
                cost = self._estimate_cost(model, tokens_used)
                
                model_response = ModelResponse(
                    model=model,
                    prompt=prompt,
                    response=response,
                    timestamp=datetime.now(),
                    tokens_used=int(tokens_used),
                    cost_estimate=cost,
                    response_time=end_time - start_time
                )
                
                self.responses.append(model_response)
                self.total_cost += cost
                results.append(model_response)
                
            except Exception as e:
                with self.output_area:
                    print(f"❌ Error with {model}: {str(e)}")
        
        self._display_results(results)
        self._update_cost_display()
    
    def _get_model_response(self, model: str, prompt: str, temperature: float, max_tokens: int) -> str:
        """Get response from a specific model."""
        if model.startswith('gpt'):
            response = self.clients['openai'].chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        
        elif model.startswith('claude'):
            response = self.clients['anthropic'].messages.create(
                model=model.replace('claude-3-', 'claude-3-') + '-20240307',
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        
        elif model == 'gemini-pro':
            response = self.clients['gemini'].generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=temperature,
                    max_output_tokens=max_tokens
                )
            )
            return response.text
        
        else:
            raise ValueError(f"Unknown model: {model}")
    
    def _estimate_cost(self, model: str, tokens: int) -> float:
        """Estimate the cost for a model response."""
        if model in self.COST_ESTIMATES:
            # Assume 70% input, 30% output tokens
            input_tokens = tokens * 0.7
            output_tokens = tokens * 0.3
            
            cost_per_1k = self.COST_ESTIMATES[model]
            input_cost = (input_tokens / 1000) * cost_per_1k['input']
            output_cost = (output_tokens / 1000) * cost_per_1k['output']
            
            return input_cost + output_cost
        return 0.0
    
    def _display_results(self, results: List[ModelResponse]):
        """Display the results from model runs."""
        with self.output_area:
            clear_output()
            
            for result in results:
                print(f"\n{'='*60}")
                print(f"🤖 Model: {result.model}")
                print(f"⏱️ Response Time: {result.response_time:.2f}s")
                print(f"🎯 Tokens: {result.tokens_used}")
                print(f"💰 Cost: ${result.cost_estimate:.4f}")
                print(f"{'='*60}")
                print(f"\n{result.response}\n")
    
    def _compare_results(self, button):
        """Display a comparison of recent results."""
        if len(self.responses) < 2:
            with self.output_area:
                clear_output()
                print("⚠️ Need at least 2 responses to compare. Run some models first!")
            return
        
        # Get the most recent responses for comparison
        recent_responses = self.responses[-min(len(self.responses), 4):]
        
        with self.output_area:
            clear_output()
            print("📊 MODEL COMPARISON")
            print("=" * 80)
            
            # Summary table
            print(f"{'Model':<20} {'Tokens':<10} {'Time (s)':<10} {'Cost ($)':<10}")
            print("-" * 60)
            
            for response in recent_responses:
                print(f"{response.model:<20} {response.tokens_used:<10} "
                      f"{response.response_time:<10.2f} {response.cost_estimate:<10.4f}")
            
            print("\n" + "=" * 80)
            
            # Side-by-side responses
            for i, response in enumerate(recent_responses, 1):
                print(f"\n{i}. {response.model.upper()}")
                print("-" * 40)
                print(response.response[:200] + "..." if len(response.response) > 200 else response.response)
    
    def _clear_history(self, button):
        """Clear the response history."""
        self.responses.clear()
        self.total_cost = 0.0
        self._update_cost_display()
        
        with self.output_area:
            clear_output()
            print("🗑️ History cleared!")
    
    def _update_cost_display(self):
        """Update the cost display."""
        self.cost_display.value = f'<b>Total Cost: ${self.total_cost:.4f}</b>'
    
    def export_results(self, filename: str = None) -> str:
        """Export results to JSON file."""
        if not filename:
            filename = f"model_playground_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        export_data = {
            'total_cost': self.total_cost,
            'total_responses': len(self.responses),
            'responses': [asdict(response) for response in self.responses]
        }
        
        # Convert datetime objects to strings
        for response in export_data['responses']:
            response['timestamp'] = response['timestamp'].isoformat()
        
        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        return filename
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """Get usage statistics."""
        if not self.responses:
            return {'message': 'No responses recorded yet.'}
        
        model_stats = {}
        for response in self.responses:
            if response.model not in model_stats:
                model_stats[response.model] = {
                    'count': 0,
                    'total_tokens': 0,
                    'total_cost': 0.0,
                    'avg_response_time': 0.0
                }
            
            stats = model_stats[response.model]
            stats['count'] += 1
            stats['total_tokens'] += response.tokens_used
            stats['total_cost'] += response.cost_estimate
            stats['avg_response_time'] += response.response_time
        
        # Calculate averages
        for model, stats in model_stats.items():
            stats['avg_response_time'] /= stats['count']
            stats['avg_tokens_per_response'] = stats['total_tokens'] / stats['count']
        
        return {
            'total_responses': len(self.responses),
            'total_cost': self.total_cost,
            'model_stats': model_stats
        }


def create_playground() -> ModelPlayground:
    """Create and return a new model playground instance."""
    return ModelPlayground()