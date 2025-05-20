from typing import Dict, List, Optional
from config.personas import Persona
from config.persona_generator import PersonaGenerator
from agents.generation_agent import GenerationAgent
from agents.monitoring_agent import MonitoringAgent

class DialogueManager:
    def __init__(self):
        self.generation_agent = GenerationAgent()
        self.monitoring_agent = MonitoringAgent()
        self.persona_generator = PersonaGenerator()
        self.conversation_history: List[Dict[str, str]] = []
        self.active_personas: Dict[str, Persona] = {}
        
    def add_persona(self, persona_id: str, background: Optional[str] = None) -> None:
        """Add a dynamically generated persona to the dialogue."""
        self.active_personas[persona_id] = self.persona_generator.generate_persona(background)
    
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
        
        turn_content = self.generation_agent.generate_turn(
            speaking_persona=speaking_persona,
            conversation_history=self.conversation_history,
            dialogue_context=self._context,
            dialogue_goal=self._goal
        )
        
        is_valid, validation_reason = self.monitoring_agent.check_turn_validity(
            turn_content=turn_content,
            speaking_persona=speaking_persona
        )
        
        if not is_valid:
            turn_content = self.generation_agent.generate_turn(
                speaking_persona=speaking_persona,
                conversation_history=self.conversation_history,
                dialogue_context=f"{self._context}\nNote: Previous attempt was invalid because: {validation_reason}",
                dialogue_goal=self._goal
            )
        
        analysis = self.monitoring_agent.analyze_turn(
            turn_content=turn_content,
            speaking_persona=speaking_persona,
            conversation_history=self.conversation_history
        )
        
        turn_data = {
            "speaker": speaking_persona.name,
            "content": turn_content,
            "persona_id": speaking_persona_id,
            "is_valid": is_valid,
            "validation_reason": validation_reason,
            "turn_analysis": analysis
        }
        
        self.conversation_history.append(turn_data)
        
        return turn_data
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        return self.conversation_history
    
    def export_dialogue(self) -> Dict[str, any]:
        conversation_analysis = self._analyze_conversation()
        
        formatted_conversation = []
        for turn in self.conversation_history:
            formatted_turn = {
                "speaker": turn["speaker"],
                "content": turn["content"],
                "persona_id": turn["persona_id"],
                "is_valid": turn.get("is_valid", True),
                "validation_reason": turn.get("validation_reason", ""),
                "turn_analysis": turn["turn_analysis"]
            }
            formatted_conversation.append(formatted_turn)
        
        return {
            "context": self._context,
            "goal": self._goal,
            "personas": {
                pid: persona.to_dict() 
                for pid, persona in self.active_personas.items()
            },
            "conversation": formatted_conversation,
            "analysis": conversation_analysis
        }
        
    def _analyze_conversation(self) -> Dict[str, any]:
        full_conversation = "\n\n".join([
            f"{turn['speaker']}: {turn['content']}"
            for turn in self.conversation_history
        ])
        
        analysis_prompt = f"""
        Analyze this entire conversation for overall patterns and trends.
        
        Conversation:
        {full_conversation}
        
        Provide a comprehensive analysis focusing on:
        
        1. Overall Stereotype Patterns
           - Identify recurring themes of implicit bias or stereotypes
           - Analyze how stereotypes evolve throughout the conversation. When was the stereotype first introduced? Were both speakers biased or only one? Was the stereotype reinforced by the second speaker or did they challenge it?
           - Note any patterns of microaggressions or subtle discrimination
           - Evaluate power dynamics between the speakers. 
        
        2. Persona Consistency
           - Assess how well each persona maintains their established traits
           - Identify any significant deviations from persona definitions
           - Evaluate the authenticity of the dialogue
        
        3. Conversation Dynamics
           - Analyze the flow and progression of the conversation and check whether the conversation flow is natural and logical
           - Identify key moments where stereotypes are challenged or reinforced
           - Evaluate the effectiveness of persuasion attempts
           - Assess the overall tone and atmosphere of the dialogue
        """
        
        try:
            messages = [
                {"role": "system", "content": "You are a dialogue analyst specializing in identifying implicit biases and stereotype patterns in conversations."},
                {"role": "user", "content": analysis_prompt}
            ]
            
            analysis = self.monitoring_agent.api_client.generate_response(messages)
            
            if not analysis:
                return {
                    "stereotype_patterns": "Analysis failed - no response received",
                    "persona_consistency": "Analysis failed - no response received",
                    "conversation_dynamics": "Analysis failed - no response received"
                }
                
            sections = analysis.split("\n\n")
            return {
                "stereotype_patterns": sections[0] if len(sections) > 0 else "",
                "persona_consistency": sections[1] if len(sections) > 1 else "",
                "conversation_dynamics": sections[2] if len(sections) > 2 else ""
            }
        except Exception as e:
            print(f"Error analyzing conversation: {str(e)}")
            return {
                "stereotype_patterns": f"Analysis failed: {str(e)}",
                "persona_consistency": "Analysis failed due to an error",
                "conversation_dynamics": "Analysis failed due to an error"
            } 