let ws = null;
let scenarios = [];

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
        case 'turn':
            addDialogueTurn(data);
            addAnalysisItem(data);
            break;
        case 'complete':
            showCompletionMessage(data.message);
            break;
        case 'error':
            showErrorMessage(data.message);
            break;
    }
}

function addDialogueTurn(data) {
    const turnDiv = document.createElement('div');
    turnDiv.className = `dialogue-turn ${data.persona}`;
    
    let text = data.text;
    if (data.analysis.highlighted_segments.length > 0) {
        data.analysis.highlighted_segments.forEach(segment => {
            text = text.replace(
                segment.text,
                `<span class="highlight-stereotype">${segment.text}</span>`
            );
        });
    }
    
    turnDiv.innerHTML = `
        <div class="font-semibold mb-2">${data.persona}</div>
        <div>${text}</div>
    `;
    
    dialogueContainer.appendChild(turnDiv);
    dialogueContainer.scrollTop = dialogueContainer.scrollHeight;
}

function addAnalysisItem(data) {
    const analysisDiv = document.createElement('div');
    analysisDiv.className = `analysis-item ${data.analysis.stereotype_detected ? 'stereotype-detected' : 'no-stereotype'}`;
    
    analysisDiv.innerHTML = `
        <div class="font-semibold mb-2">${data.persona}'s Turn Analysis</div>
        <div class="text-sm">
            <p>Stereotype Detected: ${data.analysis.stereotype_detected ? 'Yes' : 'No'}</p>
            <p>Confidence: ${(data.analysis.confidence * 100).toFixed(1)}%</p>
            ${data.analysis.highlighted_segments.length > 0 ? `
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
    generateBtn.disabled = false;
}

function showErrorMessage(message) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'text-center text-red-600 mt-4';
    messageDiv.textContent = `Error: ${message}`;
    dialogueContainer.appendChild(messageDiv);
    generateBtn.disabled = false;
}

async function loadScenarios() {
    try {
        const response = await fetch('/api/scenarios');
        scenarios = await response.json();
        
        const categories = [...new Set(scenarios.map(s => s.category_name))];
        categorySelect.innerHTML = `
            <option value="">Select a category...</option>
            ${categories.map(category => `
                <option value="${category}">${category}</option>
            `).join('')}
        `;
    } catch (error) {
        console.error('Error loading scenarios:', error);
    }
}

function updateScenarioSelect(category) {
    const filteredScenarios = scenarios.filter(s => s.category_name === category);
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
    const category = categorySelect.value;
    const scenarioId = scenarioSelect.value;
    
    if (!category || !scenarioId) {
        alert('Please select both a category and a scenario');
        return;
    }
    
    dialogueContainer.innerHTML = '';
    analysisContainer.innerHTML = '';
    
    generateBtn.disabled = true;
    
    ws.send(JSON.stringify({
        category_id: category,
        scenario_id: scenarioId
    }));
});

document.addEventListener('DOMContentLoaded', () => {
    initWebSocket();
    loadScenarios();
    generateBtn.disabled = true;
}); 