const API_BASE_URL = '/api';

// DOM elements
const chatMessages = document.getElementById('chatMessages');
const userInput = document.getElementById('userInput');
const sendButton = document.getElementById('sendButton');
const typingIndicator = document.getElementById('typingIndicator');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    userInput.focus();
    
    // Send on Enter key
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    
    // Send button click
    sendButton.addEventListener('click', sendMessage);
});

function getCurrentTime() {
    const now = new Date();
    return now.toLocaleTimeString('en-US', { 
        hour: '2-digit', 
        minute: '2-digit' 
    });
}

function addMessage(content, isUser = false, confidence = null) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    const p = document.createElement('p');
    p.textContent = content;
    contentDiv.appendChild(p);
    
    // Add confidence badge for bot messages
    if (!isUser && confidence !== null && confidence > 0) {
        const badge = document.createElement('div');
        badge.className = 'confidence-badge';
        badge.textContent = `Confidence: ${(confidence * 100).toFixed(1)}%`;
        contentDiv.appendChild(badge);
    }
    
    const timeDiv = document.createElement('div');
    timeDiv.className = 'message-time';
    timeDiv.textContent = getCurrentTime();
    
    messageDiv.appendChild(contentDiv);
    messageDiv.appendChild(timeDiv);
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function showTypingIndicator() {
    typingIndicator.classList.add('active');
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function hideTypingIndicator() {
    typingIndicator.classList.remove('active');
}

function setInputEnabled(enabled) {
    userInput.disabled = !enabled;
    sendButton.disabled = !enabled;
    if (enabled) {
        userInput.focus();
    }
}

async function sendMessage() {
    const question = userInput.value.trim();
    
    if (!question) {
        return;
    }
    
    // Add user message to chat
    addMessage(question, true);
    userInput.value = '';
    
    // Disable input while processing
    setInputEnabled(false);
    showTypingIndicator();
    
    try {
        const response = await fetch(`${API_BASE_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ question: question }),
        });
        
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({ detail: 'Unknown error' }));
            throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Add bot response
        addMessage(data.answer, false, data.confidence);
        
    } catch (error) {
        console.error('Error:', error);
        addMessage(
            `Sorry, I encountered an error: ${error.message}. Please try again.`,
            false
        );
    } finally {
        hideTypingIndicator();
        setInputEnabled(true);
    }
}

