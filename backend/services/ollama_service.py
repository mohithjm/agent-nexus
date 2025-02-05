import requests
from typing import List, Dict

class OllamaService:
    @staticmethod
    def list_models() -> List[Dict[str, str]]:
        """
        Fetch available Ollama models
        
        Returns:
            List of available models with their details
        """
        try:
            response = requests.get("http://localhost:11434/api/tags")
            response.raise_for_status()
            models = response.json().get('models', [])
            return [
                {
                    "name": model['name'],
                    "size": model['size'],
                    "modified_at": model['modified_at']
                } for model in models
            ]
        except requests.RequestException as e:
            print(f"Error fetching Ollama models: {e}")
            return []

    @staticmethod
    def generate_response(model: str, prompt: str, system_prompt: str = "") -> str:
        """
        Generate a response using a specific Ollama model
        
        Args:
            model (str): Name of the Ollama model
            prompt (str): User prompt
            system_prompt (str, optional): System-level instructions
        
        Returns:
            Generated response from the model
        """
        payload = {
            "model": model,
            "prompt": prompt,
            "system": system_prompt,
            "stream": False
        }
        
        try:
            response = requests.post("http://localhost:11434/api/generate", json=payload)
            response.raise_for_status()
            return response.json().get('response', '')
        except requests.RequestException as e:
            print(f"Error generating response: {e}")
            return ""