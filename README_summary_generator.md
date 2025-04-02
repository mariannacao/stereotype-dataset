# Dialogue Summary Generator

This tool generates summary reports for the dialogue datasets created by the Persuasion Dialogue Framework. It creates both category-specific summaries and an overall dataset summary.

## Features

- Automatically finds and processes the most recent dialogue output directory
- Generates detailed summaries for each stereotype category
- Creates an overall summary of the entire dataset
- Provides quick access to key information from each dialogue
- Helps researchers and analysts quickly understand the content of the dialogues

## Usage

1. Make sure you have already generated dialogue files using the main script:
   ```
   python main.py
   ```

2. Run the summary generator script:
   ```
   python generate_summary.py
   ```

3. The script will automatically:
   - Find the most recent `dialogue_outputs_*` directory
   - Generate a summary for each category in the dataset
   - Create an overall summary of the entire dataset

## Output Files

The script generates the following files:

### Category Summaries
- Located in each category directory as `_category_summary.txt`
- Contains:
  - Category name and description
  - Number of scenarios
  - Summary of each dialogue including:
    - Scenario name
    - Personas involved
    - Brief conversation summary
    - Key analysis points

### Overall Summary
- Located in the main output directory as `_overall_summary.txt`
- Contains:
  - Dataset metadata (timestamp, total categories, total dialogues)
  - Summary of each category
  - Links to category-specific summaries

## Example

For a dataset with categories like "gender", "race_ethnicity", etc., the script will create:
- `dialogue_outputs_TIMESTAMP/_overall_summary.txt`
- `dialogue_outputs_TIMESTAMP/gender/_category_summary.txt`
- `dialogue_outputs_TIMESTAMP/race_ethnicity/_category_summary.txt`
- And so on for each category

## Requirements

- Python 3.6+
- No additional dependencies beyond those required by the main project 