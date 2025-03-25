import os
import sys
import json

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
    from agents.dialogue_manager import DialogueManager

    def main():
        # Initialize the dialogue manager
        manager = DialogueManager()
        
        # Add personas
        manager.add_persona("urban_prof", EXAMPLE_PERSONAS["urban_professional"])
        manager.add_persona("rural_trade", EXAMPLE_PERSONAS["rural_tradesperson"])
        
        # Set up the dialogue context
        context = """Setting: A community meeting about installing a new tech hub in a rural town.
        The discussion is about the potential benefits and drawbacks of the development."""
        
        goal = """Generate a dialogue that explores different perspectives on technological development
        in rural areas, revealing potential stereotypes and biases that might emerge in such discussions."""
        
        # Start the dialogue
        manager.start_dialogue(context=context, goal=goal)
        
        # Generate a few turns of dialogue
        speakers = ["urban_prof", "rural_trade", "urban_prof", "rural_trade"]
        
        print("\nContext:", context)
        print("\nGoal:", goal)
        print("\nStarting dialogue...\n")
        
        for speaker_id in speakers:
            print(f"\nGenerating turn for {speaker_id}...")
            result = manager.generate_turn(speaker_id)
            
            print(f"\n{result['speaker']}: {result['content']}")
            print("\nAnalysis:")
            print("- Persona Consistency:", result['analysis']['persona_consistency'])
            print("- Stereotype Patterns:", result['analysis']['stereotype_patterns'])
            print("- Language Authenticity:", result['analysis']['language_authenticity'])
            print("\n" + "-"*80)
        
        # Export the dialogue
        output = manager.export_dialogue()
        
        # Save to file
        with open("dialogue_output.json", "w") as f:
            json.dump(output, f, indent=2)
        
        print("\nDialogue saved to dialogue_output.json")

    if __name__ == "__main__":
        main()

except ImportError as e:
    print(f"\nImport Error: {e}")
    print("\nPlease verify that all required files exist:")
    required_files = [
        "config/__init__.py",
        "config/personas.py",
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
