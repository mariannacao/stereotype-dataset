def build_prompt(persona, context):
    return f"""You are {persona['name']}, a person who is {persona['traits']}.
Continue the following conversation in character:

{context}
"""
