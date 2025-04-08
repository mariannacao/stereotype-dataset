import os
import sys
import json
import random
from datetime import datetime
from pathlib import Path
from config.dialogue_contexts import DialogueScenario

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
        """Create directory if it doesn't exist."""
        Path(path).mkdir(parents=True, exist_ok=True)

    def generate_dialogue(scenario: DialogueScenario, persona_pairs: list, num_turns: int = 12):
        """
        Generate a dialogue for a specific scenario and persona pair.
        
        Args:
            scenario: The scenario object to use
            persona_pairs: List of tuples of persona IDs to use
            num_turns: Number of turns to generate
        """
        manager = DialogueManager()
        
        for persona_id, persona in persona_pairs:
            manager.add_persona(persona_id, persona)
        
        manager.start_dialogue(context=scenario.context, goal=scenario.goal)
        
        print(f"\nScenario: {scenario.name}")
        print("\nContext:", scenario.context)
        print("\nGoal:", scenario.goal)
        print("\nSuggested Topics:")
        for topic in scenario.suggested_topics:
            print(f"- {topic}")
        print("\nStarting dialogue...\n")
        
        for turn in range(num_turns):
            current_pair = persona_pairs[turn % len(persona_pairs)]
            persona_id = current_pair[0]
            
            print(f"\nGenerating turn {turn + 1} for {persona_id}...")
            result = manager.generate_turn(persona_id)
            
            print(f"\n{result['speaker']}: {result['content']}")
            print("\nTurn Analysis:")
            print("- Persona Consistency:", result['analysis']['persona_consistency'])
            print("- Stereotype Patterns:", result['analysis']['stereotype_patterns'])
            print("- Language Authenticity:", result['analysis']['language_authenticity'])
            print("\n" + "-"*80)
        
        output = manager.export_dialogue()
        
        output["scenario"] = scenario.to_dict()
        
        print("\nOverall Conversation Analysis:")
        print("\nStereotype Patterns:")
        print(output["analysis"]["stereotype_patterns"])
        print("\nPersona Consistency:")
        print(output["analysis"]["persona_consistency"])
        print("\nConversation Dynamics:")
        print(output["analysis"]["conversation_dynamics"])
        print("\n" + "="*80)
        
        return output

    def main():
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_output_dir = f"dialogue_outputs_{timestamp}"
        ensure_directory(base_output_dir)
        
        all_dialogues = {
            "metadata": {
                "timestamp": timestamp,
                "total_categories": len(STEREOTYPE_CATEGORIES),
                "categories": []
            }
        }
        
        for category_id, category in STEREOTYPE_CATEGORIES.items():
            print(f"\nProcessing category: {category.name}")
            
            category_dir = os.path.join(base_output_dir, category_id)
            ensure_directory(category_dir)
            
            category_dialogues = []
            
            for scenario in category.scenarios:
                # Use the personas specified in the scenario
                persona_pairs = []
                for persona_id in scenario.persona_ids:
                    if persona_id in EXAMPLE_PERSONAS:
                        persona_pairs.append((persona_id, EXAMPLE_PERSONAS[persona_id]))
                    else:
                        print(f"Warning: Persona ID '{persona_id}' not found in EXAMPLE_PERSONAS")
                
                # If no valid personas were found, use a default pair
                if not persona_pairs:
                    print("Warning: No valid personas found for scenario. Using default personas.")
                    persona_pairs = [
                        ("urban_prof", EXAMPLE_PERSONAS["urban_professional"]),
                        ("rural_trade", EXAMPLE_PERSONAS["rural_tradesperson"])
                    ]
                
                dialogue = generate_dialogue(scenario, persona_pairs)
                category_dialogues.append(dialogue)
                
                dialogue_filename = f"{scenario.name.lower().replace(' ', '_')}.json"
                dialogue_path = os.path.join(category_dir, dialogue_filename)
                with open(dialogue_path, "w") as f:
                    json.dump(dialogue, f, indent=2)
            
            category_metadata = {
                "name": category.name,
                "description": category.description,
                "num_scenarios": len(category.scenarios),
                "dialogues": category_dialogues
            }
            
            category_meta_path = os.path.join(category_dir, "_category_info.json")
            with open(category_meta_path, "w") as f:
                json.dump(category_metadata, f, indent=2)
            
            all_dialogues["metadata"]["categories"].append({
                "id": category_id,
                "name": category.name,
                "num_dialogues": len(category_dialogues)
            })
        
        meta_path = os.path.join(base_output_dir, "_dataset_info.json")
        with open(meta_path, "w") as f:
            json.dump(all_dialogues, f, indent=2)
        
        print(f"\nAll dialogues saved to {base_output_dir}/")
        print("Directory structure:")
        print(f"- {base_output_dir}/")
        for category_id in STEREOTYPE_CATEGORIES.keys():
            print(f"  - {category_id}/")
            print(f"    - _category_info.json")
            print(f"    - [dialogue files...]")
        print(f"  - _dataset_info.json")

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
