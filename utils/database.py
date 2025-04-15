import sqlite3
from typing import List, Dict, Any
import json
from datetime import datetime

class DialogueDatabase:
    def __init__(self, db_path: str = "stereotype_dialogues.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.create_tables()
    
    def create_tables(self):
        """Create the necessary tables if they don't exist."""
        cursor = self.conn.cursor()
        
        # Create stereotype categories table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS stereotype_categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT NOT NULL
        )
        """)
        
        # Create scenarios table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS scenarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_id INTEGER,
            name TEXT NOT NULL,
            context TEXT NOT NULL,
            goal TEXT NOT NULL,
            FOREIGN KEY (category_id) REFERENCES stereotype_categories(id)
        )
        """)
        
        # Create personas table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS personas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            background TEXT NOT NULL,
            personality_traits TEXT NOT NULL
        )
        """)
        
        # Create dialogues table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS dialogues (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            scenario_id INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (scenario_id) REFERENCES scenarios(id)
        )
        """)
        
        # Create dialogue_turns table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS dialogue_turns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dialogue_id INTEGER,
            turn_number INTEGER NOT NULL,
            speaker_id INTEGER,
            content TEXT NOT NULL,
            FOREIGN KEY (dialogue_id) REFERENCES dialogues(id),
            FOREIGN KEY (speaker_id) REFERENCES personas(id)
        )
        """)
        
        # Create analysis table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS analysis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dialogue_id INTEGER,
            turn_id INTEGER,
            aspect TEXT NOT NULL,
            content TEXT NOT NULL,
            FOREIGN KEY (dialogue_id) REFERENCES dialogues(id),
            FOREIGN KEY (turn_id) REFERENCES dialogue_turns(id)
        )
        """)
        
        self.conn.commit()
    
    def insert_stereotype_category(self, name: str, description: str) -> int:
        """Insert a new stereotype category and return its ID."""
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO stereotype_categories (name, description) VALUES (?, ?)",
            (name, description)
        )
        self.conn.commit()
        return cursor.lastrowid
    
    def insert_scenario(self, category_id: int, name: str, context: str, goal: str) -> int:
        """Insert a new scenario and return its ID."""
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO scenarios (category_id, name, context, goal) VALUES (?, ?, ?, ?)",
            (category_id, name, context, goal)
        )
        self.conn.commit()
        return cursor.lastrowid
    
    def insert_persona(self, name: str, background: str, personality_traits: List[str]) -> int:
        """Insert a new persona and return its ID."""
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO personas (name, background, personality_traits) VALUES (?, ?, ?)",
            (name, background, json.dumps(personality_traits))
        )
        self.conn.commit()
        return cursor.lastrowid
    
    def insert_dialogue(self, scenario_id: int) -> int:
        """Insert a new dialogue and return its ID."""
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO dialogues (scenario_id) VALUES (?)",
            (scenario_id,)
        )
        self.conn.commit()
        return cursor.lastrowid
    
    def insert_dialogue_turn(self, dialogue_id: int, turn_number: int, speaker_id: int, content: str) -> int:
        """Insert a new dialogue turn and return its ID."""
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO dialogue_turns (dialogue_id, turn_number, speaker_id, content) VALUES (?, ?, ?, ?)",
            (dialogue_id, turn_number, speaker_id, content)
        )
        self.conn.commit()
        return cursor.lastrowid
    
    def insert_analysis(self, dialogue_id: int, turn_id: int, aspect: str, content: str):
        """Insert analysis for a dialogue or turn."""
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO analysis (dialogue_id, turn_id, aspect, content) VALUES (?, ?, ?, ?)",
            (dialogue_id, turn_id, aspect, content)
        )
        self.conn.commit()
    
    def get_persona_by_name(self, name: str) -> Dict[str, Any]:
        """Retrieve a persona by name."""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT id, name, background, personality_traits FROM personas WHERE name = ?",
            (name,)
        )
        row = cursor.fetchone()
        if row:
            return {
                "id": row[0],
                "name": row[1],
                "background": row[2],
                "personality_traits": json.loads(row[3])
            }
        return None
    
    def get_scenario_by_name(self, name: str) -> Dict[str, Any]:
        """Retrieve a scenario by name."""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT id, category_id, name, context, goal FROM scenarios WHERE name = ?",
            (name,)
        )
        row = cursor.fetchone()
        if row:
            return {
                "id": row[0],
                "category_id": row[1],
                "name": row[2],
                "context": row[3],
                "goal": row[4]
            }
        return None
    
    def close(self):
        """Close the database connection."""
        self.conn.close() 