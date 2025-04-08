from typing import Dict, List, Tuple
from utils.api_wrapper import OpenRouterAPI
from config.personas import Persona

class MonitoringAgent:
    def __init__(self, api_client: OpenRouterAPI = None):
        self.api_client = api_client or OpenRouterAPI()
        
        self.analysis_prompts = {
            "persona_consistency": """Analyze if the response aligns with the persona's characteristics. Focus on key traits and background.""",
            "stereotype_patterns": """Identify any implicit stereotypes in the response. Look for assumptions about groups or individuals.""",
            "language_authenticity": """Check if the language matches the persona's background and communication style."""
        }
        
        self.analysis_system_prompt = """You are an expert at analyzing dialogue for persona consistency and stereotype patterns. 
        Provide concise, focused analysis in 1-2 sentences per aspect."""
    
    def analyze_turn(self, 
                    turn_content: str,
                    speaking_persona: Persona,
                    conversation_history: List[Dict[str, str]]) -> Dict[str, any]:
        """
        Analyze a single dialogue turn for consistency and stereotype patterns.
        
        Args:
            turn_content: The content of the current dialogue turn
            speaking_persona: The persona who spoke this turn
            conversation_history: Previous messages in the conversation
            
        Returns:
            Dictionary containing analysis results
        """
        analysis = {}
        
        # Prepare the analysis context
        context = f"Persona: {speaking_persona.name}\nBackground: {speaking_persona.background}\nTraits: {', '.join(speaking_persona.personality_traits)}\n\n"
        context += f"Current Turn: {turn_content}\n\n"
        
        # Analyze each aspect
        for aspect, prompt in self.analysis_prompts.items():
            messages = [
                {"role": "system", "content": self.analysis_system_prompt},
                {"role": "user", "content": context + prompt}
            ]
            
            try:
                response = self.api_client.generate_response(messages, temperature=0.3)
                analysis[aspect] = response if response else "Analysis failed"
            except Exception as e:
                print(f"Error in {aspect} analysis: {str(e)}")
                analysis[aspect] = "Analysis error"
        
        return analysis
    
    def analyze_conversation(self, 
                           dialogue: List[Dict[str, str]], 
                           personas: Dict[str, Persona]) -> Dict[str, str]:
        """
        Analyze the complete conversation for overall patterns and dynamics.
        
        Args:
            dialogue: Complete conversation
            personas: Dictionary of participating personas
            
        Returns:
            Dictionary containing overall analysis
        """
        # Prepare conversation context
        context = "Complete Conversation:\n"
        for turn in dialogue:
            context += f"{turn['speaker']}: {turn['content']}\n"
        
        # Analyze overall patterns
        analysis_prompts = {
            "stereotype_patterns": "Identify recurring stereotype patterns in the conversation.",
            "persona_consistency": "Evaluate overall consistency of personas throughout the dialogue.",
            "conversation_dynamics": "Analyze how the conversation evolved and the interaction between personas."
        }
        
        overall_analysis = {}
        for aspect, prompt in analysis_prompts.items():
            messages = [
                {"role": "system", "content": self.analysis_system_prompt},
                {"role": "user", "content": context + "\n" + prompt}
            ]
            
            try:
                response = self.api_client.generate_response(messages, temperature=0.3)
                overall_analysis[aspect] = response if response else "Analysis failed"
            except Exception as e:
                print(f"Error in {aspect} analysis: {str(e)}")
                overall_analysis[aspect] = "Analysis error"
        
        return overall_analysis
    
    def _format_history(self, history: List[Dict[str, str]]) -> str:
        """Format conversation history for analysis."""
        return "\n".join([
            f"{msg.get('speaker', 'Unknown')}: {msg.get('content', '')}"
            for msg in history
        ])
    
    def check_turn_validity(self, 
                          turn_content: str,
                          speaking_persona: Persona) -> Tuple[bool, str]:
        """
        Quick check if a dialogue turn is valid for the given persona.
        
        Args:
            turn_content: The content to validate
            speaking_persona: The persona who generated the content
            
        Returns:
            Tuple of (is_valid, reason)
        """
        validation_prompt = f"""
        Quickly validate if this dialogue turn is appropriate for the given persona.
        
        Persona:
        {speaking_persona.get_prompt_description()}
        
        Turn Content:
        {turn_content}
        
        You MUST respond in exactly this format:
        VALID: <reason why the turn is valid>
        or
        INVALID: <reason why the turn is invalid>
        
        Your response must start with either VALID: or INVALID: followed by your explanation.
        """
        
        messages = [
            {"role": "system", "content": "You are a dialogue validator. You MUST respond with either 'VALID:' or 'INVALID:' followed by a reason."},
            {"role": "user", "content": validation_prompt}
        ]
        
        response = self.api_client.generate_response(messages)
        
        # Handle empty responses
        if not response or not response.strip():
            return False, "Empty response from validator"
            
        response = response.strip()
        
        # Check for valid/invalid prefix
        is_valid = response.upper().startswith("VALID:")
        
        # Extract reason safely
        try:
            if ":" in response:
                reason = response.split(":", 1)[1].strip()
            else:
                # If no colon found, use the whole response as the reason
                reason = response.strip()
                
            # If reason is empty, provide a default
            if not reason:
                reason = "No specific reason provided"
                
        except Exception as e:
            # Fallback for any parsing errors
            reason = "Error parsing validation response"
            is_valid = False
        
        return is_valid, reason 