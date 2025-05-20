let ws = null;
let scenarios = [];
let isGenerating = false;

const categorySelect = document.getElementById('categorySelect');
const scenarioSelect = document.getElementById('scenarioSelect');
const generateBtn = document.getElementById('generateBtn');
const dialogueContainer = document.getElementById('dialogueContainer');
const analysisContainer = document.getElementById('analysisContainer');

function initWebSocket() {
    ws = new WebSocket(`ws://${window.location.host}/ws`);
    
    ws.onopen = () => {
        console.log('WebSocket connected');
        generateBtn.disabled = false;
    };
    
    ws.onclose = () => {
        console.log('WebSocket disconnected');
        generateBtn.disabled = true;
        setTimeout(initWebSocket, 5000);
    };
    
    ws.onerror = (error) => {
        console.error('WebSocket error:', error);
    };
    
    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        handleWebSocketMessage(data);
    };
}

function handleWebSocketMessage(data) {
    switch (data.type) {
        case 'metadata':
            addPersonaMetadata(data.personas);
            break;
        case 'turn':
            addDialogueTurn(data);
            addAnalysisItem(data);
            break;
        case 'complete':
            showCompletionMessage(data.message);
            isGenerating = false;
            updateGenerateButton();
            break;
        case 'error':
            showErrorMessage(data.message);
            isGenerating = false;
            updateGenerateButton();
            break;
    }
}

function addPersonaMetadata(personas) {
    const metadataDiv = document.createElement('div');
    metadataDiv.className = 'metadata-section mb-4';
    metadataDiv.innerHTML = `
        <h2 class="text-xl font-semibold mb-4">Characters</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            ${personas.map(persona => `
                <div class="persona-card bg-white p-6 rounded-lg shadow-md">
                    <div class="flex items-center mb-4">
                        <div class="w-12 h-12 bg-indigo-100 rounded-full flex items-center justify-center mr-4">
                            <span class="text-indigo-600 font-semibold text-lg">${persona.name.split(' ').map(n => n[0]).join('')}</span>
                        </div>
                        <div>
                            <h3 class="font-semibold text-lg">${persona.name}</h3>
                            <p class="text-gray-600 text-sm">${persona.attributes.occupation}</p>
                        </div>
                    </div>
                    
                    <div class="space-y-4">
                        <div>
                            <h4 class="text-sm font-medium text-gray-500 mb-1">Background</h4>
                            <p class="text-gray-700">${persona.background}</p>
                        </div>
                        
                        <div>
                            <h4 class="text-sm font-medium text-gray-500 mb-1">Attributes</h4>
                            <div class="grid grid-cols-2 gap-2">
                                ${Object.entries(persona.attributes).map(([key, value]) => `
                                    <div class="text-sm">
                                        <span class="text-gray-500">${key.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}:</span>
                                        <span class="text-gray-700">${value}</span>
                                    </div>
                                `).join('')}
                            </div>
                        </div>
                        
                        <div>
                            <h4 class="text-sm font-medium text-gray-500 mb-1">Personality Traits</h4>
                            <div class="flex flex-wrap gap-2">
                                ${persona.personality_traits.map(trait => `
                                    <span class="px-2 py-1 bg-indigo-50 text-indigo-700 rounded-full text-sm">${trait}</span>
                                `).join('')}
                            </div>
                        </div>
                        
                        <div>
                            <h4 class="text-sm font-medium text-gray-500 mb-1">Communication Style</h4>
                            <div class="grid grid-cols-2 gap-2">
                                ${Object.entries(persona.communication_style).map(([key, value]) => `
                                    <div class="text-sm">
                                        <span class="text-gray-500">${key.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}:</span>
                                        <span class="text-gray-700">${value}</span>
                                    </div>
                                `).join('')}
                            </div>
                        </div>
                        
                        <div>
                            <h4 class="text-sm font-medium text-gray-500 mb-1">Core Values</h4>
                            <div class="flex flex-wrap gap-2">
                                ${persona.values.map(value => `
                                    <span class="px-2 py-1 bg-green-50 text-green-700 rounded-full text-sm">${value}</span>
                                `).join('')}
                            </div>
                        </div>
                        
                        <div>
                            <h4 class="text-sm font-medium text-gray-500 mb-1">Key Experiences</h4>
                            <ul class="list-disc list-inside text-sm text-gray-700 space-y-1">
                                ${persona.experiences.map(exp => `
                                    <li>${exp}</li>
                                `).join('')}
                            </ul>
                        </div>
                    </div>
                </div>
            `).join('')}
        </div>
    `;
    
    dialogueContainer.parentNode.insertBefore(metadataDiv, dialogueContainer);
}

function addDialogueTurn(data) {
    const turnDiv = document.createElement('div');
    turnDiv.className = `dialogue-turn ${data.persona_id}`;
    
    let text = '';
    try {
        if (typeof data.content === 'string') {
            text = data.content;
        } else if (typeof data.content === 'object') {
            text = data.content.content || JSON.stringify(data.content);
        } else {
            text = JSON.stringify(data.content);
        }
    } catch (e) {
        console.error('Error parsing dialogue text:', e);
        text = 'Error displaying dialogue';
    }
    
    if (data.turn_analysis && data.turn_analysis.highlighted_segments && data.turn_analysis.highlighted_segments.length > 0) {
        data.turn_analysis.highlighted_segments.forEach(segment => {
            text = text.replace(
                segment.text,
                `<span class="highlight-stereotype">${segment.text}</span>`
            );
        });
    }
    
    const personaNumber = parseInt(data.persona_id.replace('persona', ''));
    const personaCard = document.querySelector(`.persona-card:nth-child(${personaNumber}) h3`);
    const personaName = personaCard ? personaCard.textContent : data.speaker;
    
    turnDiv.innerHTML = `
        <div class="font-semibold mb-2">${personaName}</div>
        <div class="whitespace-pre-wrap">${text}</div>
    `;
    
    dialogueContainer.appendChild(turnDiv);
    dialogueContainer.scrollTop = dialogueContainer.scrollHeight;
}

function addAnalysisItem(data) {
    const analysisDiv = document.createElement('div');
    analysisDiv.className = `analysis-item ${data.analysis.stereotype_detected ? 'stereotype-detected' : 'no-stereotype'}`;
    
    let analysisText = '';
    try {
        if (data.text && data.text.turn_analysis) {
            analysisText = data.text.turn_analysis.stereotype_analysis || 
                          data.text.turn_analysis.persona_consistency || '';
        }
    } catch (e) {
        console.error('Error parsing analysis:', e);
    }
    
    analysisDiv.innerHTML = `
        <div class="font-semibold mb-2">${data.persona}'s Turn Analysis</div>
        <div class="text-sm">
            <p>Stereotype Detected: ${data.analysis.stereotype_detected ? 'Yes' : 'No'}</p>
            <p>Confidence: ${(data.analysis.confidence * 100).toFixed(1)}%</p>
            ${analysisText ? `
                <div class="mt-2 p-2 bg-gray-50 rounded">
                    <p class="font-medium">Analysis:</p>
                    <p class="whitespace-pre-wrap">${analysisText}</p>
                </div>
            ` : ''}
            ${data.analysis.highlighted_segments && data.analysis.highlighted_segments.length > 0 ? `
                <p class="mt-2">Highlighted Segments:</p>
                <ul class="list-disc list-inside">
                    ${data.analysis.highlighted_segments.map(segment => 
                        `<li>${segment.text}</li>`
                    ).join('')}
                </ul>
            ` : ''}
        </div>
    `;
    
    analysisContainer.appendChild(analysisDiv);
    analysisContainer.scrollTop = analysisContainer.scrollHeight;
}

function showCompletionMessage(message) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'text-center text-green-600 mt-4';
    messageDiv.textContent = message;
    dialogueContainer.appendChild(messageDiv);
}

function showErrorMessage(message) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'text-center text-red-600 mt-4';
    messageDiv.textContent = `Error: ${message}`;
    dialogueContainer.appendChild(messageDiv);
}

function updateGenerateButton() {
    generateBtn.disabled = isGenerating;
    generateBtn.innerHTML = isGenerating ? 
        '<span class="loading"></span> Generating...' : 
        'Generate Dialogue';
}

async function loadScenarios() {
    try {
        const response = await fetch('/api/scenarios');
        scenarios = await response.json();
        
        const categories = [...new Set(scenarios.map(s => s.category_id))];
        categorySelect.innerHTML = `
            <option value="">Select a category...</option>
            ${categories.map(categoryId => {
                const category = scenarios.find(s => s.category_id === categoryId);
                return `<option value="${categoryId}">${category.category_name}</option>`;
            }).join('')}
        `;
    } catch (error) {
        console.error('Error loading scenarios:', error);
    }
}

function updateScenarioSelect(categoryId) {
    let filteredScenarios;
    if (categoryId === 'all') {
        filteredScenarios = scenarios.filter(s => s.category_id !== 'all');
    } else {
        filteredScenarios = scenarios.filter(s => s.category_id === categoryId);
    }
    
    scenarioSelect.innerHTML = `
        <option value="">Select a scenario...</option>
        ${filteredScenarios.map(scenario => `
            <option value="${scenario.id}">${scenario.name}</option>
        `).join('')}
    `;
}

categorySelect.addEventListener('change', (e) => {
    updateScenarioSelect(e.target.value);
});

generateBtn.addEventListener('click', () => {
    const categoryId = categorySelect.value;
    const scenarioId = scenarioSelect.value;
    
    if (!categoryId || !scenarioId) {
        alert('Please select both a category and a scenario');
        return;
    }
    
    dialogueContainer.innerHTML = '';
    analysisContainer.innerHTML = '';
    
    isGenerating = true;
    updateGenerateButton();
    
    ws.send(JSON.stringify({
        category_id: categoryId,
        scenario_id: scenarioId
    }));
});

document.addEventListener('DOMContentLoaded', () => {
    initWebSocket();
    loadScenarios();
    generateBtn.disabled = true;
}); 