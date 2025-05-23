import os
import time
from typing import List, Dict, Any, Optional
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class OpenRouterAPI:
    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.referer = os.getenv("OPENROUTER_REFERER", "http://localhost:3000")
        self.title = os.getenv("OPENROUTER_TITLE", "PersuasionDialogue")
        self.model = os.getenv("OPENROUTER_MODEL", "deepseek/deepseek-chat-v3-0324:free")
        
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY not found in environment variables")
            
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.api_key,
            default_headers={
                "HTTP-Referer": self.referer,
                "X-Title": self.title
            },
            timeout=30.0
        )
        
        self.max_retries = 10
        self.retry_delay = 5
        self.max_tokens = 40000
        self.max_input_tokens = 80000
     
    def generate_response(self, 
                         messages: List[Dict[str, str]], 
                         temperature: float = 0.7,
                         max_tokens: Optional[int] = None,
                         top_p: Optional[float] = None) -> Optional[str]:
        """
        Generate a response using the OpenRouter API with retry logic.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            temperature: Controls randomness (0.0-1.0)
            max_tokens: Maximum number of tokens to generate
            top_p: Nucleus sampling parameter
            
        Returns:
            Generated text response or None if all retries fail
        """
        retries = 0
        last_error = None
        current_delay = self.retry_delay
        
        while retries < self.max_retries:
            try:
                params: Dict[str, Any] = {
                    "model": self.model,
                    "messages": messages,
                    "temperature": temperature,
                    "max_tokens": max_tokens or self.max_tokens,
                }
                
                if top_p is not None:
                    params["top_p"] = top_p
                
                response = self.client.chat.completions.create(**params)
                
                if response and response.choices and len(response.choices) > 0:
                    content = response.choices[0].message.content
                    if content and content.strip():
                        return content
                    else:
                        print(f"Warning: Empty content in response (attempt {retries + 1}/{self.max_retries})")
                else:
                    print(f"Warning: Empty response from API (attempt {retries + 1}/{self.max_retries})")
                
                retries += 1
                if retries < self.max_retries:
                    print(f"Retrying in {current_delay} seconds...")
                    time.sleep(current_delay)
                    current_delay *= 2  
                    
            except Exception as e:
                last_error = str(e)
                print(f"Error in API call (attempt {retries + 1}/{self.max_retries}): {last_error}")
                retries += 1
                
                if retries < self.max_retries:
                    print(f"Retrying in {current_delay} seconds...")
                    time.sleep(current_delay)
                    current_delay *= 2 
        
        print(f"All {self.max_retries} attempts failed. Last error: {last_error}")
        return None