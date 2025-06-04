let ws = null;
let scenarios = [];
let isGenerating = false;

const categorySelect = document.getElementById('categorySelect');
const scenarioSelect = document.getElementById('scenarioSelect');
const generateBtn = document.getElementById('generateBtn');
const dialogueContainer = document.getElementById('dialogueContainer');
const analysisContainer = document.getElementById('analysisContainer');
const turnsInput = document.getElementById('turnsInput');

function forceReloadStyles() {
    const links = document.getElementsByTagName('link');
    for (let i = 0; i < links.length; i++) {
        if (links[i].rel === 'stylesheet') {
            const href = links[i].href.split('?')[0];
            links[i].href = href + '?v=' + new Date().getTime();
        }
    }
}

function initWebSocket() {
    ws = new WebSocket(`ws://${window.location.host}/ws`);
    
    ws.onopen = () => {
        console.log('WebSocket connected');
        generateBtn.disabled = false;
        forceReloadStyles();
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
    console.log('Received WebSocket message:', data);  
    
    switch (data.type) {
        case 'metadata':
            console.log('Number of personas:', data.personas.length); 
            addPersonaMetadata(data.personas);
            break;
        case 'turn':
            addDialogueTurn(data);
            addAnalysisItem(data);
            break;
        case 'complete':
            addOverallAnalysis(null);
            setTimeout(() => {
                if (data.overall_analysis) {
                    renderOverallAnalysis(document.querySelector('.overall-analysis'), data.overall_analysis);
                }
                showCompletionMessage(data.message);
                isGenerating = false;
                updateGenerateButton();
            }, 100);
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
    metadataDiv.className = 'metadata-section mb-8 w-full';
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
    
    const configPanel = document.querySelector('.bg-white.rounded-lg.shadow-md.p-6.mb-8');
    const mainContentArea = document.querySelector('.grid.grid-cols-1.lg\\:grid-cols-2.gap-8');
    configPanel.parentNode.insertBefore(metadataDiv, mainContentArea);
}

function addDialogueTurn(data) {
    const turnDiv = document.createElement('div');
    turnDiv.className = `dialogue-turn ${data.persona_id}`;
    turnDiv.dataset.turnIndex = dialogueContainer.children.length;
    
    let text = data.content;
    
    const normalizeText = (str) => {
        return str
            .replace(/\u2019/g, "'")
            .replace(/\u2018/g, "'")
            .replace(/\u201c/g, '"')
            .replace(/\u201d/g, '"')
            .replace(/\u2014/g, '-')
            .replace(/\u2013/g, '-')
            .replace(/\u2026/g, '...')
            .replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
            .trim();
    };
    
    const matches = [];
    
    if (data.turn_analysis && data.turn_analysis.stereotype_quotes && data.turn_analysis.stereotype_quotes.length > 0) {
        const sortedQuotes = [...data.turn_analysis.stereotype_quotes]
            .map(quote => quote.replace(/^\d+\.\s*/, '').trim())
            .sort((a, b) => b.length - a.length);
        
        sortedQuotes.forEach(quote => {
            const cleanQuote = normalizeText(quote);
            const regex = new RegExp(cleanQuote, 'gi');
            let match;
            while ((match = regex.exec(text)) !== null) {
                matches.push({
                    start: match.index,
                    end: match.index + match[0].length,
                    type: 'stereotype',
                    text: match[0]
                });
            }
        });
    }
    
    if (data.turn_analysis && data.turn_analysis.anti_stereotype_quotes && data.turn_analysis.anti_stereotype_quotes.length > 0) {
        const sortedQuotes = [...data.turn_analysis.anti_stereotype_quotes]
            .map(quote => quote.replace(/^\d+\.\s*/, '').trim())
            .map(quote => quote.replace(/\s*\([^)]*\)/, '').trim())
            .sort((a, b) => b.length - a.length);
        
        sortedQuotes.forEach(quote => {
            const cleanQuote = normalizeText(quote);
            const regex = new RegExp(cleanQuote, 'gi');
            let match;
            while ((match = regex.exec(text)) !== null) {
                matches.push({
                    start: match.index,
                    end: match.index + match[0].length,
                    type: 'anti-stereotype',
                    text: match[0]
                });
            }
        });
    }
    
    matches.sort((a, b) => a.start - b.start);
    
    matches.reverse().forEach(match => {
        const before = text.slice(0, match.start);
        const after = text.slice(match.end);
        const className = match.type === 'stereotype' ? 'highlight-stereotype' : 'highlight-anti-stereotype';
        text = before + `<span class="${className}">${match.text}</span>` + after;
    });
    
    turnDiv.innerHTML = `
        <div class="font-semibold mb-2">${data.speaker}</div>
        <div class="whitespace-pre-wrap">${text}</div>
    `;
    
    turnDiv.addEventListener('click', () => {
        document.querySelectorAll('.dialogue-turn, .analysis-item').forEach(el => {
            el.classList.remove('elevated');
        });
        
        turnDiv.classList.add('elevated');
        
        const analysisItem = analysisContainer.children[turnDiv.dataset.turnIndex];
        if (analysisItem) {
            analysisItem.classList.add('elevated');
            analysisItem.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }
    });
    
    dialogueContainer.appendChild(turnDiv);
    dialogueContainer.scrollTop = dialogueContainer.scrollHeight;
}

function addAnalysisItem(data) {
    const analysisDiv = document.createElement('div');
    const hasStereotypes = data.turn_analysis.stereotype_quotes.length > 0;
    const isPersonaConsistent = data.turn_analysis.persona_consistency.toLowerCase().includes('consistent') || 
                              !data.turn_analysis.persona_consistency.toLowerCase().includes('inconsistent');
    
    analysisDiv.className = `analysis-item ${data.persona_id}`;
    analysisDiv.dataset.turnIndex = analysisContainer.children.length;
    analysisDiv.style.cursor = 'pointer';
    
    analysisDiv.innerHTML = `
        <div class="font-semibold mb-2">${data.speaker}'s Turn Analysis</div>
        <div class="text-sm space-y-4">
            <div>
                <p class="font-bold text-gray-800">Stereotype Analysis</p>
                <div class="mt-1 p-2 rounded ${hasStereotypes ? 'bg-red-50' : 'bg-green-50'}">
                    <p class="whitespace-pre-wrap">${data.turn_analysis.stereotype_analysis}</p>
                </div>
            </div>
            
            <div>
                <p class="font-bold text-gray-800">Persona Consistency</p>
                <div class="mt-1 p-2 rounded ${isPersonaConsistent ? 'bg-green-50' : 'bg-red-50'}">
                    <p class="whitespace-pre-wrap">${data.turn_analysis.persona_consistency}</p>
                </div>
            </div>
            
            <div>
                <p class="font-bold text-gray-800">Conversation Dynamics</p>
                <div class="mt-1 p-2 rounded bg-gray-50">
                    <p class="whitespace-pre-wrap">${data.turn_analysis.conversation_dynamics}</p>
                </div>
            </div>
        </div>
    `;
    
    analysisDiv.addEventListener('click', () => {
        document.querySelectorAll('.dialogue-turn, .analysis-item').forEach(el => {
            el.classList.remove('elevated');
        });
        
        analysisDiv.classList.add('elevated');
        
        const turnDiv = dialogueContainer.children[analysisDiv.dataset.turnIndex];
        if (turnDiv) {
            turnDiv.classList.add('elevated');
            turnDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }
    });
    
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
    const numTurns = parseInt(turnsInput.value) || 2;
    
    if (!categoryId || !scenarioId) {
        alert('Please select both a category and a scenario');
        return;
    }
    
    if (numTurns < 2) {
        alert('Number of turns must be at least 2');
        return;
    }
    
    dialogueContainer.innerHTML = '';
    analysisContainer.innerHTML = '';
    
    const existingMetadata = document.querySelector('.metadata-section');
    if (existingMetadata) {
        existingMetadata.remove();
    }
    
    isGenerating = true;
    updateGenerateButton();
    
    ws.send(JSON.stringify({
        category_id: categoryId,
        scenario_id: scenarioId,
        num_turns: numTurns
    }));
});

function addOverallAnalysis(statistics) {
    const overallDiv = document.createElement('div');
    overallDiv.className = 'overall-analysis';
    
    overallDiv.innerHTML = `
        <div class="bg-white rounded-lg shadow-md p-6">
            <h2 class="text-xl font-semibold mb-4">Overall Analysis</h2>
            <div class="loading-analysis">
                <div class="animate-pulse space-y-4">
                    <div class="h-4 bg-gray-200 rounded w-3/4"></div>
                    <div class="space-y-3">
                        <div class="grid grid-cols-2 gap-4">
                            <div class="h-20 bg-gray-200 rounded"></div>
                            <div class="h-20 bg-gray-200 rounded"></div>
                            <div class="h-20 bg-gray-200 rounded"></div>
                            <div class="h-20 bg-gray-200 rounded"></div>
                        </div>
                    </div>
                    <div class="h-4 bg-gray-200 rounded w-1/2"></div>
                    <div class="h-32 bg-gray-200 rounded"></div>
                    <div class="h-4 bg-gray-200 rounded w-2/3"></div>
                    <div class="h-32 bg-gray-200 rounded"></div>
                </div>
            </div>
        </div>
    `;
    
    const overallAnalysisContainer = document.getElementById('overallAnalysisContainer');
    overallAnalysisContainer.innerHTML = '';
    overallAnalysisContainer.appendChild(overallDiv);
}

function renderOverallAnalysis(overallDiv, statistics) {
    if (!overallDiv) return;
    
    const stats = statistics;
    
    const summaryHTML = `
        <div class="mb-6">
            <h3 class="text-lg font-semibold mb-3">Overall Dialogue Statistics</h3>
            <div class="grid grid-cols-2 gap-4">
                <div class="bg-gray-50 p-4 rounded-lg">
                    <p class="text-sm text-gray-600">Total Turns</p>
                    <p class="text-2xl font-bold">${stats.statistics.total_turns || 0}</p>
                </div>
                <div class="bg-gray-50 p-4 rounded-lg">
                    <p class="text-sm text-gray-600">Total Stereotypes</p>
                    <p class="text-2xl font-bold text-red-600">${stats.statistics.total_stereotypes || 0}</p>
                </div>
                <div class="bg-gray-50 p-4 rounded-lg">
                    <p class="text-sm text-gray-600">Anti-Stereotypes</p>
                    <p class="text-2xl font-bold text-green-600">${stats.statistics.total_anti_stereotypes || 0}</p>
                </div>
                <div class="bg-gray-50 p-4 rounded-lg">
                    <p class="text-sm text-gray-600">Stereotype Ratio</p>
                    <p class="text-2xl font-bold">${stats.statistics.total_turns ? (stats.statistics.total_stereotypes / stats.statistics.total_turns).toFixed(2) : '0.00'}</p>
                </div>
            </div>
        </div>
    `;
    
    const evolutionHTML = `
        <div class="mb-6">
            <h3 class="text-lg font-semibold mb-3">Stereotype Evolution</h3>
            <div class="bg-gray-50 p-4 rounded-lg">
                <div class="space-y-2">
                    ${(stats.evolution || []).map(ev => `
                        <div class="flex items-start">
                            <span class="w-16 text-sm">Turn ${ev.turn}:</span>
                            <div class="flex-1">
                                <div class="flex items-center mb-1">
                                    <span class="text-sm font-medium">Intensity: ${ev.intensity}/5</span>
                                    <div class="ml-2 w-24 bg-gray-200 rounded-full h-2">
                                        <div class="bg-indigo-600 h-2 rounded-full" style="width: ${ev.intensity * 20}%"></div>
                                    </div>
                                </div>
                                <p class="text-sm text-gray-600">${ev.note}</p>
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
        </div>
    `;
    
    const powerHTML = `
        <div class="mb-6">
            <h3 class="text-lg font-semibold mb-3">Power Dynamics</h3>
            <div class="bg-gray-50 p-4 rounded-lg">
                <div class="space-y-4">
                    ${Object.entries(stats.power_dynamics || {}).map(([speaker, data]) => `
                        <div>
                            <div class="flex justify-between items-center mb-1">
                                <span class="font-semibold">${speaker}</span>
                                <span class="text-sm text-gray-600">Influence: ${data.influence.toFixed(1)}</span>
                            </div>
                            <div class="w-full bg-gray-200 rounded-full h-2">
                                <div class="bg-indigo-600 h-2 rounded-full" style="width: ${data.influence * 20}%"></div>
                            </div>
                            <p class="text-sm text-gray-600 mt-1">${data.observation}</p>
                        </div>
                    `).join('')}
                </div>
            </div>
        </div>
    `;
    
    const crossHTML = `
        <div class="mb-6">
            <h3 class="text-lg font-semibold mb-3">Cross-Stereotype Analysis</h3>
            <div class="bg-gray-50 p-4 rounded-lg">
                <div class="grid grid-cols-2 gap-4">
                    ${(stats.cross_stereotypes || []).map(cross => `
                        <div class="border rounded p-3">
                            <div class="font-semibold text-sm mb-1">${cross.group1} + ${cross.group2}</div>
                            <p class="text-sm text-gray-600">${cross.interaction}</p>
                        </div>
                    `).join('')}
                </div>
            </div>
        </div>
    `;
    
    const targetedGroupsHTML = `
        <div class="mb-6">
            <h3 class="text-lg font-semibold mb-3">Targeted Groups Analysis</h3>
            <div class="bg-gray-50 p-4 rounded-lg">
                <div class="space-y-4">
                    ${Object.entries(stats.targeted_groups || {}).map(([group, data]) => `
                        <div class="border rounded p-3">
                            <div class="flex justify-between items-center mb-2">
                                <span class="font-semibold">${group}</span>
                                <span class="text-sm ${getSeverityColor(data.severity)}">${data.severity}</span>
                            </div>
                            <div class="flex justify-between text-sm text-gray-600 mb-2">
                                <span>Frequency: ${data.frequency}</span>
                            </div>
                            <p class="text-sm text-gray-600">${data.observation}</p>
                        </div>
                    `).join('')}
                </div>
            </div>
        </div>
    `;
    
    const severityHTML = `
        <div class="mb-6">
            <h3 class="text-lg font-semibold mb-3">Severity Analysis</h3>
            <div class="bg-gray-50 p-4 rounded-lg">
                <div class="space-y-3">
                    ${(stats.severity_analysis || []).map(sev => `
                        <div class="flex items-start">
                            <span class="w-16 text-sm">Turn ${sev.turn}:</span>
                            <div class="flex-1">
                                <div class="flex items-center">
                                    <span class="text-sm font-medium ${getSeverityColor(sev.severity)}">${sev.severity}</span>
                                </div>
                                <p class="text-sm text-gray-600">${sev.justification}</p>
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
        </div>
    `;
    
    const mitigationHTML = `
        <div class="mb-6">
            <h3 class="text-lg font-semibold mb-3">Mitigation Effectiveness</h3>
            <div class="bg-gray-50 p-4 rounded-lg">
                <div class="space-y-3">
                    ${(stats.mitigation_effectiveness || []).map(mit => `
                        <div class="flex items-start">
                            <span class="w-16 text-sm">Turn ${mit.turn}:</span>
                            <div class="flex-1">
                                <div class="flex items-center">
                                    <span class="text-sm font-medium">${mit.challenge}</span>
                                    <span class="ml-2">${mit.success ? '✅' : '❌'}</span>
                                </div>
                                <p class="text-sm text-gray-600">${mit.outcome}</p>
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
        </div>
    `;
    
    const narrativeHTML = `
        <div class="mb-6">
            <h3 class="text-lg font-semibold mb-3">Narrative Summary</h3>
            <div class="bg-gray-50 p-4 rounded-lg">
                <p class="text-gray-700">${stats.narrative_summary || ''}</p>
            </div>
        </div>
    `;
    
    overallDiv.innerHTML = `
        <div class="bg-white rounded-lg shadow-md p-6">
            <h2 class="text-xl font-semibold mb-4">Overall Analysis</h2>
            ${summaryHTML}
            ${evolutionHTML}
            ${powerHTML}
            ${crossHTML}
            ${targetedGroupsHTML}
            ${severityHTML}
            ${mitigationHTML}
            ${narrativeHTML}
        </div>
    `;
}

function getSeverityColor(severity) {
    switch (severity.toLowerCase()) {
        case 'severe':
            return 'text-red-600';
        case 'moderate':
            return 'text-yellow-600';
        case 'mild':
            return 'text-green-600';
        default:
            return 'text-gray-600';
    }
}

function generateSparkline(evolution) {
    const maxIntensity = Math.max(...evolution.map(e => e.intensity));
    const points = evolution.map(e => (e.intensity / maxIntensity) * 100);
    
    const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svg.setAttribute("width", "100%");
    svg.setAttribute("height", "100%");
    svg.setAttribute("viewBox", "0 0 100 20");
    
    const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
    const d = points.map((p, i) => 
        `${i === 0 ? 'M' : 'L'} ${(i / (points.length - 1)) * 100} ${100 - p}`
    ).join(' ');
    
    path.setAttribute("d", d);
    path.setAttribute("fill", "none");
    path.setAttribute("stroke", "#4f46e5");
    path.setAttribute("stroke-width", "2");
    
    svg.appendChild(path);
    return svg.outerHTML;
}

document.addEventListener('DOMContentLoaded', () => {
    initWebSocket();
    loadScenarios();
    generateBtn.disabled = true;
}); 