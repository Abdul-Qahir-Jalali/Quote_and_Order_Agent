// Basic Interactivity
document.addEventListener('DOMContentLoaded', () => {

    /* --- Chat Integration --- */
    const chatInput = document.getElementById('chatInput');
    const sendBtn = document.getElementById('sendMessage');
    const chatBody = document.getElementById('chatBody');
    const toggleChat = document.getElementById('toggleChat');
    const chatWidget = document.querySelector('.chat-widget');
    
    // Generate a random session ID
    const sessionId = 'sess_' + Math.random().toString(36).substr(2, 9);
    
    function appendMessage(text, isUser) {
        const div = document.createElement('div');
        div.classList.add('message');
        div.classList.add(isUser ? 'user-message' : 'bot-message');
        
        if (isUser) {
            div.textContent = text;
        } else {
            // Check if marked is available, otherwise fallback
            if (typeof marked !== 'undefined') {
                div.innerHTML = marked.parse(text);
            } else {
                div.textContent = text;
            }
        }
        
        chatBody.appendChild(div);
        return div; // Return element for scrolling control
    }

    function scrollToBottom() {
        chatBody.scrollTop = chatBody.scrollHeight;
    }

    async function sendMessage() {
        const text = chatInput.value.trim();
        if (!text) return;
        
        appendMessage(text, true);
        chatInput.value = '';
        scrollToBottom(); // User message always goes to bottom
        
        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: text, session_id: sessionId })
            });

            const data = await response.json();
            
            // Handle Actions
            let msgDiv = null;
            if (data.response) {
                msgDiv = appendMessage(data.response, false);
            }
            
            if (data.show_form) {
                const mode = data.meta ? (data.meta.form_mode || 'edit') : 'edit';
                renderChatForm(data.state, mode);
                // If we have a text message, scroll to it so user reads from top
                if (msgDiv) {
                    msgDiv.scrollIntoView({ behavior: 'smooth', block: 'start' });
                } else {
                    scrollToBottom();
                }
            } else {
                // Normal text response
                scrollToBottom();
            }

            if (data.error) {
                appendMessage("Error: " + data.error, false);
                scrollToBottom();
            }

        } catch (err) {
            console.error(err);
            appendMessage("Sorry, something went wrong.", false);
            scrollToBottom();
        }
    }

    function renderChatForm(prefillData = {}, mode = 'edit') {
        const formDiv = document.createElement('div');
        formDiv.className = "chat-form-container";
        
        // Safety check for nulls
        const safe = (val) => val || "";
        
        // Get product interest value
        const pInterest = safe(prefillData.product_interest);
        
        // Check if we have a valid known product to lock
        const knownProducts = ['The Cloud Sofa', 'Classic Chesterfield', 'Artisan Oak Table', 'Velvet Armchair'];
        const isLocked = knownProducts.includes(pInterest);
        
        // Helper to check if product is selected
        const isSelected = (prod) => pInterest === prod ? 'selected' : '';

        let productHtml = '';
        if (isLocked) {
             // Render Read-Only Input
             productHtml = `<input type="text" id="cf_product" value="${pInterest}" readonly style="background-color: #e9ecef; cursor: not-allowed; font-weight: bold; color: #555;">`;
        } else {
             // Render Dropdown (Fallback)
             productHtml = `
                <select id="cf_product">
                    <option value="" disabled ${!pInterest ? 'selected' : ''}>Select Product</option>
                    <option value="The Cloud Sofa" ${isSelected('The Cloud Sofa')}>The Cloud Sofa</option>
                    <option value="Classic Chesterfield" ${isSelected('Classic Chesterfield')}>Classic Chesterfield</option>
                    <option value="Artisan Oak Table" ${isSelected('Artisan Oak Table')}>Artisan Oak Table</option>
                    <option value="Velvet Armchair" ${isSelected('Velvet Armchair')}>Velvet Armchair</option>
                    <option ${!knownProducts.includes(pInterest) && pInterest ? 'selected value="'+pInterest+'"' : ''}>${!knownProducts.includes(pInterest) && pInterest ? pInterest : 'Other'}</option>
                </select>`;
        }

        const btnText = mode === 'confirm' ? "Confirm Order" : "Send Details";
        const btnClass = mode === 'confirm' ? "btn-confirm" : ""; // Add style hook if needed
        const isConfirm = mode === 'confirm';

        formDiv.innerHTML = `
            <div class="chat-form">
                <input type="text" id="cf_name" placeholder="Full Name" value="${safe(prefillData.full_name)}">
                <input type="email" id="cf_email" placeholder="Email" value="${safe(prefillData.email)}">
                <input type="tel" id="cf_phone" placeholder="Phone" value="${safe(prefillData.phone)}">
                <input type="text" id="cf_address" placeholder="Address" value="${safe(prefillData.address)}">
                ${productHtml}
                <input type="number" id="cf_qty" placeholder="Qty" value="${prefillData.quantity || 1}">
                <button onclick="submitChatForm(this, ${isConfirm})" class="${btnClass}">${btnText}</button>
            </div>
        `;
        chatBody.appendChild(formDiv);
        // Note: No auto-scroll here anymore
    }

    // Expose this function globally so the HTML button can call it
    window.submitChatForm = async function(btn, isConfirmation = false) {
        console.log("Submit button clicked. Mode Confirm:", isConfirmation);
        const parent = btn.parentElement;
        if (!parent) return;

        try {
            const getVal = (id) => {
                const el = parent.querySelector(id);
                return el ? el.value : '';
            };

            const details = {
                full_name: getVal('#cf_name'),
                email: getVal('#cf_email'),
                phone: getVal('#cf_phone'),
                address: getVal('#cf_address'),
                product_interest: getVal('#cf_product'),
                quantity: parseInt(getVal('#cf_qty')) || 1
            };
            
            // Add confirmation flag if applicable
            if (isConfirmation) {
                details.confirmed = true;
            }

            // Disable form
            btn.disabled = true;
            btn.textContent = isConfirmation ? "Confirmed!" : "Sent!";
            
            const jsonMsg = "Here are my details: ```json" + JSON.stringify(details) + "```";
            
            appendMessage("📝 Form Submitted", true);
            scrollToBottom();
            
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: jsonMsg, session_id: sessionId })
            });

            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

            const data = await response.json();
            
            let msgDiv = null;
            if (data.response) {
                msgDiv = appendMessage(data.response, false);
            }

            if (data.show_form) {
                // Check if we are in confirm mode
                const mode = data.meta ? (data.meta.form_mode || 'edit') : 'edit';
                renderChatForm(data.state, mode);
                
                // CRITICAL FIX: Scroll to top of message so user sees errors
                if (msgDiv) {
                    msgDiv.scrollIntoView({ behavior: 'smooth', block: 'start' });
                } else {
                    scrollToBottom();
                }
            } else {
                scrollToBottom();
            }
        } catch(e) { 
            console.error("Submission Error:", e);
            btn.disabled = false;
            btn.textContent = "Try Again";
            appendMessage("Error submitting form. Please try again.", false);
            scrollToBottom();
        }
    };

    sendBtn.addEventListener('click', sendMessage);
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });

    // Make chat collapsible
    let isOpen = true;
    toggleChat.addEventListener('click', () => {
        if (isOpen) {
            chatWidget.style.bottom = "-440px"; // Hide body
            toggleChat.textContent = "+";
        } else {
            chatWidget.style.bottom = "20px";
            toggleChat.textContent = "−";
        }
        isOpen = !isOpen;
    });

    /* --- Legacy Form Handler --- */
    const legacyForm = document.getElementById('legacyForm');
    if (legacyForm) {
        legacyForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            alert("This is the legacy form. The goal is to use the Chatbot instead!");
        });
    }
});
