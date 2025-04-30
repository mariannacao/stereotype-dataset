from typing import List, Dict, Optional
from dataclasses import dataclass
from config.persona_generator import PersonaGenerator

@dataclass
class DialogueScenario:
    name: str
    context: str
    goal: str
    suggested_topics: List[str]
    persona_backgrounds: List[str]  # List of backgrounds for personas in this scenario

@dataclass
class StereotypeCategory:
    name: str
    description: str
    scenarios: List[DialogueScenario]

# Initialize persona generator
persona_generator = PersonaGenerator()

# Define stereotype categories
STEREOTYPE_CATEGORIES = {
    "race_ethnicity": StereotypeCategory(
        name="Race and Ethnicity Stereotypes",
        description="Stereotypes based on racial and ethnic backgrounds",
        scenarios=[
            DialogueScenario(
                name="Academic Achievement",
                context="""A university faculty meeting discussing student performance and academic support programs. 
                The conversation reveals implicit racial biases about academic ability and achievement.""",
                goal="Explore racial and ethnic stereotypes about academic performance and intelligence",
                suggested_topics=[
                    "Academic expectations",
                    "Support program access",
                    "Cultural factors",
                    "Achievement gaps"
                ],
                persona_backgrounds=["urban", "suburban", "rural"]
            ),
            DialogueScenario(
                name="Workplace Dynamics",
                context="""A team meeting about project assignments and leadership roles. 
                The discussion reveals racial and ethnic biases in professional settings.""",
                goal="Examine racial and ethnic stereotypes in workplace dynamics",
                suggested_topics=[
                    "Leadership potential",
                    "Team collaboration",
                    "Professional competence",
                    "Career advancement"
                ],
                persona_backgrounds=["urban", "suburban"]
            )
        ]
    ),
    
    "gender": StereotypeCategory(
        name="Gender Stereotypes",
        description="Stereotypes based on gender identity",
        scenarios=[
            DialogueScenario(
                name="Work-Life Balance",
                context="""A team meeting about flexible work arrangements and parental leave policies. 
                The discussion reveals different expectations for men and women regarding work-life balance.""",
                goal="Examine gender-based assumptions about work-life balance and caregiving responsibilities",
                suggested_topics=[
                    "Parental leave",
                    "Flexible scheduling",
                    "Career advancement",
                    "Workplace expectations"
                ],
                persona_backgrounds=["urban", "suburban", "rural"]
            ),
            DialogueScenario(
                name="Leadership Styles",
                context="""A leadership training session discussing different management approaches. 
                The conversation reveals gender-based assumptions about leadership effectiveness.""",
                goal="Explore gender stereotypes in leadership and management",
                suggested_topics=[
                    "Decision-making styles",
                    "Communication approaches",
                    "Conflict resolution",
                    "Team management"
                ],
                persona_backgrounds=["urban", "suburban"]
            )
        ]
    ),
    
    "socioeconomic": StereotypeCategory(
        name="Socioeconomic Stereotypes",
        description="Stereotypes based on socioeconomic status",
        scenarios=[
            DialogueScenario(
                name="Educational Access",
                context="""A school board meeting discussing funding allocation and educational programs. 
                The conversation reveals class-based assumptions about educational needs and opportunities.""",
                goal="Explore socioeconomic stereotypes about educational access and achievement",
                suggested_topics=[
                    "Resource allocation",
                    "Program accessibility",
                    "Parental involvement",
                    "Educational support"
                ],
                persona_backgrounds=["urban", "suburban", "rural"]
            ),
            DialogueScenario(
                name="Career Opportunities",
                context="""A career fair where different companies discuss their hiring practices. 
                The conversation reveals class-based assumptions about career potential.""",
                goal="Examine socioeconomic stereotypes in career development",
                suggested_topics=[
                    "Professional networks",
                    "Skill development",
                    "Career advancement",
                    "Workplace culture"
                ],
                persona_backgrounds=["urban", "suburban"]
            )
        ]
    ),
    
    "education": StereotypeCategory(
        name="Education Level Stereotypes",
        description="Stereotypes based on educational attainment",
        scenarios=[
            DialogueScenario(
                name="Professional Competence",
                context="""A team meeting discussing project assignments and expertise. 
                The conversation reveals educational background biases about professional capability.""",
                goal="Explore educational stereotypes about professional competence and expertise",
                suggested_topics=[
                    "Professional expertise",
                    "Problem-solving ability",
                    "Communication skills",
                    "Leadership potential"
                ],
                persona_backgrounds=["urban", "suburban", "rural"]
            ),
            DialogueScenario(
                name="Career Advancement",
                context="""A promotion committee meeting discussing career development paths. 
                The discussion reveals educational background assumptions about career potential.""",
                goal="Examine educational stereotypes about career advancement and potential",
                suggested_topics=[
                    "Career opportunities",
                    "Professional growth",
                    "Leadership roles",
                    "Skill development"
                ],
                persona_backgrounds=["urban", "suburban"]
            )
        ]
    ),
    
    "religion": StereotypeCategory(
        name="Religious Stereotypes",
        description="Stereotypes based on religious beliefs and practices",
        scenarios=[
            DialogueScenario(
                name="Workplace Accommodation",
                context="""A human resources meeting discussing religious accommodation requests. 
                The conversation reveals implicit biases about religious practices and workplace integration.""",
                goal="Explore religious stereotypes in workplace accommodation and inclusion",
                suggested_topics=[
                    "Religious holidays",
                    "Prayer spaces",
                    "Dress codes",
                    "Workplace culture"
                ],
                persona_backgrounds=["urban", "suburban"]
            ),
            DialogueScenario(
                name="Community Integration",
                context="""A community center meeting about local events and programs. 
                The discussion reveals assumptions about religious groups and community participation.""",
                goal="Examine religious stereotypes in community settings",
                suggested_topics=[
                    "Community events",
                    "Cultural celebrations",
                    "Interfaith dialogue",
                    "Social integration"
                ],
                persona_backgrounds=["urban", "suburban"]
            )
        ]
    ),
    
    "disability": StereotypeCategory(
        name="Disability Stereotypes",
        description="Stereotypes based on physical and mental abilities",
        scenarios=[
            DialogueScenario(
                name="Workplace Accessibility",
                context="""A team meeting discussing workplace accommodations and accessibility features. 
                The conversation reveals assumptions about disability and workplace capabilities.""",
                goal="Explore disability stereotypes in workplace settings",
                suggested_topics=[
                    "Accessibility features",
                    "Workplace accommodations",
                    "Professional capabilities",
                    "Team dynamics"
                ],
                persona_backgrounds=["urban", "suburban"]
            ),
            DialogueScenario(
                name="Educational Support",
                context="""A school meeting about special education programs and support services. 
                The discussion reveals assumptions about learning abilities and educational needs.""",
                goal="Examine disability stereotypes in educational settings",
                suggested_topics=[
                    "Learning accommodations",
                    "Support services",
                    "Academic expectations",
                    "Social integration"
                ],
                persona_backgrounds=["urban", "suburban"]
            )
        ]
    )
} 