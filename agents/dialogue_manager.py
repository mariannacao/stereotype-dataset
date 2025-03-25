from .generation_agent import GenerationAgent
from .monitoring_agent import MonitoringAgent

class DialogueManager:
    def __init__(self, personas, topic):
        self.personas = personas
        self.topic = topic
        self.generation_agent = GenerationAgent()
        self.monitoring_agent = MonitoringAgent()
        self.dialogue_history = []
        
    def generate_turn(self, speaker_id):
        persona = self.personas[speaker_id]
        context = self._format_dialogue_history()
        
        # Generate response
        response = self.generation_agent.generate_response(
            persona,
            context,
            self.topic
        )
        
        # Check consistency
        if self.monitoring_agent.check_consistency(persona, context + f"\n{persona['name']}: {response}"):
            self.dialogue_history.append({
                "speaker": persona['name'],
                "text": response
            })
            return response
        else:
            # If inconsistent, try one more time
            response = self.generation_agent.generate_response(
                persona,
                context,
                self.topic
            )
            self.dialogue_history.append({
                "speaker": persona['name'],
                "text": response
            })
            return response
    
    def _format_dialogue_history(self):
        return "\n".join([
            f"{turn['speaker']}: {turn['text']}"
            for turn in self.dialogue_history
        ]) 