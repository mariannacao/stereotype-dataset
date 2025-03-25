from typing import Dict, List
from .dialogue_contexts import DialogueScenario

class StereotypeCategory:
    def __init__(self,
                 name: str,
                 description: str,
                 scenarios: List[DialogueScenario]):
        self.name = name
        self.description = description
        self.scenarios = scenarios
    
    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "description": self.description,
            "scenarios": [s.to_dict() for s in self.scenarios]
        }

# Define stereotype categories with their scenarios
STEREOTYPE_CATEGORIES = {
    "tech_generational": StereotypeCategory(
        name="Technology and Generational Divides",
        description="Stereotypes about age-based technological aptitude and resistance to change",
        scenarios=[
            DialogueScenario(
                name="Digital Workplace Transition",
                context="""A company meeting discussing the transition to fully digital workflows. 
                Younger and older employees are debating the merits and challenges.""",
                goal="Explore generational stereotypes about technology adoption and workplace change",
                suggested_topics=[
                    "Learning curve concerns",
                    "Work efficiency",
                    "Traditional vs modern methods",
                    "Experience vs innovation"
                ]
            )
        ]
    ),
    
    "gender_workplace": StereotypeCategory(
        name="Gender in Professional Settings",
        description="Gender-based stereotypes in workplace dynamics and leadership",
        scenarios=[
            DialogueScenario(
                name="Tech Leadership Discussion",
                context="""A tech company's leadership meeting discussing promotion criteria and 
                team dynamics. The conversation reveals subtle gender biases in tech culture.""",
                goal="Examine how gender stereotypes influence professional interactions and opportunities",
                suggested_topics=[
                    "Leadership styles",
                    "Technical expertise perception",
                    "Work-life balance",
                    "Communication patterns"
                ]
            )
        ]
    ),
    
    "rural_urban": StereotypeCategory(
        name="Rural-Urban Cultural Divide",
        description="Stereotypes based on geographic and cultural differences between urban and rural communities",
        scenarios=[
            DialogueScenario(
                name="Community Development",
                context="""A mixed group of urban developers and rural residents discussing a new 
                development project that would modernize a small town.""",
                goal="Explore stereotypes about rural and urban perspectives on progress",
                suggested_topics=[
                    "Local values",
                    "Economic development",
                    "Cultural preservation",
                    "Modern vs traditional lifestyles"
                ]
            )
        ]
    ),
    
    "education_class": StereotypeCategory(
        name="Educational and Socioeconomic Background",
        description="Stereotypes related to educational attainment and social class",
        scenarios=[
            DialogueScenario(
                name="School Reform Debate",
                context="""A community discussion about educational priorities, revealing assumptions 
                about the value of different types of education and career paths.""",
                goal="Examine class-based stereotypes in educational values and opportunities",
                suggested_topics=[
                    "Academic vs vocational training",
                    "College preparation",
                    "Career success definitions",
                    "Resource allocation"
                ]
            )
        ]
    ),
    
    "cultural_communication": StereotypeCategory(
        name="Cultural Communication Styles",
        description="Stereotypes about communication patterns across different cultural backgrounds",
        scenarios=[
            DialogueScenario(
                name="International Team Collaboration",
                context="""A global team meeting where different communication styles and cultural 
                expectations create subtle tensions and misunderstandings.""",
                goal="Explore stereotypes about cultural communication norms",
                suggested_topics=[
                    "Direct vs indirect communication",
                    "Meeting participation styles",
                    "Decision-making processes",
                    "Conflict resolution approaches"
                ]
            )
        ]
    ),
    
    "age_workplace": StereotypeCategory(
        name="Age and Workplace Value",
        description="Stereotypes about age-related workplace contributions and adaptability",
        scenarios=[
            DialogueScenario(
                name="Workplace Modernization",
                context="""A company-wide initiative to modernize work processes creates tension 
                between employees of different age groups.""",
                goal="Examine age-based stereotypes about workplace adaptation and value",
                suggested_topics=[
                    "Experience vs new skills",
                    "Change adaptation",
                    "Mentorship dynamics",
                    "Career development"
                ]
            )
        ]
    ),
    
    "regional_competence": StereotypeCategory(
        name="Regional Professional Competence",
        description="Stereotypes about professional capability based on regional background",
        scenarios=[
            DialogueScenario(
                name="Remote Work Dynamics",
                context="""A company discussing remote work policies reveals biases about the 
                capabilities and work ethic of teams from different regions.""",
                goal="Explore regional stereotypes in professional settings",
                suggested_topics=[
                    "Work quality expectations",
                    "Time zone collaboration",
                    "Local work cultures",
                    "Professional standards"
                ]
            )
        ]
    ),
    
    "innovation_tradition": StereotypeCategory(
        name="Innovation vs Traditional Expertise",
        description="Stereotypes about the value of innovation versus traditional experience",
        scenarios=[
            DialogueScenario(
                name="Industry Evolution",
                context="""A traditional industry facing technological disruption reveals tensions 
                between innovation-focused and experience-based approaches.""",
                goal="Examine stereotypes about traditional versus innovative approaches",
                suggested_topics=[
                    "Industry knowledge value",
                    "Adaptation to change",
                    "Risk assessment",
                    "Market evolution"
                ]
            )
        ]
    )
} 