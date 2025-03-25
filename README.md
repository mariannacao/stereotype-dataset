# Implicit Stereotype Multi-turn Conversation Dataset Builder

## Project Overview
A framework for generating multi-turn dialogue between AI agents with persona and implicit stereotype awareness.

## Core Components
1. **Implicit Stereotypes**
   - Models how persuasive language is influenced by context-dependent stereotypes
   - Uses role-based scenarios to explore stereotype manifestation

2. **Persona System**
   - Each speaker has defined attributes (gender, education, background)
   - Currently using urban-educated vs rural-traditional personas

3. **Multi-Agent Architecture**
   - Generation Agent: Produces dialogue
   - Monitoring Agent: Checks persona adherence
   - Dialogue Manager: Handles turn-taking

## Technical Details
- Using OpenRouter API with DeepSeek free model
- Python-based implementation
- OpenAI SDK compatible

## Current Progress
- Implemented basic API wrapper for OpenRouter
- Created test_api.py for API verification
- Designed initial persona templates
- Started multi-agent framework implementation

## Environment Setup
```env
OPENROUTER_API_KEY=your_key_here
OPENROUTER_MODEL=deepseek/deepseek-chat-v3-0324:free
```

## Next Steps
- Complete implementation of dialogue generation framework
- Refine prompts for better persona consistency
- Implement full monitoring system
