import os
import sys
import json
import random
from datetime import datetime
from pathlib import Path
from config.dialogue_contexts import DialogueScenario
from typing import Dict, List
from config.stereotype_categories import STEREOTYPE_CATEGORIES
from agents.dialogue_manager import DialogueManager

current_dir = os.getcwd()
print(f"Current working directory: {current_dir}")

print("\nFiles in current directory:")
for f in os.listdir(current_dir):
    print(f"- {f}")

config_dir = os.path.join(current_dir, "config")
print("\nFiles in config directory:")
if os.path.exists(config_dir):
    for f in os.listdir(config_dir):
        print(f"- {f}")
else:
    print("Config directory does not exist!")

project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

print(f"\nProject root: {project_root}")
print(f"Python path: {sys.path}")

try:
    from config.personas import EXAMPLE_PERSONAS
    from config.dialogue_contexts import DIALOGUE_SCENARIOS
    from config.stereotype_categories import STEREOTYPE_CATEGORIES
    from agents.dialogue_manager import DialogueManager

    def ensure_directory(path: str):
        Path(path).mkdir(parents=True, exist_ok=True)

    def generate_dialogue(scenario, category_name: str) -> Dict:
        """Generate a dialogue for a given scenario."""
        dialogue_manager = DialogueManager()
        
        for i, background in enumerate(scenario.persona_backgrounds):
            dialogue_manager.add_persona(f"persona{i+1}", background=background)
        
        dialogue_manager.start_dialogue(
            context=scenario.context,
            goal=scenario.goal
        )
        
        for i in range(len(scenario.persona_backgrounds)):
            dialogue_manager.generate_turn(f"persona{i+1}")
        
        return dialogue_manager.export_dialogue()

    def main():
        output_dir = "output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        for category_id, category in STEREOTYPE_CATEGORIES.items():
            print(f"\nProcessing category: {category.name}")
            
            for scenario in category.scenarios:
                print(f"Generating dialogue for scenario: {scenario.name}")
                
                dialogue = generate_dialogue(scenario, category.name)
                
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{output_dir}/{category_id}_{scenario.name.lower().replace(' ', '_')}_{timestamp}.json"
                
                with open(filename, 'w') as f:
                    json.dump(dialogue, f, indent=2)
                
                print(f"Saved dialogue to {filename}")

    if __name__ == "__main__":
        main()

except ImportError as e:
    print(f"\nImport Error: {e}")
    print("\nPlease verify that all required files exist:")
    required_files = [
        "config/__init__.py",
        "config/personas.py",
        "config/dialogue_contexts.py",
        "config/stereotype_categories.py",
        "agents/__init__.py",
        "agents/dialogue_manager.py",
        "agents/generation_agent.py",
        "agents/monitoring_agent.py",
        "prompts/__init__.py",
        "prompts/templates.py",
        "utils/__init__.py",
        "utils/api_wrapper.py"
    ]
    
    for file in required_files:
        path = os.path.join(project_root, file)
        exists = os.path.exists(path)
        print(f"- {file}: {'✓' if exists else '✗'}")
