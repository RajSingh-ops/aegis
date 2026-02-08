document.addEventListener('DOMContentLoaded', function() {
    const logContainer = document.getElementById('log-container');
    const thoughtContainer = document.getElementById('thought-stream');
    const inputField = document.getElementById('audit-input');
    const sendBtn = document.getElementById('send-btn');
    const statusDot = document.querySelector('.pulse');
    const statusText = document.querySelector('.status-indicator span');

    // WebSocket Connection
    // Note: Assuming port 8001 as per current server run, but ideally dynamic or 8000
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const auditSocket = new WebSocket(`${protocol}//${window.location.host}/ws/auditor/`);

    auditSocket.onopen = function(e) {
        console.log('Aegis Auditor Connected');
        statusText.innerText = "ACTIVE - MONITORING";
        statusDot.style.backgroundColor = "var(--accent-success)";
    };

    auditSocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
        statusText.innerText = "OFFLINE";
        statusDot.style.backgroundColor = "var(--accent-danger)";
        statusDot.style.animation = "none";
    };

    auditSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        console.log("Received:", data);

        if (data.type === 'audit_response') {
            appendLog(data.message, data.thought_signature);
        }
    };

    function sendMessage() {
        const message = inputField.value;
        if (message.trim() === "") return;

        auditSocket.send(JSON.stringify({
            'message': message
        }));
        
        // Optimistic UI update (optional, but good for chat feel)
        // appendLog(`User: ${message}`, null, true);
        
        inputField.value = '';
    }

    sendBtn.onclick = sendMessage;
    inputField.onkeyup = function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    };

    function appendLog(message, thoughtSignature, isUser = false) {
        const entry = document.createElement('div');
        entry.className = 'log-entry';
        
        const timestamp = new Date().toLocaleTimeString();
        
        let contentHtml = `
            <span class="log-timestamp">${timestamp}</span>
            <div class="log-content">${message}</div>
        `;

        if (thoughtSignature) {
            contentHtml += `<div class="thought-bubble">🧠 Thought Sig: ${thoughtSignature}</div>`;
        }

        // Simple heuristic for styling warnings
        if (message.includes("violation") || message.includes("High")) {
            entry.classList.add('high-severity');
        }

        entry.innerHTML = contentHtml;
        logContainer.prepend(entry); // Newest on top
    }
});
