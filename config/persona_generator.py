from typing import Dict, List, Optional
import random
from config.personas import Persona, PersonaAttribute

class PersonaGenerator:
    def __init__(self):
        self.genders = ["male", "female", "non-binary"]
        self.backgrounds = ["urban", "suburban", "rural"]
        self.marital_statuses = ["single", "married", "divorced", "widowed"]
        self.income_levels = ["lower class", "lower middle class", "middle class", "upper middle class", "upper class"]
        
        self.personality_traits = [
            "analytical", "creative", "ambitious", "empathetic", "practical",
            "visionary", "traditional", "innovative", "adaptable", "reserved",
            "outgoing", "detail-oriented", "big-picture", "collaborative", "independent"
        ]
        
        self.communication_styles = {
            "vocabulary": ["technical", "colloquial", "academic", "professional", "casual"],
            "tone": ["formal", "informal", "friendly", "reserved", "enthusiastic"],
            "approach": ["direct", "diplomatic", "analytical", "emotional", "practical"],
            "expressions": ["uses industry jargon", "uses local expressions", "uses academic terminology", 
                          "uses technical terms", "uses everyday language"]
        }
        
        self.values = [
            "innovation", "tradition", "community", "individualism", "efficiency",
            "sustainability", "growth", "stability", "equality", "meritocracy",
            "collaboration", "independence", "adaptability", "consistency", "progress"
        ]
        
        self.experiences = [
            "led successful projects", "worked in multiple industries", "started a business",
            "volunteered in community", "worked internationally", "mentored others",
            "faced significant challenges", "achieved major milestones", "learned from failures",
            "adapted to change", "overcame obstacles", "built strong networks"
        ]
        
        # Define name components for different cultural backgrounds
        self.name_components = {
            "european": {
                "first_names": ["James", "Emma", "Lucas", "Sophia", "William", "Olivia", "Henry", "Ava"],
                "last_names": ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis"]
            },
            "asian": {
                "first_names": ["Wei", "Mei", "Jin", "Ling", "Chen", "Xia", "Min", "Hao"],
                "last_names": ["Wang", "Li", "Zhang", "Liu", "Chen", "Yang", "Huang", "Zhao"]
            },
            "hispanic": {
                "first_names": ["Carlos", "Maria", "Jose", "Ana", "Miguel", "Sofia", "Juan", "Isabella"],
                "last_names": ["Garcia", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Perez", "Sanchez"]
            },
            "african": {
                "first_names": ["Kwame", "Amina", "Idris", "Zahara", "Tunde", "Nia", "Kofi", "Aisha"],
                "last_names": ["Okafor", "Diallo", "Ndiaye", "Ogunleye", "Bello", "Sow", "Adeleke", "Traore"]
            }
        }
    
    def generate_name(self, background: str) -> str:
        """Generate a culturally appropriate name based on background."""
        if background == "urban":
            cultural_background = random.choice(list(self.name_components.keys()))
        elif background == "rural":
            cultural_background = random.choice(["european", "hispanic"])
        else:  # suburban
            cultural_background = random.choice(["european", "asian", "hispanic"])
            
        first_name = random.choice(self.name_components[cultural_background]["first_names"])
        last_name = random.choice(self.name_components[cultural_background]["last_names"])
        return f"{first_name} {last_name}"
    
    def generate_attributes(self, background: str) -> Dict[str, str]:
        """Generate basic attributes for a persona."""
        age = random.randint(25, 65)
        gender = random.choice(self.genders)
        education = self._generate_education(background)
        occupation = self._generate_occupation(background, education)
        location = self._generate_location(background)
        income_level = random.choice(self.income_levels)
        marital_status = random.choice(self.marital_statuses)
        
        return {
            "gender": gender,
            "age": str(age),
            "education": education,
            "occupation": occupation,
            "location": location,
            "background": background,
            "income_level": income_level,
            "marital_status": marital_status
        }
    
    def _generate_education(self, background: str) -> str:
        """Generate education level based on background."""
        if background == "urban":
            return random.choice([
                "Bachelor's degree",
                "Master's degree",
                "Ph.D.",
                "Professional certification"
            ])
        elif background == "suburban":
            return random.choice([
                "High school diploma",
                "Associate's degree",
                "Bachelor's degree",
                "Master's degree"
            ])
        else:  # rural
            return random.choice([
                "High school diploma",
                "Technical certification",
                "Associate's degree",
                "Bachelor's degree"
            ])
    
    def _generate_occupation(self, background: str, education: str) -> str:
        """Generate occupation based on background and education."""
        if background == "urban":
            if "Ph.D." in education or "Master's" in education:
                return random.choice([
                    "Senior Software Engineer",
                    "Data Scientist",
                    "Research Director",
                    "University Professor",
                    "Medical Doctor"
                ])
            else:
                return random.choice([
                    "Software Developer",
                    "Marketing Manager",
                    "Financial Analyst",
                    "Project Manager",
                    "Business Consultant"
                ])
        elif background == "suburban":
            if "Bachelor's" in education or "Master's" in education:
                return random.choice([
                    "Teacher",
                    "Nurse",
                    "Accountant",
                    "Sales Manager",
                    "HR Specialist"
                ])
            else:
                return random.choice([
                    "Retail Manager",
                    "Office Administrator",
                    "Customer Service Representative",
                    "Real Estate Agent",
                    "Insurance Agent"
                ])
        else:  # rural
            if "Technical" in education or "Associate's" in education:
                return random.choice([
                    "Auto Mechanic",
                    "Electrician",
                    "Plumber",
                    "HVAC Technician",
                    "Construction Supervisor"
                ])
            else:
                return random.choice([
                    "Farm Manager",
                    "Small Business Owner",
                    "Truck Driver",
                    "Warehouse Supervisor",
                    "Maintenance Worker"
                ])
    
    def _generate_location(self, background: str) -> str:
        """Generate location based on background."""
        if background == "urban":
            return random.choice([
                "New York City",
                "San Francisco",
                "Chicago",
                "Los Angeles",
                "Boston"
            ])
        elif background == "suburban":
            return random.choice([
                "Suburban Chicago",
                "Suburban Atlanta",
                "Suburban Dallas",
                "Suburban Denver",
                "Suburban Seattle"
            ])
        else:  # rural
            return random.choice([
                "Rural Montana",
                "Rural Iowa",
                "Rural Texas",
                "Rural Kentucky",
                "Rural Oregon"
            ])
    
    def generate_background(self, attributes: Dict[str, str]) -> str:
        """Generate a background story based on attributes."""
        gender = attributes["gender"]
        age = int(attributes["age"])
        education = attributes["education"]
        occupation = attributes["occupation"]
        location = attributes["location"]
        background = attributes["background"]
        
        if background == "urban":
            return f"""Born and raised in {location} to {random.choice(['immigrant', 'local'])} parents who emphasized 
            education and professional development. Has lived in major urban centers most of {random.choice(['his', 'her', 'their'])} 
            life and values innovation and progress."""
        elif background == "suburban":
            return f"""Grew up in {location} in a {random.choice(['middle-class', 'working-class'])} family. 
            Pursued {education} and built a career in {occupation}. Values community and stability while 
            embracing gradual change."""
        else:  # rural
            return f"""Third-generation resident of {location} who grew up in a {random.choice(['farming', 'small business', 'working-class'])} 
            family. Developed practical skills early in life and later pursued {education} to enhance {random.choice(['his', 'her', 'their'])} 
            career in {occupation}. Deeply connected to the local community."""
    
    def generate_personality_traits(self, background: str) -> List[str]:
        """Generate personality traits based on background."""
        num_traits = random.randint(4, 6)
        if background == "urban":
            traits = [t for t in self.personality_traits if t in ["analytical", "ambitious", "innovative", "adaptable", "outgoing", "big-picture"]]
        elif background == "suburban":
            traits = [t for t in self.personality_traits if t in ["practical", "empathetic", "collaborative", "reserved", "detail-oriented", "traditional"]]
        else:  # rural
            traits = [t for t in self.personality_traits if t in ["practical", "traditional", "independent", "reserved", "detail-oriented", "collaborative"]]
        return random.sample(traits, num_traits)
    
    def generate_communication_style(self, background: str) -> Dict[str, str]:
        """Generate communication style based on background."""
        if background == "urban":
            return {
                "vocabulary": random.choice(["technical", "professional", "academic"]),
                "tone": random.choice(["formal", "professional", "enthusiastic"]),
                "approach": random.choice(["direct", "analytical", "innovative"]),
                "expressions": random.choice(["uses industry jargon", "uses technical terms", "uses academic terminology"])
            }
        elif background == "suburban":
            return {
                "vocabulary": random.choice(["professional", "colloquial", "casual"]),
                "tone": random.choice(["friendly", "reserved", "professional"]),
                "approach": random.choice(["diplomatic", "practical", "emotional"]),
                "expressions": random.choice(["uses everyday language", "uses local expressions", "uses professional terms"])
            }
        else:  # rural
            return {
                "vocabulary": random.choice(["colloquial", "casual", "practical"]),
                "tone": random.choice(["informal", "friendly", "reserved"]),
                "approach": random.choice(["practical", "direct", "emotional"]),
                "expressions": random.choice(["uses local expressions", "uses everyday language", "uses practical terms"])
            }
    
    def generate_values(self, background: str) -> List[str]:
        """Generate a set of core values for the persona."""
        # Define a comprehensive set of values
        values = [
            # Personal values
            "Family and relationships",
            "Personal growth",
            "Health and wellness",
            "Financial security",
            "Work-life balance",
            "Independence",
            "Creativity",
            "Adventure",
            "Stability",
            "Tradition",
            
            # Professional values
            "Career advancement",
            "Professional excellence",
            "Innovation",
            "Leadership",
            "Teamwork",
            "Work ethic",
            "Continuous learning",
            "Problem-solving",
            "Adaptability",
            "Time management",
            
            # Social values
            "Community service",
            "Social justice",
            "Diversity and inclusion",
            "Environmental sustainability",
            "Cultural preservation",
            "Global awareness",
            "Civic engagement",
            "Interpersonal relationships",
            "Communication",
            "Empathy",
            
            # Educational values
            "Lifelong learning",
            "Intellectual curiosity",
            "Critical thinking",
            "Knowledge sharing",
            "Research and discovery",
            "Academic excellence",
            "Educational access",
            "Mentorship",
            "Collaborative learning",
            "Innovation in education"
        ]
        
        # Adjust values based on background
        if background == "urban":
            values.extend([
                "Urban development",
                "Cultural diversity",
                "Technological advancement",
                "Global connectivity",
                "Innovation in urban spaces"
            ])
        elif background == "suburban":
            values.extend([
                "Community development",
                "Family-oriented living",
                "Quality education",
                "Safe neighborhoods",
                "Local business support"
            ])
        elif background == "rural":
            values.extend([
                "Agricultural sustainability",
                "Rural development",
                "Traditional knowledge",
                "Natural resource conservation",
                "Local community support"
            ])
        
        # Sample 5-7 values
        num_values = random.randint(5, 7)
        return random.sample(values, min(num_values, len(values)))
    
    def generate_experiences(self, background: str) -> List[str]:
        """Generate experiences based on background."""
        # Define a comprehensive set of experiences
        experiences = [
            # Professional experiences
            "Led successful projects",
            "Worked in multiple industries",
            "Started a business",
            "Managed large teams",
            "Developed innovative solutions",
            "Received industry recognition",
            "Mentored junior colleagues",
            "Implemented process improvements",
            "Expanded business operations",
            "Navigated industry changes",
            
            # Educational experiences
            "Completed advanced degrees",
            "Attended professional conferences",
            "Published research papers",
            "Taught courses or workshops",
            "Participated in academic programs",
            "Received academic awards",
            "Conducted field research",
            "Developed educational materials",
            "Led student organizations",
            "Participated in study abroad",
            
            # Community experiences
            "Volunteered in local organizations",
            "Served on community boards",
            "Organized community events",
            "Led youth programs",
            "Participated in cultural activities",
            "Supported local businesses",
            "Advocated for community needs",
            "Built community partnerships",
            "Created community resources",
            "Mentored community members",
            
            # Personal development experiences
            "Overcame significant challenges",
            "Adapted to major life changes",
            "Developed new skills",
            "Built professional networks",
            "Achieved personal goals",
            "Balanced multiple responsibilities",
            "Navigated cultural differences",
            "Learned from failures",
            "Pursued continuous learning",
            "Maintained work-life balance"
        ]
        
        # Add background-specific experiences
        if background == "urban":
            experiences.extend([
                "Worked in diverse urban environments",
                "Navigated city infrastructure",
                "Participated in urban development",
                "Engaged with diverse communities",
                "Adapted to urban lifestyle"
            ])
        elif background == "suburban":
            experiences.extend([
                "Contributed to suburban development",
                "Participated in local schools",
                "Supported suburban businesses",
                "Engaged in community activities",
                "Balanced suburban lifestyle"
            ])
        elif background == "rural":
            experiences.extend([
                "Worked in agricultural settings",
                "Participated in rural development",
                "Supported local farming",
                "Engaged in rural traditions",
                "Adapted to rural lifestyle"
            ])
        
        # Sample 4-6 experiences
        num_experiences = random.randint(4, 6)
        return random.sample(experiences, min(num_experiences, len(experiences)))
    
    def generate_persona(self, background: Optional[str] = None) -> Persona:
        """Generate a complete persona."""
        if background is None:
            background = random.choice(self.backgrounds)
            
        name = self.generate_name(background)
        attributes = self.generate_attributes(background)
        background_text = self.generate_background(attributes)
        personality_traits = self.generate_personality_traits(background)
        communication_style = self.generate_communication_style(background)
        values = self.generate_values(background)
        experiences = self.generate_experiences(background)
        
        return Persona(
            name=name,
            attributes=attributes,
            background=background_text,
            personality_traits=personality_traits,
            communication_style=communication_style,
            values=values,
            experiences=experiences
        ) 