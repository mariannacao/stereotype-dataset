from utils.api_wrapper import LLMClient
from prompts.prompt_templates import build_prompt

class DialogueAgent:
    def __init__(self, persona):
        self.persona = persona
        self.llm_client = LLMClient()
    
    def generate_reply(self, context):
        prompt = build_prompt(self.persona, context)
        return self.llm_client.call_llm(prompt)
