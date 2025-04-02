#!/usr/bin/env python3
import os
import json
import glob
from pathlib import Path
from datetime import datetime

def format_persona(persona_data):
    """Format persona data into a readable text block."""
    output = []
    
    output.append(f"PERSONA: {persona_data['name']}")
    output.append("=" * 50)
    
    output.append("ATTRIBUTES:")
    for attr_name, attr_value in persona_data['attributes'].items():
        output.append(f"  • {attr_name.replace('_', ' ').title()}: {attr_value}")
    
    if persona_data.get('background'):
        output.append("\nBACKGROUND:")
        output.append(persona_data['background'])
    
    if persona_data.get('personality_traits'):
        output.append("\nPERSONALITY TRAITS:")
        output.append(", ".join(persona_data['personality_traits']))
    
    if persona_data.get('communication_style'):
        output.append("\nCOMMUNICATION STYLE:")
        for aspect, style in persona_data['communication_style'].items():
            output.append(f"  • {aspect.replace('_', ' ').title()}: {style}")
    
    if persona_data.get('values'):
        output.append("\nCORE VALUES:")
        output.append(", ".join(persona_data['values']))
    
    if persona_data.get('experiences'):
        output.append("\nKEY EXPERIENCES:")
        for exp in persona_data['experiences']:
            output.append(f"  • {exp}")
    
    return "\n".join(output)

def format_conversation(conversation_history):
    """Format conversation history into a readable text block."""
    output = []
    output.append("CONVERSATION HISTORY AND TURN-BY-TURN ANALYSIS")
    output.append("=" * 50)
    
    if not conversation_history:
        output.append("No conversation history available.")
        return "\n".join(output)
    
    for i, turn in enumerate(conversation_history, 1):
        output.append(f"\nTurn {i}:")
        output.append(f"Speaker: {turn['speaker']}")
        output.append(f"Content: {turn['content']}")
        
        if 'analysis' in turn:
            output.append("\nTurn Analysis:")
            analysis = turn['analysis']
            
            if 'stereotype_present' in analysis:
                output.append(f"  • Stereotype Present: {analysis['stereotype_present']}")
            
            if 'stereotype_type' in analysis:
                output.append(f"  • Type of Stereotype: {analysis['stereotype_type']}")
            
            if 'implicitness' in analysis:
                output.append(f"  • Implicitness: {analysis['implicitness']}")
                if 'implicit_indicators' in analysis:
                    output.append("    Indicators:")
                    for indicator in analysis['implicit_indicators']:
                        output.append(f"    - {indicator}")
            
            if 'contextual_justification' in analysis:
                output.append(f"  • Contextual Justification: {analysis['contextual_justification']}")
            
            if 'impact' in analysis:
                output.append(f"  • Impact on Conversation: {analysis['impact']}")
            
            if 'language_patterns' in analysis:
                output.append("  • Language Patterns:")
                for pattern in analysis['language_patterns']:
                    output.append(f"    - {pattern}")
        
        output.append("-" * 50)
    
    return "\n".join(output)

def format_analysis(analysis_data):
    """Format analysis data into a readable text block."""
    output = []
    output.append("OVERALL CONVERSATION ANALYSIS")
    output.append("=" * 50)
    
    if not analysis_data:
        output.append("No analysis available.")
        return "\n".join(output)
    
    if 'stereotype_patterns' in analysis_data:
        output.append("\nRecurring Stereotype Patterns:")
        patterns = analysis_data['stereotype_patterns']
        if isinstance(patterns, str):
            patterns = patterns.replace("###", "").replace("####", "").replace("**", "").strip()
            output.append(patterns)
        elif isinstance(patterns, dict):
            for key, value in patterns.items():
                output.append(f"\n• {key.replace('_', ' ').title()}:")
                output.append(f"  {value}")
    
    if 'stereotype_evolution' in analysis_data:
        output.append("\nEvolution of Stereotypes:")
        evolution = analysis_data['stereotype_evolution']
        if isinstance(evolution, list):
            for stage in evolution:
                output.append(f"• {stage}")
        else:
            output.append(evolution)
    
    if 'cross_cultural_dynamics' in analysis_data:
        output.append("\nCross-Cultural Dynamics:")
        output.append(analysis_data['cross_cultural_dynamics'])
    
    if 'power_dynamics' in analysis_data:
        output.append("\nPower Dynamics:")
        output.append(analysis_data['power_dynamics'])
    
    if 'dialogue_impact' in analysis_data:
        output.append("\nImpact on Dialogue Progression:")
        output.append(analysis_data['dialogue_impact'])
    
    for key, value in analysis_data.items():
        if key not in ['stereotype_patterns', 'stereotype_evolution', 'cross_cultural_dynamics', 
                      'power_dynamics', 'dialogue_impact'] and value and value != "---":
            output.append(f"\n{key.replace('_', ' ').title()}:")
            if isinstance(value, str):
                value = value.replace("###", "").replace("####", "").replace("**", "").strip()
                paragraphs = value.split("\n\n")
                for paragraph in paragraphs:
                    output.append(paragraph.strip())
            elif isinstance(value, dict):
                for subkey, subvalue in value.items():
                    output.append(f"• {subkey.replace('_', ' ').title()}: {subvalue}")
            elif isinstance(value, list):
                for item in value:
                    output.append(f"• {item}")
            
            output.append("-" * 50)
    
    return "\n".join(output)

def format_scenario(scenario_data):
    """Format scenario data into a readable text block."""
    output = []
    output.append("SCENARIO INFORMATION")
    output.append("=" * 50)
    
    output.append(f"Name: {scenario_data['name']}")
    
    output.append("\nContext:")
    output.append(scenario_data['context'])
    
    output.append("\nGoal:")
    output.append(scenario_data['goal'])
    
    if scenario_data.get('suggested_topics'):
        output.append("\nSuggested Topics:")
        for topic in scenario_data['suggested_topics']:
            output.append(f"  • {topic}")
    
    if scenario_data.get('potential_conflicts'):
        output.append("\nPotential Conflicts:")
        for conflict in scenario_data['potential_conflicts']:
            output.append(f"  • {conflict}")
    
    return "\n".join(output)

def process_json_file(json_path):
    """Process a single JSON file and create a formatted text file."""
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
        
        output = []
        
        output.append("DIALOGUE SUMMARY")
        output.append("=" * 80)
        
        if 'scenario' in data:
            output.append(format_scenario(data['scenario']))
            output.append("\n" + "=" * 80)
        
        output.append("\nPERSONAS")
        output.append("=" * 80)
        for persona_id, persona_data in data.get('personas', {}).items():
            output.append(format_persona(persona_data))
            output.append("\n" + "-" * 80)
        
        conversation_data = data.get('conversation', [])
        output.append("\n" + format_conversation(conversation_data))
        
        if 'analysis' in data:
            output.append("\n" + format_analysis(data['analysis']))
        
        json_dir = os.path.dirname(json_path)
        json_filename = os.path.basename(json_path)
        text_filename = json_filename.replace('.json', '.txt')
        text_path = os.path.join(json_dir, text_filename)
        
        with open(text_path, 'w') as f:
            f.write("\n".join(output))
        
        print(f"Created formatted text file: {text_path}")
        return text_path
    
    except Exception as e:
        print(f"Error processing {json_path}: {str(e)}")
        return None

def process_directory(directory_path):
    """Process all JSON files in a directory and its subdirectories."""
    json_files = glob.glob(os.path.join(directory_path, "**", "*.json"), recursive=True)
    json_files = [f for f in json_files if not os.path.basename(f).startswith('_')]
    
    print(f"Found {len(json_files)} JSON files to process")
    
    for json_path in json_files:
        process_json_file(json_path)

def main():
    output_dirs = glob.glob("dialogue_outputs_*")
    if not output_dirs:
        print("No dialogue output directories found")
        return
    
    latest_dir = max(output_dirs, key=os.path.getctime)
    print(f"Processing directory: {latest_dir}")
    
    process_directory(latest_dir)
    
    print("\nAll dialogue files have been formatted into text files.")
    print(f"Text files are located in the same directories as the original JSON files.")

if __name__ == "__main__":
    main() 