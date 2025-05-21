# Multiturn Dialogue Generation Framework with Implicit Stereotype Analysis

A web application that generates and analyzes dialogues to explore implicit biases and stereotypes in conversations.

## Features

- Generate dialogues between two personas with different backgrounds
- Analyze conversations for implicit biases and stereotypes
- Highlight stereotype-containing quotes in the dialogue
- Control number of turns in the conversation
- Save generated dialogues to timestamped JSON files

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the web application:
```bash
python web/app.py
```

3. Open `http://localhost:5000` in your browser

## Usage

1. Select a category and scenario
2. Set the number of turns (minimum 2)
3. Click "Generate Dialogue"
4. View the generated dialogue and analysis
5. Generated dialogues are saved in the `output` folder