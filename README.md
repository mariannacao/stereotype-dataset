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
  - Robust error handling with retry logic

### Core Components

#### 1. Stereotype Categories (`config/stereotype_categories.py`)

Eight fundamental dimensions of stereotypes:
- **Gender**: Gender identity and expression stereotypes
- **Race/Ethnicity**: Racial and ethnic identity stereotypes
- **Socioeconomic**: Social class and economic status stereotypes
- **Age**: Age and generational difference stereotypes
- **Religion**: Religious beliefs and practices stereotypes
- **Disability**: Physical and cognitive abilities stereotypes
- **Education**: Educational attainment stereotypes
- **Regional**: Geographic location and cultural background stereotypes

Each category includes:
- Clear description
- Multiple scenarios
- Suggested discussion topics
- Potential conflict areas

#### 2. Persona Management (`config/personas.py`)

- **Classes**:
  - `PersonaAttribute`: Represents individual persona characteristics
  - `Persona`: Complete persona definition with attributes, background, and traits
  
- **Features**:
  - Structured attribute storage
  - Natural language description generation
  - JSON serialization support
  - Example personas with diverse backgrounds

#### 3. API Integration (`utils/api_wrapper.py`)

- **Class**: `OpenRouterAPI`
- **Key Features**:
  - Environment variable management
  - Configurable API parameters
  - Robust error handling:
    - Automatic retries (3 attempts)
    - Exponential backoff (2s, 4s, 8s)
    - Detailed error logging
    - Fallback responses
  - Message formatting for API calls
  - Support for temperature and sampling parameters

#### 4. Generation Agent (`agents/generation_agent.py`)

- **Purpose**: Produces contextually appropriate dialogue turns
- **Features**:
  - Persona-aware generation
  - Context maintenance
  - System prompt engineering
  - Temperature control for output variation
  - Error recovery mechanisms

#### 5. Monitoring Agent (`agents/monitoring_agent.py`)

- **Purpose**: Ensures dialogue quality and tracks patterns
- **Analysis Areas**:
  - Persona consistency checking
  - Stereotype pattern identification
  - Language authenticity validation
  - Turn-by-turn analysis

#### 6. Dialogue Manager (`agents/dialogue_manager.py`)

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
    "conversation": List[DialogueTurn],
    "stereotype_category": {
        "name": str,
        "description": str
    }
}
```

### Output Organization

The framework organizes outputs by stereotype categories:

```
dialogue_outputs_[timestamp]/
├── gender/
│   ├── _category_info.json
│   ├── leadership_competence.json
│   └── work_life_balance.json
├── race_ethnicity/
│   ├── _category_info.json
│   ├── academic_achievement.json
│   └── professional_competence.json
...
└── _dataset_info.json
```

### Error Handling

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

## Database Schema

The SQLite database includes tables for:
- Stereotype categories
- Scenarios
- Personas
- Dialogues
- Dialogue turns
- Analysis results

## Data Storage Evolution

The project has evolved from JSON-based storage to a more robust SQLite database system:

### Previous JSON Storage
- Dialogues were saved in timestamped directories
- Each stereotype category had its own subdirectory
- Files included raw dialogues, analyses, and metadata
- Limited querying and analysis capabilities

### Current SQLite Database
The data is now stored in `stereotype_dialogues.db` with the following structure:

1. **stereotype_categories**
   - Stores different types of stereotypes (gender, race, etc.)
   - Contains name and description

2. **scenarios**
   - Stores specific dialogue scenarios
   - Links to stereotype categories
   - Contains context and goals

3. **personas**
   - Stores character definitions
   - Contains name, background, and personality traits

4. **dialogues**
   - Stores complete conversations
   - Links to scenarios
   - Includes timestamps

5. **dialogue_turns**
   - Stores individual conversation turns
   - Links to dialogues and speakers
   - Contains the actual content

6. **analysis**
   - Stores analysis results
   - Can be linked to either entire dialogues or specific turns
   - Contains different aspects of analysis (stereotypes, consistency, etc.)

### Data Flow
When a dialogue is generated:
1. The stereotype category is inserted
2. The scenario is inserted
3. Personas are inserted (if they don't exist)
4. The dialogue is inserted
5. Each turn is inserted
6. Analysis for each turn and the overall dialogue is inserted

### Advantages of Database Storage
- Better data organization
- Easier querying and analysis
- Relationships between data are maintained
- More efficient storage
- Better data integrity

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
3. Generate dialogues for each stereotype category
4. Perform analysis
5. Save results in organized directories

### Dataset Generation

The framework supports systematic dataset generation:
1. Multiple stereotype categories
2. Diverse scenarios per category
3. Various persona combinations
4. Comprehensive analysis
5. Organized output structure

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
│   ├── personas.py
│   ├── dialogue_contexts.py
│   └── stereotype_categories.py
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

## Generation Order

The dialogues are generated in the following order of stereotype categories:

1. Gender Stereotypes
2. Race and Ethnicity Stereotypes
3. Socioeconomic Status Stereotypes
4. Age Stereotypes
5. Religious Stereotypes
6. Disability Stereotypes
7. Education Level Stereotypes

Each category contains two scenarios, and the generation process follows this order. If the generation gets cut off, you can identify which category was being processed by checking the output files and their timestamps.

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your OpenRouter API key:
   ```
   OPENROUTER_API_KEY=your_api_key_here
   OPENROUTER_REFERER=http://localhost:3000
   OPENROUTER_TITLE=PersuasionDialogue
   OPENROUTER_MODEL=deepseek/deepseek-chat-v3-0324:free
   ```

## Usage

Run the main script:
```bash
python main.py
```

This will:
1. Generate dialogues for each stereotype category
2. Save them in JSON format
3. Convert them to text format
4. Create a structured output directory

## Output Structure

The script creates a directory named `dialogue_outputs_[timestamp]` containing:
- A subdirectory for each stereotype category
- JSON files for each dialogue
- Text files for each dialogue
- Metadata files with analysis information

## Analysis

The system analyzes each dialogue for:
- Stereotype patterns
- Persona consistency
- Language authenticity
- Conversation dynamics

## Requirements

- Python 3.8+
- OpenRouter API key
- Dependencies listed in requirements.txt

## License

MIT License