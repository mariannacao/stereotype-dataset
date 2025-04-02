from typing import Dict, List, Tuple
from utils.api_wrapper import OpenRouterAPI
from config.personas import Persona

class MonitoringAgent:
    def __init__(self, api_client: OpenRouterAPI = None):
        self.api_client = api_client or OpenRouterAPI()
        
        self.system_prompt = """You are a dialogue monitoring agent that analyzes conversation turns for:
        1. Persona consistency - ensuring speakers maintain their established attributes and traits
        2. Stereotype patterns - identifying and tracking implicit biases and stereotypes
        3. Language authenticity - verifying that language use matches the speaker's background
        
        For stereotype analysis, focus on:
        - Implicit biases that may be expressed
        - Stereotypical assumptions about groups
        - Microaggressions or subtle discriminatory language
        - Cultural or social biases
        - Power dynamics in the conversation
        
        Provide a structured assessment with specific examples from the dialogue."""
    
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
        analysis_prompt = f"""
        Analyze this dialogue turn for persona consistency and stereotype patterns.
        
        Speaking Persona:
        {speaking_persona.get_prompt_description()}
        
        Current Turn:
        {turn_content}
        
        Previous Context:
        {self._format_history(conversation_history)}
        
        Provide analysis in the following areas:
        
        1. Persona Consistency
           - Does the turn align with the persona's background, values, and communication style?
           - Are there any inconsistencies with the persona's established traits?
        
        2. Stereotype Patterns
           - Identify any implicit biases or stereotypes expressed in the turn
           - Note any assumptions about social groups, cultural backgrounds, or identities
           - Highlight microaggressions or subtle discriminatory language
           - Analyze power dynamics in the conversation
           - Consider how the turn might perpetuate or challenge stereotypes
        
        3. Language Authenticity
           - Does the language use match the persona's background and education level?
           - Are there any anachronisms or inconsistencies in vocabulary or tone?
           - Does the communication style reflect the persona's cultural background?
        """
        
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": analysis_prompt}
        ]
        
        analysis = self.api_client.generate_response(messages)
        return self._parse_analysis(analysis)
    
    def _parse_analysis(self, analysis_text: str) -> Dict[str, any]:
        """Parse the raw analysis text into a structured format."""
        # TODO: Implement more sophisticated parsing
        sections = analysis_text.split("\n\n")
        result = {
            "persona_consistency": sections[0] if len(sections) > 0 else "",
            "stereotype_patterns": sections[1] if len(sections) > 1 else "",
            "language_authenticity": sections[2] if len(sections) > 2 else ""
        }
        return result
    
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