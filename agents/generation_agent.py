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
        system_prompt = self.base_system_prompt
        
        if dialogue_context:
            system_prompt += f"\n\nContext: {dialogue_context}"
        if dialogue_goal:
            system_prompt += f"\n\nConversation goal: {dialogue_goal}"
        
        if not conversation_history:
            system_prompt += """\n\nThis is the FIRST turn of the conversation. You should:
            1. Start the discussion naturally, addressing the context and goal
            2. Speak in a way that establishes your persona's perspective
            3. Open the conversation in a way that invites response
            4. Make a substantive contribution that sets the tone for the dialogue
            
            Do NOT just say hello or give a minimal response. Make a meaningful opening statement."""
            
        persona_desc = speaking_persona.get_prompt_description()
        
        user_prompt = f"Persona:\n{persona_desc}\n\n"
        if conversation_history:
            user_prompt += f"Conversation history:\n" + "\n".join([
                f"{m.get('speaker', 'Unknown')}: {m.get('content', '')}" 
                for m in conversation_history
            ])
        else:
            user_prompt += f"You are starting the conversation in this context. Make a meaningful opening statement that reflects your persona and engages with the topic."
        
        response = self.api_client.generate_dialogue_turn(
            persona_description=persona_desc,
            conversation_history=conversation_history,
            system_prompt=system_prompt
        )
        
        if not response or not response.strip():
            system_prompt += "\n\nIMPORTANT: You MUST generate a substantive response. Empty or minimal responses are not acceptable."
            response = self.api_client.generate_dialogue_turn(
                persona_description=persona_desc,
                conversation_history=conversation_history,
                system_prompt=system_prompt
            )
        
        return response.strip()
    
    def format_conversation_history(self, history: List[Dict[str, str]]) -> str:
        """Format conversation history for display or logging."""
        formatted = []
        for msg in history:
            speaker = msg.get("speaker", "Unknown")
            content = msg.get("content", "")
            formatted.append(f"{speaker}: {content}")
        return "\n".join(formatted) 