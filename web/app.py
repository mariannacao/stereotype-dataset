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

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from agents.dialogue_manager import DialogueManager
from config.dialogue_contexts import DIALOGUE_SCENARIOS
from config.stereotype_categories import STEREOTYPE_CATEGORIES

app = FastAPI()

app.mount("/static", StaticFiles(directory="web/static"), name="static")

templates = Jinja2Templates(directory="web/templates")

active_connections: List[WebSocket] = []

async def broadcast_message(message: dict):
    """Broadcast a message to all connected clients."""
    for connection in active_connections:
        try:
            await connection.send_json(message)
        except WebSocketDisconnect:
            active_connections.remove(connection)

@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    """Serve the main page."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Handle WebSocket connections for real-time dialogue streaming."""
    await websocket.accept()
    active_connections.append(websocket)
    
    try:
        while True:
            data = await websocket.receive_json()
            
            scenario_id = data.get("scenario_id")
            category_id = data.get("category_id")
            
            scenario = None
            for category in STEREOTYPE_CATEGORIES.values():
                if category.id == category_id:
                    for s in category.scenarios:
                        if s.id == scenario_id:
                            scenario = s
                            break
                    break
            
            if not scenario:
                await websocket.send_json({
                    "type": "error",
                    "message": "Scenario not found"
                })
                continue
            
            dialogue_manager = DialogueManager()
            
            for i, background in enumerate(scenario.persona_backgrounds):
                dialogue_manager.add_persona(f"persona{i+1}", background=background)
            
            dialogue_manager.start_dialogue(
                context=scenario.context,
                goal=scenario.goal
            )
            
            for i in range(len(scenario.persona_backgrounds)):
                turn = dialogue_manager.generate_turn(f"persona{i+1}")
                
                analysis = {
                    "stereotype_detected": random.choice([True, False]),
                    "confidence": random.random(),
                    "highlighted_segments": [
                        {"text": turn[:50], "type": "potential_stereotype"}
                    ] if random.random() > 0.7 else []
                }
                
                await websocket.send_json({
                    "type": "turn",
                    "persona": f"persona{i+1}",
                    "text": turn,
                    "analysis": analysis
                })
                
                await asyncio.sleep(1)
            
            await websocket.send_json({
                "type": "complete",
                "message": "Dialogue generation complete"
            })
            
    except WebSocketDisconnect:
        active_connections.remove(websocket)
    except Exception as e:
        await websocket.send_json({
            "type": "error",
            "message": str(e)
        })

@app.get("/api/scenarios")
async def get_scenarios():
    """Get available dialogue scenarios."""
    scenarios = []
    for category in STEREOTYPE_CATEGORIES.values():
        for scenario in category.scenarios:
            scenarios.append({
                "id": scenario.id,
                "name": scenario.name,
                "category_id": category.id,
                "category_name": category.name
            })
    return scenarios 