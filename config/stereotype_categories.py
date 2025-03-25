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

# Define fundamental stereotype categories with their scenarios
STEREOTYPE_CATEGORIES = {
    "gender": StereotypeCategory(
        name="Gender Stereotypes",
        description="Stereotypes based on gender identity and expression",
        scenarios=[
            DialogueScenario(
                name="Leadership and Competence",
                context="""A company board meeting discussing leadership qualities and promotion criteria. 
                The conversation reveals implicit gender biases about leadership styles and competence.""",
                goal="Explore gender-based stereotypes about leadership ability and professional competence",
                suggested_topics=[
                    "Leadership styles and effectiveness",
                    "Technical vs interpersonal skills",
                    "Decision-making approaches",
                    "Communication patterns"
                ]
            ),
            DialogueScenario(
                name="Work-Life Balance",
                context="""A team meeting about flexible work arrangements and parental leave policies. 
                The discussion reveals different expectations for men and women regarding work-life balance.""",
                goal="Examine gender-based assumptions about work-life balance and caregiving responsibilities",
                suggested_topics=[
                    "Parental leave policies",
                    "Flexible work arrangements",
                    "Career advancement",
                    "Family responsibilities"
                ]
            )
        ]
    ),
    
    "race_ethnicity": StereotypeCategory(
        name="Race and Ethnicity Stereotypes",
        description="Stereotypes based on racial and ethnic identity",
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
                ]
            ),
            DialogueScenario(
                name="Professional Competence",
                context="""A hiring committee meeting discussing candidate qualifications and team fit. 
                The discussion reveals subtle racial biases in professional competence assessment.""",
                goal="Examine racial stereotypes in professional settings and hiring decisions",
                suggested_topics=[
                    "Qualification evaluation",
                    "Cultural fit assessment",
                    "Professional experience",
                    "Team dynamics"
                ]
            )
        ]
    ),
    
    "socioeconomic": StereotypeCategory(
        name="Socioeconomic Status Stereotypes",
        description="Stereotypes based on social class and economic status",
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
                ]
            ),
            DialogueScenario(
                name="Work Ethic and Values",
                context="""A community development meeting about local employment programs. 
                The discussion reveals class-based stereotypes about work ethic and values.""",
                goal="Examine socioeconomic stereotypes about work ethic and personal values",
                suggested_topics=[
                    "Work motivation",
                    "Career aspirations",
                    "Financial management",
                    "Social responsibility"
                ]
            )
        ]
    ),
    
    "age": StereotypeCategory(
        name="Age Stereotypes",
        description="Stereotypes based on age and generational differences",
        scenarios=[
            DialogueScenario(
                name="Technology Adoption",
                context="""A company meeting about digital transformation initiatives. 
                The conversation reveals age-based assumptions about technology adoption and learning ability.""",
                goal="Explore age-based stereotypes about technological competence and adaptability",
                suggested_topics=[
                    "Learning ability",
                    "Technology adoption",
                    "Change resistance",
                    "Digital skills"
                ]
            ),
            DialogueScenario(
                name="Workplace Value",
                context="""A team meeting discussing project assignments and mentorship roles. 
                The discussion reveals age-based stereotypes about workplace contributions.""",
                goal="Examine age-based stereotypes about professional value and capability",
                suggested_topics=[
                    "Experience value",
                    "Innovation potential",
                    "Leadership ability",
                    "Career development"
                ]
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
                    "Religious practices",
                    "Workplace policies",
                    "Cultural sensitivity",
                    "Team integration"
                ]
            ),
            DialogueScenario(
                name="Professional Ethics",
                context="""A business ethics committee meeting discussing company values and practices. 
                The discussion reveals religious-based assumptions about ethical behavior.""",
                goal="Examine religious stereotypes about professional ethics and values",
                suggested_topics=[
                    "Ethical standards",
                    "Business practices",
                    "Value alignment",
                    "Decision-making"
                ]
            )
        ]
    ),
    
    "disability": StereotypeCategory(
        name="Disability Stereotypes",
        description="Stereotypes based on physical and cognitive abilities",
        scenarios=[
            DialogueScenario(
                name="Workplace Accessibility",
                context="""A company meeting about workplace accessibility and accommodation. 
                The conversation reveals implicit biases about disability and workplace capability.""",
                goal="Explore disability stereotypes about workplace competence and accommodation",
                suggested_topics=[
                    "Workplace accessibility",
                    "Performance capability",
                    "Accommodation needs",
                    "Team integration"
                ]
            ),
            DialogueScenario(
                name="Professional Development",
                context="""A career development meeting discussing training and advancement opportunities. 
                The discussion reveals assumptions about disability and professional growth.""",
                goal="Examine disability stereotypes about professional development and advancement",
                suggested_topics=[
                    "Career advancement",
                    "Training opportunities",
                    "Leadership potential",
                    "Professional growth"
                ]
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
                ]
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
                ]
            )
        ]
    ),
    
    "regional": StereotypeCategory(
        name="Regional Stereotypes",
        description="Stereotypes based on geographic location and cultural background",
        scenarios=[
            DialogueScenario(
                name="Workplace Culture",
                context="""A global team meeting discussing work practices and communication styles. 
                The conversation reveals regional biases about workplace culture and effectiveness.""",
                goal="Explore regional stereotypes about workplace culture and professional practices",
                suggested_topics=[
                    "Work style differences",
                    "Communication patterns",
                    "Cultural norms",
                    "Professional standards"
                ]
            ),
            DialogueScenario(
                name="Professional Competence",
                context="""A project team meeting about international collaboration. 
                The discussion reveals regional assumptions about professional capability.""",
                goal="Examine regional stereotypes about professional competence and work ethic",
                suggested_topics=[
                    "Professional standards",
                    "Work ethic",
                    "Technical capability",
                    "Cultural competence"
                ]
            )
        ]
    )
} 