#!/usr/bin/env python3
import os
import json
import glob
from pathlib import Path
from datetime import datetime

def generate_category_summary(category_dir):
    """Generate a summary report for a category of dialogues."""
    category_info_path = os.path.join(category_dir, "_category_info.json")
    if not os.path.exists(category_info_path):
        print(f"Category info file not found: {category_info_path}")
        return None
    
    with open(category_info_path, 'r') as f:
        category_info = json.load(f)
    
    category_name = category_info.get('name', os.path.basename(category_dir))
    
    output = []
    output.append(f"SUMMARY REPORT: {category_name.upper()}")
    output.append("=" * 80)
    output.append(f"Description: {category_info.get('description', 'No description available')}")
    output.append(f"Number of scenarios: {len(category_info.get('dialogues', []))}")
    output.append("\n" + "=" * 80)
    
    for i, dialogue in enumerate(category_info.get('dialogues', []), 1):
        scenario_name = dialogue.get('scenario', {}).get('name', f"Scenario {i}")
        output.append(f"\n{i}. {scenario_name}")
        output.append("-" * 80)
        
        personas = dialogue.get('personas', {})
        if personas:
            output.append("Personas:")
            for persona_id, persona_data in personas.items():
                output.append(f"  • {persona_data.get('name', persona_id)}")
        
        conversation = dialogue.get('conversation_history', [])
        if conversation:
            output.append("\nConversation Summary:")
            for turn in conversation:
                speaker = turn.get('speaker', 'Unknown')
                content = turn.get('content', '')
                if len(content) > 100:
                    content = content[:100] + "..."
                output.append(f"  • {speaker}: {content}")
        
        analysis = dialogue.get('analysis', {})
        if analysis:
            output.append("\nKey Analysis Points:")
            for key, value in analysis.items():
                if len(value) > 150:
                    value = value[:150] + "..."
                output.append(f"  • {key.replace('_', ' ').title()}: {value}")
        
        output.append("\n" + "=" * 80)
    
    summary_path = os.path.join(category_dir, "_category_summary.txt")
    with open(summary_path, 'w') as f:
        f.write("\n".join(output))
    
    print(f"Created category summary: {summary_path}")
    return summary_path

def generate_overall_summary(base_dir):
    """Generate an overall summary of all categories."""
    dataset_info_path = os.path.join(base_dir, "_dataset_info.json")
    if not os.path.exists(dataset_info_path):
        print(f"Dataset info file not found: {dataset_info_path}")
        return None
    
    with open(dataset_info_path, 'r') as f:
        dataset_info = json.load(f)
    
    output = []
    output.append("OVERALL DIALOGUE DATASET SUMMARY")
    output.append("=" * 80)
    
    metadata = dataset_info.get('metadata', {})
    output.append(f"Generated: {metadata.get('timestamp', 'Unknown')}")
    output.append(f"Total categories: {metadata.get('total_categories', 0)}")
    output.append(f"Total dialogues: {sum(cat.get('num_dialogues', 0) for cat in metadata.get('categories', []))}")
    output.append("\n" + "=" * 80)
    
    for category in metadata.get('categories', []):
        category_id = category.get('id', 'unknown')
        category_name = category.get('name', 'Unknown Category')
        num_dialogues = category.get('num_dialogues', 0)
        
        output.append(f"\nCATEGORY: {category_name.upper()}")
        output.append("-" * 80)
        output.append(f"ID: {category_id}")
        output.append(f"Number of dialogues: {num_dialogues}")
        
        category_summary_path = os.path.join(base_dir, category_id, "_category_summary.txt")
        if os.path.exists(category_summary_path):
            output.append(f"See detailed summary in: {category_summary_path}")
        
        output.append("\n" + "-" * 80)
    
    summary_path = os.path.join(base_dir, "_overall_summary.txt")
    with open(summary_path, 'w') as f:
        f.write("\n".join(output))
    
    print(f"Created overall summary: {summary_path}")
    return summary_path

def main():
    output_dirs = glob.glob("dialogue_outputs_*")
    if not output_dirs:
        print("No dialogue output directories found")
        return
    
    latest_dir = max(output_dirs, key=os.path.getctime)
    print(f"Processing directory: {latest_dir}")
    
    for category_dir in glob.glob(os.path.join(latest_dir, "*")):
        if os.path.isdir(category_dir) and not os.path.basename(category_dir).startswith('_'):
            generate_category_summary(category_dir)
    
    generate_overall_summary(latest_dir)
    
    print("\nAll summaries have been generated.")
    print(f"Summaries are located in the {latest_dir} directory and its subdirectories.")

if __name__ == "__main__":
    main()