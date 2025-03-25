from utils.api_wrapper import LLMClient

class MonitoringAgent:
    def __init__(self):
        self.llm = LLMClient()
    
    def check_consistency(self, persona, dialogue_history):
        from prompts.templates import build_monitoring_prompt
        
        prompt = build_monitoring_prompt(persona, dialogue_history)
        messages = [{"role": "user", "content": prompt}]
        
        response = self.llm.generate_response(messages)
        return response == "CONSISTENT" 