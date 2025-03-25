import os
import sys
import json
import random

# Add debugging information
current_dir = os.getcwd()
print(f"Current working directory: {current_dir}")

# List all files in current directory
print("\nFiles in current directory:")
for f in os.listdir(current_dir):
    print(f"- {f}")

# List all files in config directory
config_dir = os.path.join(current_dir, "config")
print("\nFiles in config directory:")
if os.path.exists(config_dir):
    for f in os.listdir(config_dir):
        print(f"- {f}")
else:
    print("Config directory does not exist!")

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

print(f"\nProject root: {project_root}")
print(f"Python path: {sys.path}")

try:
    from config.personas import EXAMPLE_PERSONAS
    from config.dialogue_contexts import DIALOGUE_SCENARIOS
    from agents.dialogue_manager import DialogueManager

    def generate_dialogue(scenario_name: str, persona_pairs: list, num_turns: int = 4):
        """
        Generate a dialogue for a specific scenario and persona pair.
        
        Args:
            scenario_name: Name of the scenario to use
            persona_pairs: List of tuples of persona IDs to use
            num_turns: Number of turns to generate
        """
        # Initialize the dialogue manager
        manager = DialogueManager()
        
        # Get the scenario
        scenario = DIALOGUE_SCENARIOS[scenario_name]
        
        # Add personas
        for persona_id, persona in persona_pairs:
            manager.add_persona(persona_id, persona)
        
        # Start the dialogue
        manager.start_dialogue(context=scenario.context, goal=scenario.goal)
        
        print(f"\nScenario: {scenario.name}")
        print("\nContext:", scenario.context)
        print("\nGoal:", scenario.goal)
        print("\nSuggested Topics:")
        for topic in scenario.suggested_topics:
            print(f"- {topic}")
        print("\nStarting dialogue...\n")
        
        # Generate dialogue turns
        for turn in range(num_turns):
            # Alternate between personas
            current_pair = persona_pairs[turn % len(persona_pairs)]
            persona_id = current_pair[0]
            
            print(f"\nGenerating turn {turn + 1} for {persona_id}...")
            result = manager.generate_turn(persona_id)
            
            print(f"\n{result['speaker']}: {result['content']}")
            print("\nAnalysis:")
            print("- Persona Consistency:", result['analysis']['persona_consistency'])
            print("- Stereotype Patterns:", result['analysis']['stereotype_patterns'])
            print("- Language Authenticity:", result['analysis']['language_authenticity'])
            print("\n" + "-"*80)
        
        # Export the dialogue
        output = manager.export_dialogue()
        
        # Add scenario information to output
        output["scenario"] = scenario.to_dict()
        
        return output

    def main():
        # Define available persona pairs for different scenarios
        scenario_personas = {
            "tech_hub": [
                ("urban_prof", EXAMPLE_PERSONAS["urban_professional"]),
                ("rural_trade", EXAMPLE_PERSONAS["rural_tradesperson"])
            ],
            "education_reform": [
                ("suburban_edu", EXAMPLE_PERSONAS["suburban_educator"]),
                ("rural_trade", EXAMPLE_PERSONAS["rural_tradesperson"])
            ]
        }
        
        # Generate dialogues for different scenarios
        all_dialogues = []
        
        for scenario_name, personas in scenario_personas.items():
            print(f"\nGenerating dialogue for scenario: {scenario_name}")
            dialogue = generate_dialogue(scenario_name, personas)
            all_dialogues.append(dialogue)
        
        # Save all dialogues
        output = {
            "dialogues": all_dialogues,
            "metadata": {
                "num_scenarios": len(all_dialogues),
                "personas_used": list(EXAMPLE_PERSONAS.keys()),
                "scenarios_used": list(scenario_personas.keys())
            }
        }
        
        # Save to file
        with open("dialogue_output.json", "w") as f:
            json.dump(output, f, indent=2)
        
        print("\nAll dialogues saved to dialogue_output.json")

    if __name__ == "__main__":
        main()

except ImportError as e:
    print(f"\nImport Error: {e}")
    print("\nPlease verify that all required files exist:")
    required_files = [
        "config/__init__.py",
        "config/personas.py",
        "config/dialogue_contexts.py",
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
        path = os.path.join(current_dir, file)
        exists = os.path.exists(path)
        print(f"- {file}: {'✓' if exists else '✗'}")
