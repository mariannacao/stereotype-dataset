from typing import List, Dict, Optional
from utils.api_wrapper import OpenRouterAPI
from config.personas import Persona

class GenerationAgent:
    def __init__(self, api_client: Optional[OpenRouterAPI] = None):
        self.api_client = api_client or OpenRouterAPI()
        
        self.base_system_prompt = """You are a dialogue generation agent that creates realistic, context-aware 
        conversation turns. You should:
        1. Stay consistent with the given persona's attributes, background, and personality traits
        2. Incorporate subtle, contextually appropriate stereotypes and biases that might emerge naturally
        3. Use appropriate language patterns, vocabulary, and expressions based on the persona's background
        4. Maintain a natural flow of conversation while advancing the dialogue purpose
        
        Generate ONLY the next dialogue turn, without any additional explanations or metadata."""
    
    def generate_turn(self, 
                     speaking_persona: Persona,
                     conversation_history: List[Dict[str, str]],
                     dialogue_context: str = "",
                     dialogue_goal: str = "") -> str:
        """
        Generate the next turn in the dialogue.
        
        Args:
            speaking_persona: The persona who is speaking in this turn
            conversation_history: Previous messages in the conversation
            dialogue_context: Additional context about the conversation setting
            dialogue_goal: The goal or purpose of the conversation
            
        Returns:
            Generated dialogue turn
        """
        # rip
        return ""
    
    def format_conversation_history(self, history: List[Dict[str, str]]) -> str:
        """Format conversation history for display or logging."""
        formatted = []
        for msg in history:
            speaker = msg.get("speaker", "Unknown")
            content = msg.get("content", "")
            formatted.append(f"{speaker}: {content}")
        return "\n".join(formatted) 