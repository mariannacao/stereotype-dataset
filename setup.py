import os

# Define the project structure
structure = {
    'config': ['__init__.py', 'personas.py'],
    'agents': ['__init__.py', 'dialogue_manager.py', 'generation_agent.py', 'monitoring_agent.py'],
    'prompts': ['__init__.py', 'templates.py'],
    'utils': ['__init__.py', 'api_wrapper.py']
}

# Create directories and files
for directory, files in structure.items():
    # Create directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")
    
    # Create files if they don't exist
    for file in files:
        file_path = os.path.join(directory, file)
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                if file == '__init__.py':
                    f.write('# Package initialization\n')
            print(f"Created file: {file_path}") 