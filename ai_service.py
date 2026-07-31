import time
import json
import requests
from typing import List, Dict, Any
from config import config
from prompts import PromptTemplates

class AIContentService:
    """AI service for content generation"""
    
    def __init__(self):
        self.api_key = config.OPENAI_API_KEY
        self.model = config.AI_MODEL
        self.timeout = config.API_TIMEOUT
        self.base_url = "https://api.openai.com/v1/chat/completions"
        
    def _call_api(self, prompt: str) -> str:
        """Call the AI API with the given prompt"""
        if not self.api_key:
            return "⚠️ ကျေးဇူးပြု၍ API Key ကို ထည့်သွင်းပါ။ (Please enter your API Key)"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are a helpful content creation assistant for Myanmar content creators."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.8,
            "max_tokens": 1000,
            "stream": False
        }
        
        try:
            response = requests.post(
                self.base_url,
                headers=headers,
                json=data,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                return f"❌ API Error: {response.status_code} - {response.text}"
                
        except requests.exceptions.Timeout:
            return "⏰ Request timeout. Please try again."
        except Exception as e:
            return f"❌ Error: {str(e)}"
    
    def generate_ideas(self, topic: str, platform: str, audience: str, 
                       style: str, language: str) -> str:
        """Generate content ideas"""
        prompt = PromptTemplates.get_ideas_prompt(topic, platform, audience, style, language)
        return self._call_api(prompt)
    
    def generate_hooks(self, topic: str, platform: str, style: str, 
                       language: str) -> str:
        """Generate attention-grabbing hooks"""
        prompt = PromptTemplates.get_hooks_prompt(topic, platform, style, language)
        return self._call_api(prompt)
    
    def generate_script(self, topic: str, platform: str, audience: str,
                       style: str, language: str) -> str:
        """Generate video script"""
        prompt = PromptTemplates.get_script_prompt(topic, platform, audience, style, language)
        return self._call_api(prompt)
    
    def generate_captions(self, topic: str, platform: str, style: str,
                         language: str) -> str:
        """Generate captions"""
        prompt = PromptTemplates.get_captions_prompt(topic, platform, style, language)
        return self._call_api(prompt)
    
    def generate_hashtags(self, topic: str, platform: str, language: str) -> str:
        """Generate hashtags"""
        prompt = PromptTemplates.get_hashtags_prompt(topic, platform, language)
        return self._call_api(prompt)

ai_service = AIContentService()
