import os
from typing import List, Dict, Any, Optional
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
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
            }
        )
    
    def generate_response(self, 
                         messages: List[Dict[str, str]], 
                         temperature: float = 0.7,
                         max_tokens: Optional[int] = None,
                         top_p: Optional[float] = None) -> str:
        """
        Generate a response using the OpenRouter API.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            temperature: Controls randomness (0.0-1.0)
            max_tokens: Maximum number of tokens to generate
            top_p: Nucleus sampling parameter
            
        Returns:
            Generated text response
        """
        try:
            # Prepare the API call parameters
            params: Dict[str, Any] = {
                "model": self.model,
                "messages": messages,
                "temperature": temperature,
            }
            
            # Add optional parameters if specified
            if max_tokens is not None:
                params["max_tokens"] = max_tokens
            if top_p is not None:
                params["top_p"] = top_p
            
            # Make the API call
            response = self.client.chat.completions.create(**params)
            
            # Extract and return the generated text
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error in API call: {str(e)}")
            raise

    def generate_dialogue_turn(self,
                             persona_description: str,
                             conversation_history: List[Dict[str, str]],
                             system_prompt: str) -> str:
        """
        Generate a single turn of dialogue for a given persona.
        
        Args:
            persona_description: Description of the speaking persona
            conversation_history: List of previous messages
            system_prompt: System prompt to guide the generation
            
        Returns:
            Generated dialogue turn
        """
        # Format conversation history into role/content format expected by API
        formatted_history = []
        for msg in conversation_history:
            formatted_history.append({
                "role": "assistant" if msg.get("speaker") else "user",
                "content": f"{msg.get('speaker', 'Unknown')}: {msg.get('content', '')}"
            })

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Persona:\n{persona_description}\n\nConversation history:\n" + 
             "\n".join([f"{m.get('speaker', 'Unknown')}: {m.get('content', '')}" for m in conversation_history])}
        ]
        
        return self.generate_response(messages, temperature=0.7)