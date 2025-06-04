from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import json
import asyncio
import random
from typing import Dict, List
import sys
import os
import re
from datetime import datetime

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from agents.dialogue_manager import DialogueManager
from config.dialogue_contexts import DIALOGUE_SCENARIOS
from config.stereotype_categories import STEREOTYPE_CATEGORIES

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

active_connections: List[WebSocket] = []
current_analysis: Dict = {} 

def clean_text(text):
    if not text:
        return ""
    text = text.replace("**", "").replace("*", "")  
    text = text.replace("  \n", "\n").replace("\n  ", "\n")  
    text = re.sub(r'\s+', ' ', text)  
    return text.strip()

def ensure_directory(path: str):
    """Ensure the output directory exists."""
    Path(path).mkdir(parents=True, exist_ok=True)

def save_dialogue(dialogue_data: Dict, category_id: str, scenario_name: str, dialogue_manager: DialogueManager = None):
    """Save the generated dialogue to a JSON file."""
    output_dir = "output"
    ensure_directory(output_dir)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{output_dir}/{category_id}_{scenario_name.lower().replace(' ', '_')}_{timestamp}.json"
    
    if dialogue_manager:
        try:
            overall_analysis = dialogue_manager._analyze_conversation()
            print("\n=== RAW OVERALL ANALYSIS ===")
            print(json.dumps(overall_analysis, indent=2))
            print("===========================\n")
            
            dialogue_data["overall_analysis"] = overall_analysis
        except Exception as e:
            print(f"Error generating overall analysis for save: {str(e)}")
            dialogue_data["overall_analysis"] = {"error": str(e)}
    
    with open(filename, 'w') as f:
        json.dump(dialogue_data, f, indent=2)
    
    return filename, dialogue_data.get("overall_analysis")

async def broadcast_message(message: dict):
    for connection in active_connections:
        try:
            await connection.send_json(message)
        except WebSocketDisconnect:
            active_connections.remove(connection)

@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    
    try:
        while True:
            try:
                data = await websocket.receive_json()
                
                scenario_id = data.get("scenario_id")
                category_id = data.get("category_id")
                num_turns = data.get("num_turns", 2)
                
                if not scenario_id or not category_id:
                    await websocket.send_json({
                        "type": "error",
                        "message": "Missing required parameters"
                    })
                    continue
                
                scenario = None
                if category_id == "all":
                    for category in STEREOTYPE_CATEGORIES.values():
                        for s in category.scenarios:
                            if s.name.lower().replace(' ', '_') == scenario_id:
                                scenario = s
                                break
                        if scenario:
                            break
                else:
                    category = STEREOTYPE_CATEGORIES.get(category_id)
                    if category:
                        for s in category.scenarios:
                            if s.name.lower().replace(' ', '_') == scenario_id:
                                scenario = s
                                break
                
                if not scenario:
                    await websocket.send_json({
                        "type": "error",
                        "message": "Scenario not found"
                    })
                    continue
                
                dialogue_manager = DialogueManager()
                
                personas = []
                for i, background in enumerate(scenario.persona_backgrounds[:2]):
                    dialogue_manager.add_persona(f"persona{i+1}", background=background)
                    persona = dialogue_manager.active_personas[f"persona{i+1}"]
                    personas.append(persona.to_dict())
                
                await websocket.send_json({
                    "type": "metadata",
                    "personas": personas
                })
                
                dialogue_manager.start_dialogue(
                    context=scenario.context,
                    goal=scenario.goal
                )
                
                dialogue_data = {
                    "scenario": {
                        "name": scenario.name,
                        "category": category_id,
                        "context": scenario.context,
                        "goal": scenario.goal
                    },
                    "personas": personas,
                    "turns": []
                }
                
                for i in range(num_turns):
                    persona_id = f"persona{(i % 2) + 1}"
                    turn_data = dialogue_manager.generate_turn(persona_id)
                    
                    dialogue_data["turns"].append({
                        "persona_id": turn_data["persona_id"],
                        "speaker": turn_data["speaker"],
                        "content": turn_data["content"],
                        "turn_analysis": turn_data["turn_analysis"]
                    })
                    
                    await websocket.send_json({
                        "type": "turn",
                        "persona_id": turn_data["persona_id"],
                        "speaker": turn_data["speaker"],
                        "content": turn_data["content"],
                        "turn_analysis": turn_data["turn_analysis"]
                    })
                
                filename, cleaned_analysis = save_dialogue(dialogue_data, category_id, scenario.name, dialogue_manager)
                
                if cleaned_analysis and "error" not in cleaned_analysis:
                    await websocket.send_json({
                        "type": "complete",
                        "message": f"Dialogue generation complete. Saved to {filename}",
                        "overall_analysis": cleaned_analysis
                    })
                else:
                    await websocket.send_json({
                        "type": "error",
                        "message": f"Error generating overall analysis: {cleaned_analysis.get('error', 'Unknown error')}"
                    })
                
            except json.JSONDecodeError:
                await websocket.send_json({
                    "type": "error",
                    "message": "Invalid JSON data received"
                })
            except Exception as e:
                print(f"Error processing message: {str(e)}")
                await websocket.send_json({
                    "type": "error",
                    "message": f"Error processing message: {str(e)}"
                })
                
    except WebSocketDisconnect:
        active_connections.remove(websocket)
    except Exception as e:
        print(f"WebSocket error: {str(e)}")
        if websocket in active_connections:
            active_connections.remove(websocket)
        try:
            await websocket.send_json({
                "type": "error",
                "message": f"WebSocket error: {str(e)}"
            })
        except:
            pass

async def generate_overall_analysis(dialogue_manager: DialogueManager):
    try:
        global current_analysis
        current_analysis = dialogue_manager._analyze_conversation()
    except Exception as e:
        print(f"Error generating overall analysis: {str(e)}")
        current_analysis = {"error": str(e)}

@app.get("/api/overall-analysis")
async def get_overall_analysis():
    if not current_analysis:
        return JSONResponse(
            status_code=202,
            content={"status": "processing"}
        )
    
    if "error" in current_analysis:
        return JSONResponse(
            status_code=500,
            content={"error": current_analysis["error"]}
        )
    
    return current_analysis

@app.get("/api/scenarios")
async def get_scenarios():
    scenarios = []
    
    scenarios.append({
        "id": "all",
        "name": "All Categories",
        "category_id": "all",
        "category_name": "All Categories"
    })
    
    for category_id, category in STEREOTYPE_CATEGORIES.items():
        for scenario in category.scenarios:
            scenarios.append({
                "id": scenario.name.lower().replace(' ', '_'),
                "name": scenario.name,
                "category_id": category_id,
                "category_name": category.name
            })
    return scenarios