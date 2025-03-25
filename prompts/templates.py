def build_generation_prompt(persona, context, topic):
    return f"""You are {persona['name']}, a person with a {persona['background']} background and {persona['education']} education.
Your traits include being {', '.join(persona['traits'])}.
You speak in a {persona['speaking_style']} manner.

Current conversation context:
{context}

Topic of discussion: {topic}

Respond naturally in your persona's voice, considering your background and traits.
Keep your response concise (1-2 sentences) and relevant to the ongoing discussion.
"""

def build_monitoring_prompt(persona, dialogue_history):
    return f"""Analyze if the following dialogue maintains consistency with the speaker's persona:

Persona Details:
- Name: {persona['name']}
- Background: {persona['background']}
- Education: {persona['education']}
- Speaking style: {persona['speaking_style']}

Dialogue History:
{dialogue_history}

Evaluate:
1. Does the language match the education level?
2. Are the expressions consistent with the background?
3. Does the speaking style remain consistent?

Return only "CONSISTENT" or "INCONSISTENT"
""" 