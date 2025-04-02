from typing import Dict, List

class DialogueScenario:
    def __init__(self,
                 name: str,
                 context: str,
                 goal: str,
                 suggested_topics: List[str] = None,
                 potential_conflicts: List[str] = None,
                 persona_ids: List[str] = None):
        self.name = name
        self.context = context
        self.goal = goal
        self.suggested_topics = suggested_topics or []
        self.potential_conflicts = potential_conflicts or []
        self.persona_ids = persona_ids or []
    
    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "context": self.context,
            "goal": self.goal,
            "suggested_topics": self.suggested_topics,
            "potential_conflicts": self.potential_conflicts,
            "persona_ids": self.persona_ids
        }

# Collection of pre-defined dialogue scenarios
DIALOGUE_SCENARIOS = {
    "tech_hub": DialogueScenario(
        name="Tech Hub Development",
        context="""Setting: A community meeting in a rural town hall discussing a proposal to build a major 
        tech hub on the outskirts of town. The development would bring jobs and economic growth but might 
        affect the traditional way of life and local businesses.""",
        goal="""Generate a dialogue that explores the tension between technological progress and traditional 
        values, revealing how different backgrounds influence perspectives on development.""",
        suggested_topics=[
            "Economic impact on local businesses",
            "Job opportunities for local residents",
            "Changes to town character and culture",
            "Environmental concerns",
            "Property values and housing costs"
        ],
        potential_conflicts=[
            "Modern vs traditional work values",
            "Urban development vs rural preservation",
            "Technical skills gap",
            "Cultural changes in the community"
        ]
    ),
    
    "education_reform": DialogueScenario(
        name="Education Modernization",
        context="""Setting: A school board meeting discussing the implementation of a new technology-focused 
        curriculum in the local high school. The proposal includes mandatory coding classes and reduced 
        focus on traditional vocational training.""",
        goal="""Explore different perspectives on education reform, particularly how background and 
        experience shape views on what skills are valuable in modern society.""",
        suggested_topics=[
            "Balance of practical vs technical skills",
            "Future job market needs",
            "Cost of implementing new programs",
            "Teacher training requirements",
            "Impact on traditional subjects"
        ],
        potential_conflicts=[
            "Traditional vs modern education approaches",
            "Local job market needs vs global trends",
            "Resource allocation priorities",
            "Digital divide concerns"
        ]
    ),
    
    "farming_innovation": DialogueScenario(
        name="Agricultural Technology",
        context="""Setting: A farmers' market where traditional farmers and tech-savvy agricultural 
        consultants are discussing the implementation of smart farming technologies. The debate centers 
        on efficiency versus traditional farming methods.""",
        goal="""Generate dialogue that reveals how different approaches to farming reflect deeper 
        cultural values and assumptions about progress and tradition.""",
        suggested_topics=[
            "Cost-benefit of automation",
            "Environmental impact",
            "Food quality and safety",
            "Traditional farming knowledge",
            "Market competitiveness"
        ],
        potential_conflicts=[
            "Automation vs manual labor",
            "Data-driven vs experience-based decisions",
            "Scale of operations",
            "Environmental considerations"
        ]
    ),
    
    "healthcare_access": DialogueScenario(
        name="Rural Healthcare Technology",
        context="""Setting: A town hall meeting about implementing telemedicine services at the local 
        clinic. The discussion involves healthcare professionals from both urban and rural backgrounds.""",
        goal="""Explore how different perspectives on healthcare delivery are shaped by geographic, 
        educational, and cultural backgrounds.""",
        suggested_topics=[
            "Access to specialists",
            "Quality of care concerns",
            "Internet infrastructure needs",
            "Patient privacy",
            "Emergency response capabilities"
        ],
        potential_conflicts=[
            "Traditional vs remote healthcare",
            "Technology adoption barriers",
            "Personal touch in medicine",
            "Cost and insurance implications"
        ]
    )
} 