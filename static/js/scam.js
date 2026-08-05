// =======================================
// GAICA - Scam Detection JavaScript
// =======================================

console.log("Scam Detection Module Loaded");

// Scam Detection Function
function detectScam() {

    let input = document.getElementById("scamInput").value.trim();

    let result = document.getElementById("result");

    if (input === "") {
        result.innerHTML = "⚠ Please enter a message or URL.";
        result.style.color = "orange";
        return;
    }

    let text = input.toLowerCase();

    if (
        text.includes("otp") ||
        text.includes("bank") ||
        text.includes("verify") ||
        text.includes("prize") ||
        text.includes("lottery") ||
        text.includes("click here") ||
        text.includes("upi") ||
        text.includes("password")
    ) {

        result.innerHTML = "🚨 Warning! This message may be a Scam.";
        result.style.color = "red";

    } else {

        result.innerHTML = "✅ No obvious scam keywords found.";
        result.style.color = "green";
    }

}

// Clear Function
function clearScam() {

    document.getElementById("scamInput").value = "";

    document.getElementById("result").innerHTML = "";

}