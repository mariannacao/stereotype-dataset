# Multiturn Dialogue Generation Framework with Implicit Stereotype Analysis

## Project Overview

This project implements a sophisticated dialogue generation framework that explores how persuasive language and implicit stereotypes manifest in conversations between personas with different backgrounds. The framework uses a multi-agent architecture to generate, monitor, and analyze dialogues while maintaining persona consistency and tracking stereotype patterns.

## LLM Configuration

We use OpenRouter as our API gateway to access language models. The current configuration uses:

- **Model**: `deepseek/deepseek-chat-v3-0324:free`
  - A free tier of DeepSeek's chat model
  - Context window: Up to 32k tokens
  - Optimized for dialogue generation and contextual understanding
  - Cost: Free tier (good for testing and initial dataset generation)

- **OpenRouter Integration**:
  - Base URL: `https://openrouter.ai/api/v1`
  - Authentication: API key-based
  - Required headers:
    - `HTTP-Referer`: Site URL for rankings
    - `X-Title`: Application identifier
  - Configuration managed via environment variables in `.env`
  - Robust error handling with retry logic

### Token Usage and Costs

#### Per-Turn Token Usage (Approximate)

1. **Generation**:
   - System prompt: ~100 tokens
   - Persona description: ~50-100 tokens
   - Conversation history: Varies (~50 tokens per turn)
   - Generated response: ~50-150 tokens

2. **Analysis**:
   - Consistency check: ~200 tokens
   - Stereotype analysis: ~200 tokens
   - Language authenticity: ~200 tokens

Total per turn: ~850-1000 tokens

#### Cost Considerations

Using the free tier of DeepSeek's model through OpenRouter allows for:
- Testing and development
- Small dataset generation
- Proof of concept work

### Core Components

### 1. Stereotype Categories (`config/stereotype_categories.py`)
Eight fundamental dimensions of stereotypes:
- Gender identity and expression
- Race and ethnic identity
- Social class and economic status
- Age and generational differences
- Religious beliefs and practices
- Physical and cognitive abilities
- Educational attainment
- Geographic location and cultural background

### 2. Persona Management (`config/personas.py`, `config/persona_generator.py`)
- Structured persona definitions with attributes
- Background generation
- Personality traits and communication styles
- Value systems and experiences

### 3. Dialogue Generation (`agents/`)
- **DialogueManager**: Orchestrates the generation process
- **GenerationAgent**: Produces contextually appropriate dialogue turns
- **MonitoringAgent**: Ensures quality and tracks patterns
- **DialogueAgent**: Base class for agent functionality

### 4. API Integration (`utils/api_wrapper.py`)
- OpenRouter API integration
- Environment variable management
- Error handling and retry logic
- Response formatting

## Output Organization

The framework organizes outputs in two ways:

1. **Raw Outputs** (`output/`):
   - Individual JSON files for each dialogue
   - Named with pattern: `{category_id}_{scenario_name}_{timestamp}.json`

2. **Analysis Outputs** (`output-archive/dialogue_outputs_*`):
   - Timestamped directories for each generation run
   - Contains:
     - `_dataset_info.json`: Metadata about all dialogues
     - Category-specific subdirectories
     - Analysis summaries and formatted outputs

## Usage

### Environment Setup

1. Create `.env` file with:
```
OPENROUTER_API_KEY=your_api_key
OPENROUTER_REFERER=http://localhost:3000
OPENROUTER_TITLE=PersuasionDialogue
OPENROUTER_MODEL=deepseek/deepseek-chat-v3-0324:free
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Framework

1. Generate dialogues:
```bash
python main.py
```

2. Format dialogues for analysis:
```bash
python format_dialogues.py
```

3. Generate analysis summaries:
```bash
python generate_summary.py
```

## Dependencies

- openai>=1.0.0: OpenAI API client
- python-dotenv: Environment variable management
- requests: HTTP requests

## Data Structures

### Persona Definition
```python
{
    "name": str,
    "attributes": {
        "gender": str,
        "age": str,
        "education": str,
        "occupation": str,
        "location": str,
        "background": str,
        "income_level": str,
        "marital_status": str
    },
    "background": str,
    "personality_traits": List[str],
    "communication_style": {
        "vocabulary": str,
        "tone": str,
        "approach": str,
        "expressions": str
    },
    "values": List[str],
    "experiences": List[str]
}
```

### Dialogue Turn
```python
{
    "speaker": str,
    "content": str,
    "persona_id": str,
    "analysis": {
        "persona_consistency": str,
        "stereotype_patterns": str,
        "language_authenticity": str
    }
}
```

### Complete Dialogue Export
```python
{
    "context": str,
    "goal": str,
    "personas": Dict[str, PersonaDict],
    "conversation": List[DialogueTurn],
    "stereotype_category": {
        "name": str,
        "description": str
    }
}
```

## Error Handling

The framework implements robust error handling:

1. **API Calls**:
   - Automatic retry with exponential backoff
   - Detailed error logging
   - Fallback responses
   - Maximum retry attempts: 3

2. **Validation**:
   - Response format verification
   - Content quality checks
   - Persona consistency validation
   - Fallback mechanisms

3. **Output Management**:
   - Safe file handling
   - Directory creation checks
   - JSON validation
   - Error recovery