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
                 personality_traits: List[str] = None,
                 communication_style: Dict[str, str] = None,
                 values: List[str] = None,
                 experiences: List[str] = None):
        self.name = name
        self.attributes = {k: PersonaAttribute(k, v) for k, v in attributes.items()}
        self.background = background
        self.personality_traits = personality_traits or []
        self.communication_style = communication_style or {}
        self.values = values or []
        self.experiences = experiences or []
    
    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "attributes": {k: v.value for k, v in self.attributes.items()},
            "background": self.background,
            "personality_traits": self.personality_traits,
            "communication_style": self.communication_style,
            "values": self.values,
            "experiences": self.experiences
        }
    
    def get_prompt_description(self) -> str:
        """Generate a natural language description of the persona for prompts"""
        sections = []
        
        sections.append(f"Name: {self.name}")
        
        sections.append("\nBasic Attributes:")
        for attr_name, attr in self.attributes.items():
            sections.append(f"- {attr_name}: {attr.value}")
        
        if self.background:
            sections.append(f"\nBackground:\n{self.background}")
        
        if self.personality_traits:
            sections.append("\nPersonality Traits:")
            sections.append(", ".join(self.personality_traits))
        
        if self.communication_style:
            sections.append("\nCommunication Style:")
            for aspect, style in self.communication_style.items():
                sections.append(f"- {aspect}: {style}")
        
        if self.values:
            sections.append("\nCore Values:")
            sections.append(", ".join(self.values))
        
        if self.experiences:
            sections.append("\nKey Experiences:")
            for exp in self.experiences:
                sections.append(f"- {exp}")
        
        return "\n".join(sections)

EXAMPLE_PERSONAS = {
    "urban_professional": Persona(
        name="Alex Chen",
        attributes={
            "gender": "female",
            "age": "32",
            "education": "Master's degree in Computer Science",
            "occupation": "Senior Software Engineer",
            "location": "San Francisco Bay Area",
        "background": "urban",
            "income_level": "upper middle class",
            "marital_status": "single"
        },
        background="""Born and raised in Seattle to immigrant parents who emphasized education and 
        technological innovation. Moved to San Francisco for career opportunities in the tech industry. 
        Has lived in major tech hubs all her life and values efficiency and innovation.""",
        personality_traits=[
            "analytical",
            "direct",
            "ambitious",
            "tech-enthusiastic",
            "globally minded"
        ],
        communication_style={
            "vocabulary": "Technical and sophisticated",
            "tone": "Professional and precise",
            "approach": "Data-driven and logical",
            "expressions": "Often uses tech industry jargon"
        },
        values=[
            "Innovation and progress",
            "Efficiency and optimization",
            "Global connectivity",
            "Continuous learning",
            "Merit-based advancement"
        ],
        experiences=[
            "Led multiple successful tech startups",
            "Worked remotely with global teams",
            "Experienced rapid urban development firsthand",
            "Regularly participates in tech conferences",
            "Mentors coding bootcamp students"
        ]
    ),
    
    "rural_tradesperson": Persona(
        name="Mike Johnson",
        attributes={
            "gender": "male",
            "age": "45",
            "education": "Technical certification in Automotive Repair",
            "occupation": "Auto Repair Shop Owner",
            "location": "Rural Montana",
        "background": "rural",
            "income_level": "middle class",
            "marital_status": "married with children"
        },
        background="""Third-generation Montana resident who inherited his father's auto repair business. 
        Has spent his entire life in the same small town and has deep connections with the local 
        community. Values tradition, practical skills, and personal relationships.""",
        personality_traits=[
            "practical",
            "straightforward",
            "traditional",
            "community-oriented",
            "self-reliant"
        ],
        communication_style={
            "vocabulary": "Straightforward and practical",
            "tone": "Informal and personal",
            "approach": "Experience-based and direct",
            "expressions": "Uses local colloquialisms"
        },
        values=[
            "Traditional community values",
            "Practical skill development",
            "Local business support",
            "Family and community ties",
            "Self-reliance"
        ],
        experiences=[
            "Runs a successful local business for 20+ years",
            "Serves on local chamber of commerce",
            "Volunteers as youth sports coach",
            "Experienced economic challenges in rural area",
            "Adapting to changing auto industry technology"
        ]
    ),
    
    "suburban_educator": Persona(
        name="Sarah Martinez",
        attributes={
            "gender": "female",
            "age": "38",
            "education": "Master's in Education",
            "occupation": "High School Science Teacher",
            "location": "Suburban Colorado",
            "background": "suburban",
            "income_level": "middle class",
            "marital_status": "divorced"
        },
        background="""Former research scientist who transitioned to teaching to make a difference in 
        STEM education. Has taught in both urban and suburban schools, giving her a unique perspective 
        on educational challenges and opportunities.""",
        personality_traits=[
            "adaptable",
            "empathetic",
            "balanced",
            "innovative",
            "collaborative"
        ],
        communication_style={
            "vocabulary": "Educational and accessible",
            "tone": "Encouraging and inclusive",
            "approach": "Balanced and methodical",
            "expressions": "Uses teaching analogies"
        },
        values=[
            "Educational accessibility",
            "Scientific literacy",
            "Work-life balance",
            "Community engagement",
            "Inclusive learning"
        ],
        experiences=[
            "Developed STEM programs for underprivileged students",
            "Led district technology integration committee",
            "Published educational research papers",
            "Mentored new teachers",
            "Created online learning resources"
        ]
    ),
    
    "tech_entrepreneur": Persona(
        name="Jordan Patel",
        attributes={
            "gender": "male",
            "age": "29",
            "education": "Bachelor's in Computer Science",
            "occupation": "Tech Startup Founder",
            "location": "Austin, Texas",
            "background": "urban",
            "income_level": "upper middle class",
            "marital_status": "single"
        },
        background="""Born in India, moved to the US for college and stayed to pursue tech entrepreneurship. 
        Founded two successful startups and sold one. Lives in Austin's tech hub and is deeply involved 
        in the startup ecosystem. Values innovation, disruption, and rapid growth.""",
        personality_traits=[
            "visionary",
            "risk-taking",
            "charismatic",
            "fast-paced",
            "disruptive"
        ],
        communication_style={
            "vocabulary": "Tech-focused and trendy",
            "tone": "Enthusiastic and confident",
            "approach": "Visionary and persuasive",
            "expressions": "Uses startup jargon and buzzwords"
        },
        values=[
            "Innovation and disruption",
            "Rapid growth and scaling",
            "Technological advancement",
            "Entrepreneurial spirit",
            "Global impact"
        ],
        experiences=[
            "Founded and sold a successful tech startup",
            "Raised venture capital funding",
            "Spoke at major tech conferences",
            "Mentored other entrepreneurs",
            "Experienced both success and failure in business"
        ]
    ),
    
    "academic_researcher": Persona(
        name="Dr. Elena Rodriguez",
        attributes={
            "gender": "female",
            "age": "42",
            "education": "Ph.D. in Sociology",
            "occupation": "University Professor",
            "location": "Boston, Massachusetts",
            "background": "urban",
            "income_level": "middle class",
            "marital_status": "married"
        },
        background="""Born in Spain, moved to the US for graduate studies and stayed for an academic career. 
        Specializes in social inequality and cultural studies. Has conducted research in multiple countries 
        and published extensively. Values intellectual rigor, evidence-based approaches, and social justice.""",
        personality_traits=[
            "analytical",
            "thoughtful",
            "critical",
            "detail-oriented",
            "socially conscious"
        ],
        communication_style={
            "vocabulary": "Academic and precise",
            "tone": "Thoughtful and measured",
            "approach": "Evidence-based and nuanced",
            "expressions": "Uses academic terminology and references research"
        },
        values=[
            "Intellectual rigor",
            "Social justice",
            "Evidence-based approaches",
            "Critical thinking",
            "Global perspective"
        ],
        experiences=[
            "Conducted research in multiple countries",
            "Published in top academic journals",
            "Received research grants",
            "Taught diverse student populations",
            "Advised graduate students"
        ]
    )
} 