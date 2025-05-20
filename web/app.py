from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import json
import asyncio
import random
from typing import Dict, List
import sys
import os
from datetime import datetime

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from agents.dialogue_manager import DialogueManager
from config.dialogue_contexts import DIALOGUE_SCENARIOS
from config.stereotype_categories import STEREOTYPE_CATEGORIES

app = FastAPI()

app.mount("/static", StaticFiles(directory="web/static"), name="static")

templates = Jinja2Templates(directory="web/templates")

active_connections: List[WebSocket] = []

# def ensure_directory(path: str):
#     """Ensure the output directory exists."""
#     Path(path).mkdir(parents=True, exist_ok=True)

# def save_dialogue(dialogue_data: Dict, category_id: str, scenario_name: str):
#     """Save the generated dialogue to a JSON file."""
#     output_dir = "output"
#     ensure_directory(output_dir)
    
#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     filename = f"{output_dir}/{category_id}_{scenario_name.lower().replace(' ', '_')}_{timestamp}.json"
    
#     with open(filename, 'w') as f:
#         json.dump(dialogue_data, f, indent=2)
    
#     return filename

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
            data = await websocket.receive_json()
            
            scenario_id = data.get("scenario_id")
            category_id = data.get("category_id")
            
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
            for i, background in enumerate(scenario.persona_backgrounds):
                persona_name = f"Person {i+1}"  
                personas.append({
                    "name": persona_name,
                    "background": background
                })
                dialogue_manager.add_persona(f"persona{i+1}", background=background)
            
            await websocket.send_json({
                "type": "metadata",
                "personas": personas
            })
            
            dialogue_manager.start_dialogue(
                context=scenario.context,
                goal=scenario.goal
            )
            
            # all_turns = []
            
            for i in range(len(scenario.persona_backgrounds)):
                turn = dialogue_manager.generate_turn(f"persona{i+1}")
                
                if isinstance(turn, dict):
                    turn_text = turn.get('content', str(turn))
                else:
                    turn_text = str(turn)
                
                analysis = { # TODO: add analysis haha
                    "stereotype_detected": random.choice([True, False]),
                    "confidence": random.random(),
                    "highlighted_segments": [
                        {"text": turn_text[:50], "type": "potential_stereotype"}
                    ] if random.random() > 0.7 else []
                }
                
                # all_turns.append({
                #     "turn": turn,
                #     "analysis": analysis
                # })
                
                await websocket.send_json({
                    "type": "turn",
                    "persona": f"persona{i+1}",
                    "text": turn,
                    "analysis": analysis
                })
                
                await asyncio.sleep(1)
            
            # dialogue_data = {
            #     "category_id": category_id,
            #     "scenario_name": scenario.name,
            #     "context": scenario.context,
            #     "goal": scenario.goal,
            #     "turns": all_turns,
            #     "timestamp": datetime.now().isoformat()
            # }
            
            # saved_file = save_dialogue(dialogue_data, category_id, scenario.name)
            
            await websocket.send_json({
                "type": "complete",
                "message": "Dialogue generation complete"
            })
            
    except WebSocketDisconnect:
        active_connections.remove(websocket)
    except Exception as e:
        print(f"Error in WebSocket: {str(e)}")
        await websocket.send_json({
            "type": "error",
            "message": str(e)
        })

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