from utils.api_wrapper import LLMClient

class GenerationAgent:
    def __init__(self):
        self.llm = LLMClient()
    
    def generate_response(self, persona, context, topic):
        from prompts.templates import build_generation_prompt
        
        prompt = build_generation_prompt(persona, context, topic)
        messages = [{"role": "user", "content": prompt}]
        
        response = self.llm.generate_response(messages)
        return response 