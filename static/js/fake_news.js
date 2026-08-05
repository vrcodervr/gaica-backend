// =======================================
// GAICA - Fake News Detection JavaScript
// =======================================

console.log("Fake News Module Loaded");

// Analyze News
function analyzeNews() {

    let news = document.getElementById("newsInput").value.trim();
    let result = document.getElementById("result");

    if (news === "") {
        result.innerHTML = "⚠ Please enter a news headline or article.";
        result.style.color = "orange";
        return;
    }

    let text = news.toLowerCase();

    if (
        text.includes("breaking") ||
        text.includes("shocking") ||
        text.includes("100% true") ||
        text.includes("forward this") ||
        text.includes("viral")
    ) {

        result.innerHTML =
            "⚠ This news contains suspicious keywords. Please verify it before sharing.";

        result.style.color = "red";

    } else {

        result.innerHTML =
            "✅ No suspicious keywords found. This does not guarantee the news is true.";

        result.style.color = "green";
    }

}

// Clear Text
function clearNews() {

    document.getElementById("newsInput").value = "";
    document.getElementById("result").innerHTML = "";

}