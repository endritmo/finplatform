/**
 * chat.js — AI chat widget logic.
 * Nginx proxies /ai/ask/ → backend:8000/ai/ask/ so no port is needed.
 */
document.addEventListener('DOMContentLoaded', () => {
    const toggleBtn = document.getElementById('ai-toggle-btn');
    const modal     = document.getElementById('ai-chat-modal');
    const closeBtn  = document.getElementById('close-chat');
    const sendBtn   = document.getElementById('send-btn');
    const chatInput = document.getElementById('chat-input');
    const chatBody  = document.getElementById('chat-body');

    if (!toggleBtn) return; // widget not present on this page

    toggleBtn.addEventListener('click', () => modal.classList.toggle('hidden'));
    closeBtn.addEventListener('click',  () => modal.classList.add('hidden'));

    const sendMessage = async () => {
        const text = chatInput.value.trim();
        if (!text) return;

        appendMessage(text, 'user');
        chatInput.value = '';
        const loadingEl = appendMessage('Analyzing market data…', 'bot');

        try {
            // /ai/ask/ is proxied by Nginx to backend — no hardcoded port.
            const response = await fetch('/ai/ask/', {
                method:  'POST',
                headers: { 'Content-Type': 'application/json' },
                body:    JSON.stringify({ message: text }),
            });
            const data = await response.json();
            loadingEl.remove();
            appendMessage(data.response || data.message, 'bot');
        } catch (err) {
            loadingEl.remove();
            appendMessage('Error connecting to AI service.', 'bot');
        }
        chatBody.scrollTop = chatBody.scrollHeight;
    };

    function linkify(text) {
        return text.replace(/(https?:\/\/[^\s]+)/g,
            (url) => `<a href="${url}" target="_blank" rel="noopener noreferrer" style="color:#4ea1ff;text-decoration:underline">🔗 Source</a>`
        );
    }

    function appendMessage(text, sender) {
        const div = document.createElement('div');
        div.classList.add('message', sender);
        div.innerHTML = linkify(text).replace(/\n/g, '<br>');
        chatBody.appendChild(div);
        chatBody.scrollTop = chatBody.scrollHeight;
        return div;
    }

    sendBtn.addEventListener('click', sendMessage);
    chatInput.addEventListener('keypress', (e) => { if (e.key === 'Enter') sendMessage(); });
});
