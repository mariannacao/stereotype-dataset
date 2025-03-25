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
    from config.personas import PERSONAS
    from agents.dialogue_manager import DialogueManager

    def main():
        # Initialize dialogue manager with personas and topic
        dialogue_manager = DialogueManager(
            personas={
                "speaker1": PERSONAS["urban_educated"],
                "speaker2": PERSONAS["rural_traditional"]
            },
            topic="The impact of technology on traditional farming methods"
        )
        
        # Generate dialogue turns
        for _ in range(6):  # 3 turns each
            dialogue_manager.generate_turn("speaker1")
            dialogue_manager.generate_turn("speaker2")
        
        # Save dialogue history
        with open("dialogue_output.json", "w") as f:
            json.dump(dialogue_manager.dialogue_history, f, indent=2)
        
        # Print dialogue
        print("\nGenerated Dialogue:")
        print(dialogue_manager._format_dialogue_history())

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
