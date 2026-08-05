// ====================================
// GAICA - Global Agentic AI Crisis Assistant
// Main JavaScript
// ====================================

console.log("GAICA Loaded Successfully");

// Welcome Message
window.addEventListener("load", function () {
    console.log("Welcome to GAICA");
});

// Get Started Button
function getStarted() {
    window.location.href = "/register";
}

// Login Button
function loginPage() {
    window.location.href = "/login";
}

// AI Chat
function openChat() {
    window.location.href = "/chat";
}

// Emergency
function openEmergency() {
    window.location.href = "/emergency";
}

// Smooth Scroll
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener("click", function (e) {
        e.preventDefault();

        const target = document.querySelector(this.getAttribute("href"));

        if (target) {
            target.scrollIntoView({
                behavior: "smooth"
            });
        }
    });
});

// Button Hover Effect
const buttons = document.querySelectorAll("button");

buttons.forEach(function(button) {

    button.addEventListener("mouseover", function () {
        button.style.transform = "scale(1.05)";
    });

    button.addEventListener("mouseout", function () {
        button.style.transform = "scale(1)";
    });

});

// Footer Year
const footer = document.querySelector("footer h3");

if (footer) {
    footer.innerHTML = "GAICA © " + new Date().getFullYear();
}

console.log("Main.js Loaded Successfully");