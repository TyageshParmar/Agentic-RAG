document.addEventListener('DOMContentLoaded', () => {
    const chatContainer = document.getElementById('chatContainer');
    const queryInput = document.getElementById('queryInput');
    const sendBtn = document.getElementById('sendBtn');

    // Auto-resize textarea
    queryInput.addEventListener('input', function () {
        this.style.height = 'auto';
        const newHeight = Math.min(this.scrollHeight, 120);
        this.style.height = newHeight + 'px';

        // Enable/disable send button based on content
        sendBtn.disabled = this.value.trim() === '';
    });

    // Handle Enter key (send on Enter, newline on Shift+Enter)
    queryInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    sendBtn.addEventListener('click', sendMessage);

    // Provide globally so sidebar can click it
    window.setQuery = function (text) {
        queryInput.value = text;
        queryInput.dispatchEvent(new Event('input'));
        sendMessage();

        // On mobile, close sidebar or focus input
        if (window.innerWidth <= 900) {
            queryInput.focus();
        }
    };

    function appendUserMessage(text) {
        const msgDiv = document.createElement('div');
        msgDiv.className = 'message user-message';
        msgDiv.innerHTML = `
            <div class="avatar bg-purple">👤</div>
            <div class="message-content">${escapeHTML(text)}</div>
        `;
        chatContainer.appendChild(msgDiv);
        scrollToBottom();
    }

    function appendBotLoading() {
        const msgDiv = document.createElement('div');
        msgDiv.className = 'message bot-message loading-msg';
        msgDiv.id = 'loadingMessage';
        msgDiv.innerHTML = `
            <div class="avatar bg-blue">🤖</div>
            <div class="typing-indicator">
                <div class="dot"></div>
                <div class="dot"></div>
                <div class="dot"></div>
            </div>
        `;
        chatContainer.appendChild(msgDiv);
        scrollToBottom();
        return msgDiv;
    }

    function removeBotLoading() {
        const loadingMsg = document.getElementById('loadingMessage');
        if (loadingMsg) {
            loadingMsg.remove();
        }
    }

    function escapeHTML(str) {
        if (!str) return '';
        return str.replace(/[&<>'"]/g,
            tag => ({
                '&': '&amp;',
                '<': '&lt;',
                '>': '&gt;',
                "'": '&#39;',
                '"': '&quot;'
            }[tag] || tag)
        );
    }

    function appendBotResponse(data, isError = false) {
        const msgDiv = document.createElement('div');
        msgDiv.className = 'message bot-message';

        if (isError) {
            msgDiv.innerHTML = `
                <div class="avatar bg-blue">🤖</div>
                <div class="message-content error-msg">
                    <p>❌ ${escapeHTML(data)}</p>
                </div>
            `;
        } else {
            // Build the agentic sub-steps HTML
            let stepsHTML = '';

            // Planner Step
            let plannerList = '';
            if (data.plan && data.plan.sections_to_search && data.plan.sections_to_search.length > 0) {
                plannerList = data.plan.sections_to_search.map(s => `<li>${escapeHTML(s)}</li>`).join('');
            }
            stepsHTML += `
                <div class="agent-step">
                    <div class="step-header">🧠 Planner Agent</div>
                    <div class="step-content">
                        <p><strong>Intent:</strong> Analysis / Info</p>
                        ${plannerList ? `<p><strong>Target Sections:</strong></p><ul>${plannerList}</ul>` : ''}
                    </div>
                </div>
            `;

            // Retriever Step
            let retrieverList = '';
            if (data.retrieval_passages && data.retrieval_passages.length > 0) {
                retrieverList = data.retrieval_passages.map(p => `
                    <div class="passage-small">
                        <strong>${escapeHTML(p.section || 'Unknown')}</strong> (Score: ${(p.score || 0).toFixed(3)})<br>
                        <span style="font-size:0.8em; opacity:0.8">${escapeHTML(p.text).substring(0, 150)}...</span>
                    </div>
                `).join('');
            } else {
                retrieverList = '<p>No passages retrieved.</p>';
            }
            stepsHTML += `
                <div class="agent-step">
                    <div class="step-header">🔍 Retrieval Agent (${data.retrieval_passages?.length || 0} hits)</div>
                    <div class="step-content">
                        ${retrieverList}
                    </div>
                </div>
            `;

            // Synthesizer Step
            const evidenceLines = (data.evidence_text || '').split('\n').filter(l => l.trim()).map(l => escapeHTML(l)).join('<br>');
            stepsHTML += `
                <div class="agent-step">
                    <div class="step-header">🧩 Synthesis Agent</div>
                    <div class="step-content" style="font-family:monospace; white-space:pre-wrap; font-size: 0.8em;">${evidenceLines || 'No evidence synthesized.'}</div>
                </div>
            `;

            msgDiv.innerHTML = `
                <div class="avatar bg-blue">🤖</div>
                <div class="message-content markdown-body">
                    ${marked.parse(data.final_answer || "Sorry, I couldn't generate an answer.")}
                    <div class="agent-details">
                        ${stepsHTML}
                    </div>
                </div>
            `;
        }

        chatContainer.appendChild(msgDiv);
        bindAccordions(msgDiv);
        scrollToBottom();
    }

    function bindAccordions(container) {
        const headers = container.querySelectorAll('.step-header');
        headers.forEach(header => {
            header.addEventListener('click', () => {
                header.classList.toggle('open');
                const content = header.nextElementSibling;
                content.classList.toggle('open');
                scrollToBottom();
            });
        });
    }

    function scrollToBottom() {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    async function sendMessage() {
        const query = queryInput.value.trim();
        if (!query) return;

        // UI changes
        appendUserMessage(query);
        queryInput.value = '';
        queryInput.style.height = 'auto';
        sendBtn.disabled = true;

        appendBotLoading();

        try {
            const response = await fetch('https://your-username-your-space-name.hf.space/api/query', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ query: query })
            });

            removeBotLoading();

            if (!response.ok) {
                const errData = await response.json();
                throw new Error(errData.detail || 'Failed to fetch response from API');
            }

            const data = await response.json();
            appendBotResponse(data);

        } catch (error) {
            removeBotLoading();
            appendBotResponse(error.message, true);
        }
    }
});

