from typing import Dict, List, Optional

class PersonaAttribute:
    def __init__(self, name: str, value: str, description: Optional[str] = None):
        self.name = name
        self.value = value
        self.description = description or ""

class Persona:
    def __init__(self, 
                 name: str,
                 attributes: Dict[str, str],
                 background: str = "",
                 personality_traits: List[str] = None):
        self.name = name
        self.attributes = {k: PersonaAttribute(k, v) for k, v in attributes.items()}
        self.background = background
        self.personality_traits = personality_traits or []
    
    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "attributes": {k: v.value for k, v in self.attributes.items()},
            "background": self.background,
            "personality_traits": self.personality_traits
        }
    
    def get_prompt_description(self) -> str:
        """Generate a natural language description of the persona for prompts"""
        desc = [f"Name: {self.name}"]
        
        # Add attributes
        for attr_name, attr in self.attributes.items():
            desc.append(f"{attr_name}: {attr.value}")
        
        # Add background if present
        if self.background:
            desc.append(f"\nBackground: {self.background}")
            
        # Add personality traits if present
        if self.personality_traits:
            traits = ", ".join(self.personality_traits)
            desc.append(f"\nPersonality traits: {traits}")
            
        return "\n".join(desc)

# Example personas
EXAMPLE_PERSONAS = {
    "urban_professional": Persona(
        name="Alex Chen",
        attributes={
            "gender": "female",
            "age": "32",
            "education": "Master's degree",
            "occupation": "Software Engineer",
            "location": "San Francisco",
            "background": "urban"
        },
        background="Grew up in a tech-focused city environment, values efficiency and innovation",
        personality_traits=["analytical", "direct", "ambitious"]
    ),
    
    "rural_tradesperson": Persona(
        name="Mike Johnson",
        attributes={
            "gender": "male", 
            "age": "45",
            "education": "Technical certification",
            "occupation": "Auto mechanic",
            "location": "Rural Montana",
            "background": "rural"
        },
        background="Lifelong resident of a small town, values tradition and practical skills",
        personality_traits=["practical", "straightforward", "traditional"]
    )
} 