from typing import Dict, List, Optional
from config.personas import Persona
from agents.generation_agent import GenerationAgent
from agents.monitoring_agent import MonitoringAgent

class DialogueManager:
    def __init__(self):
        self.generation_agent = GenerationAgent()
        self.monitoring_agent = MonitoringAgent()
        self.conversation_history: List[Dict[str, str]] = []
        self.active_personas: Dict[str, Persona] = {}
        
    def add_persona(self, persona_id: str, persona: Persona):
        """Add a persona to the dialogue."""
        self.active_personas[persona_id] = persona
    
    def start_dialogue(self, 
                      context: str = "",
                      goal: str = "") -> None:
        """Start a new dialogue session."""
        self.conversation_history = []
        self._context = context
        self._goal = goal
    
    def generate_turn(self, speaking_persona_id: str) -> Dict[str, any]:
        """
        Generate and validate the next dialogue turn.
        
        Args:
            speaking_persona_id: ID of the persona whose turn it is
            
        Returns:
            Dictionary containing the turn results and analysis
        """
        if speaking_persona_id not in self.active_personas:
            raise ValueError(f"Unknown persona ID: {speaking_persona_id}")
        
        speaking_persona = self.active_personas[speaking_persona_id]
        
        # Generate the turn
        turn_content = self.generation_agent.generate_turn(
            speaking_persona=speaking_persona,
            conversation_history=self.conversation_history,
            dialogue_context=self._context,
            dialogue_goal=self._goal
        )
        
        # Validate the turn
        is_valid, validation_reason = self.monitoring_agent.check_turn_validity(
            turn_content=turn_content,
            speaking_persona=speaking_persona
        )
        
        if not is_valid:
            # If invalid, try one more time
            turn_content = self.generation_agent.generate_turn(
                speaking_persona=speaking_persona,
                conversation_history=self.conversation_history,
                dialogue_context=f"{self._context}\nNote: Previous attempt was invalid because: {validation_reason}",
                dialogue_goal=self._goal
            )
        
        # Analyze the turn
        analysis = self.monitoring_agent.analyze_turn(
            turn_content=turn_content,
            speaking_persona=speaking_persona,
            conversation_history=self.conversation_history
        )
        
        # Add to conversation history
        self.conversation_history.append({
            "speaker": speaking_persona.name,
            "content": turn_content,
            "persona_id": speaking_persona_id
        })
        
        return {
            "content": turn_content,
            "speaker": speaking_persona.name,
            "is_valid": is_valid,
            "validation_reason": validation_reason,
            "analysis": analysis
        }
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """Get the current conversation history."""
        return self.conversation_history
    
    def export_dialogue(self) -> Dict[str, any]:
        """Export the complete dialogue with metadata."""
        return {
            "context": self._context,
            "goal": self._goal,
            "personas": {
                pid: persona.to_dict() 
                for pid, persona in self.active_personas.items()
            },
            "conversation": self.conversation_history
        } 