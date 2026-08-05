// =======================================
// GAICA - AI Chatbot JavaScript
// =======================================

console.log("GAICA Chatbot Loaded");

// Escape user input to prevent XSS
function escapeHTML(str) {
    let div = document.createElement("div");
    div.textContent = str;
    return div.innerHTML;
}

// Send Message
function sendMessage() {

    let input = document.getElementById("userInput");
    let chatBox = document.getElementById("chatBox");

    let message = input.value.trim();

    if (message === "") {
        alert("Please enter a message.");
        return;
    }

    let safeMessage = escapeHTML(message);

    // User Message
    chatBox.insertAdjacentHTML("beforeend", `
        <div class="user-message">
            <b>You:</b> ${safeMessage}
        </div>
    `);

    // AI Reply
    let reply = getBotReply(message);

    chatBox.insertAdjacentHTML("beforeend", `
        <div class="bot-message">
            <b>GAICA AI:</b> ${reply}
        </div>
    `);

    input.value = "";

    chatBox.scrollTop = chatBox.scrollHeight;
}

// Send message on Enter key press
document.addEventListener("DOMContentLoaded", function () {
    let input = document.getElementById("userInput");
    if (input) {
        input.addEventListener("keypress", function (e) {
            if (e.key === "Enter") {
                sendMessage();
            }
        });
    }
});

// Basic AI Reply
function getBotReply(message) {

    message = message.toLowerCase();

    if (message.includes("hello") || message.includes("hi")) {
        return "Hello! Welcome to GAICA.";
    }

    if (message.includes("scam")) {
        return "Please open the Scam Detection page to analyze suspicious messages.";
    }

    if (message.includes("fake news")) {
        return "You can verify news in the Fake News section.";
    }

    if (message.includes("emergency")) {
        return "Please visit the Emergency section for immediate assistance.";
    }

    if (message.includes("help")) {
        return "I am here to help you with crisis management.";
    }

    return "Sorry, I don't understand. AI integration will be added soon.";
}

// Clear Chat
function clearChat() {

    document.getElementById("chatBox").innerHTML = "";
}