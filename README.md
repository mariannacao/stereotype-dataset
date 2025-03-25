# Persuasion Dialogue Framework with Persona and Stereotype Awareness

## Project Overview

This project implements a sophisticated dialogue generation framework that explores how persuasive language and implicit stereotypes manifest in conversations between personas with different backgrounds. The framework uses a multi-agent architecture to generate, monitor, and analyze dialogues while maintaining persona consistency and tracking stereotype patterns.

## Technical Implementation

### LLM Configuration

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

### Core Components

#### 1. Persona Management (`config/personas.py`)

- **Classes**:
  - `PersonaAttribute`: Represents individual persona characteristics
  - `Persona`: Complete persona definition with attributes, background, and traits
  
- **Features**:
  - Structured attribute storage
  - Natural language description generation
  - JSON serialization support
  - Example personas included (urban professional and rural tradesperson)

#### 2. API Integration (`utils/api_wrapper.py`)

- **Class**: `OpenRouterAPI`
- **Key Features**:
  - Environment variable management
  - Configurable API parameters
  - Error handling and retry logic
  - Message formatting for API calls
  - Support for temperature and sampling parameters

#### 3. Generation Agent (`agents/generation_agent.py`)

- **Purpose**: Produces contextually appropriate dialogue turns
- **Features**:
  - Persona-aware generation
  - Context maintenance
  - System prompt engineering
  - Temperature control for output variation

#### 4. Monitoring Agent (`agents/monitoring_agent.py`)

- **Purpose**: Ensures dialogue quality and tracks patterns
- **Analysis Areas**:
  - Persona consistency checking
  - Stereotype pattern identification
  - Language authenticity validation
  - Turn-by-turn analysis

#### 5. Dialogue Manager (`agents/dialogue_manager.py`)

- **Purpose**: Orchestrates the dialogue generation process
- **Features**:
  - Turn management
  - Persona tracking
  - Dialogue context maintenance
  - Export functionality
  - Invalid turn handling and regeneration

### Data Structures

#### 1. Persona Definition
```python
{
    "name": str,
    "attributes": {
        "gender": str,
        "age": str,
        "education": str,
        "occupation": str,
        "location": str,
        "background": str
    },
    "background": str,
    "personality_traits": List[str]
}
```

#### 2. Dialogue Turn
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

#### 3. Complete Dialogue Export
```python
{
    "context": str,
    "goal": str,
    "personas": Dict[str, PersonaDict],
    "conversation": List[DialogueTurn]
}
```

### Output and Analysis

The framework generates several types of output:

1. **Real-time Analysis**:
   - Turn-by-turn persona consistency checks
   - Stereotype pattern identification
   - Language authenticity validation

2. **Dialogue Export** (`dialogue_output.json`):
   - Full conversation history
   - Speaker metadata
   - Turn-level analysis
   - Context and goals
   - Persona definitions

3. **Analysis Metrics**:
   - Persona consistency scores
   - Stereotype pattern frequency
   - Language authenticity measures

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

Basic usage:
```python
python main.py
```

This will:
1. Initialize the dialogue manager
2. Load predefined personas
3. Generate a multi-turn dialogue
4. Perform analysis
5. Save results to `dialogue_output.json`

### Dataset Generation

The framework can be extended for dataset generation by:
1. Defining multiple scenarios
2. Creating diverse personas
3. Running multiple dialogue sessions
4. Collecting and aggregating results

## Token Usage and Costs

### Per-Turn Token Usage (Approximate)

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

### Cost Considerations

Using the free tier of DeepSeek's model through OpenRouter allows for:
- Testing and development
- Small dataset generation
- Proof of concept work

For larger datasets, consider:
1. Rate limiting implementation
2. Batch processing
3. Cost monitoring
4. Error handling and retry logic

## Future Extensions

1. **Additional Personas**:
   - More demographic variations
   - Complex background stories
   - Specialized knowledge areas

2. **Enhanced Analysis**:
   - Quantitative stereotype metrics
   - Sentiment analysis
   - Bias detection algorithms

3. **Dataset Generation**:
   - Scenario templating
   - Automated variation generation
   - Quality filtering

4. **Model Variations**:
   - Different LLM testing
   - Parameter optimization
   - Custom fine-tuning

## Dependencies

- openai>=1.0.0: OpenAI API client
- python-dotenv: Environment variable management
- requests: HTTP requests

## Project Structure
```
stereotype-dialogue/
├── agents/
│   ├── __init__.py
│   ├── dialogue_manager.py
│   ├── generation_agent.py
│   └── monitoring_agent.py
├── config/
│   ├── __init__.py
│   └── personas.py
├── utils/
│   ├── __init__.py
│   └── api_wrapper.py
├── prompts/
│   └── __init__.py
├── .env
├── .gitignore
├── main.py
├── requirements.txt
└── README.md
```
