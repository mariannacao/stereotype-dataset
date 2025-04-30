import os
import sys
import json
import random
from datetime import datetime
from pathlib import Path
from config.dialogue_contexts import DialogueScenario
from typing import List, Dict
from dotenv import load_dotenv
from agents.dialogue_manager import DialogueManager
from utils.api_wrapper import OpenRouterAPI
from utils.database import DialogueDatabase

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
        manager = DialogueManager(db)
        
        for persona_id, persona in persona_pairs:
            manager.add_persona(persona_id, persona)
        
        manager.start_dialogue(
            context=scenario.context,
            goal=scenario.goal,
            scenario_id=scenario_id
        )
        
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
        
        # Finalize the dialogue and store the overall analysis
        manager.finalize_dialogue()
        
        print("\nDialogue saved to database")
        print("\n" + "="*80)

    def main():
        # Initialize database
        db = DialogueDatabase()
        
        # Load environment variables
        load_dotenv()
        
        # Initialize API
        api = OpenRouterAPI()
        
        # Process each stereotype category
        for category_id, category in STEREOTYPE_CATEGORIES.items():
            print(f"\nProcessing category: {category.name}")
            
            # Insert stereotype category
            category_id = db.insert_stereotype_category(category.name, category.description)
            
            for scenario in category.scenarios:
                # Insert scenario
                scenario_id = db.insert_scenario(
                    category_id=category_id,
                    name=scenario.name,
                    context=scenario.context,
                    goal=scenario.goal
                )
                
                # Use the personas specified in the scenario
                persona_pairs = []
                for persona_id in scenario.persona_ids:
                    if persona_id in EXAMPLE_PERSONAS:
                        persona = EXAMPLE_PERSONAS[persona_id]
                        # Insert persona if not exists
                        existing_persona = db.get_persona_by_name(persona.name)
                        if not existing_persona:
                            persona_id = db.insert_persona(
                                name=persona.name,
                                background=persona.background,
                                personality_traits=persona.personality_traits
                            )
                        else:
                            persona_id = existing_persona["id"]
                        persona_pairs.append((persona_id, persona))
                    else:
                        print(f"Warning: Persona ID '{persona_id}' not found in EXAMPLE_PERSONAS")
                
                # If no valid personas were found, use a default pair
                if not persona_pairs:
                    print("Warning: No valid personas found for scenario. Using default personas.")
                    default_personas = [
                        ("urban_prof", EXAMPLE_PERSONAS["urban_professional"]),
                        ("rural_trade", EXAMPLE_PERSONAS["rural_tradesperson"])
                    ]
                    for persona_id, persona in default_personas:
                        existing_persona = db.get_persona_by_name(persona.name)
                        if not existing_persona:
                            persona_id = db.insert_persona(
                                name=persona.name,
                                background=persona.background,
                                personality_traits=persona.personality_traits
                            )
                        else:
                            persona_id = existing_persona["id"]
                        persona_pairs.append((persona_id, persona))
                
                # Generate dialogue
                dialogue = generate_dialogue(scenario, persona_pairs)
                
                # Insert dialogue
                dialogue_id = db.insert_dialogue(scenario_id)
                
                # Insert dialogue turns and analysis
                for turn_num, turn in enumerate(dialogue["conversation"]):
                    # Insert dialogue turn
                    turn_id = db.insert_dialogue_turn(
                        dialogue_id=dialogue_id,
                        turn_number=turn_num,
                        speaker_id=turn["persona_id"],
                        content=turn["content"]
                    )
                    
                    # Insert turn analysis
                    for aspect, content in turn["analysis"].items():
                        db.insert_analysis(
                            dialogue_id=dialogue_id,
                            turn_id=turn_id,
                            aspect=aspect,
                            content=content
                        )
                
                # Insert overall analysis
                for aspect, content in dialogue["analysis"].items():
                    db.insert_analysis(
                        dialogue_id=dialogue_id,
                        turn_id=None,  # Overall analysis
                        aspect=aspect,
                        content=content
                    )
        
        # Close database connection
        db.close()
        
        print("\nAll dialogues saved to database")

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
