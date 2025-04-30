from typing import List, Dict, Optional, Any
from utils.api_wrapper import OpenRouterAPI
from config.personas import Persona

class GenerationAgent:
    def __init__(self, api_client: Optional[OpenRouterAPI] = None):
        self.api_client = api_client or OpenRouterAPI()
        
        self.system_prompt = """Generate natural dialogue that reflects the persona's characteristics and background. 
        Keep responses focused and relevant to the conversation topic."""
    
    def generate_turn(self,
                     speaking_persona: Persona,
                     conversation_history: List[Dict[str, str]],
                     context: str,
                     goal: str) -> str:
        """
        Generate a single turn of dialogue for a given persona.
        
        Args:
            speaking_persona: The speaking persona's information
            conversation_history: Previous turns in the conversation
            context: The conversation context
            goal: The conversation goal
            
        Returns:
            Generated dialogue turn
        """
        # Format conversation history (keep only last 3 turns to save tokens)
        recent_history = conversation_history[-3:] if len(conversation_history) > 3 else conversation_history
        history_text = "\n".join([f"{turn['speaker']}: {turn['content']}" for turn in recent_history])
        
        # Prepare the generation prompt
        prompt = f"""Context: {context}
Goal: {goal}

Persona: {speaking_persona.name}
Background: {speaking_persona.background}
Key Traits: {', '.join(speaking_persona.personality_traits[:3])}

Recent Conversation:
{history_text}

Generate a natural response that:
1. Aligns with the persona's characteristics
2. Advances the conversation
3. Shows engagement with the topic
4. Maintains a natural flow

Response:"""
        
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": prompt}
        ]
        
        try:
            response = self.api_client.generate_response(
                messages,
                temperature=0.7,
                max_tokens=150  # Limit response length
            )
            return response if response else "[Error: Unable to generate response]"
        except Exception as e:
            print(f"Error generating turn: {str(e)}")
            return "[Error: Generation failed]"
    
    def format_conversation_history(self, history: List[Dict[str, str]]) -> str:
        """Format conversation history for display or logging."""
        formatted = []
        for msg in history:
            speaker = msg.get("speaker", "Unknown")
            content = msg.get("content", "")
            formatted.append(f"{speaker}: {content}")
        return "\n".join(formatted) 