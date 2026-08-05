// =======================================
// GAICA - Emergency JavaScript
// =======================================

console.log("Emergency Module Loaded");

// Escape user input to prevent XSS
function escapeHTML(str) {
    let div = document.createElement("div");
    div.textContent = str;
    return div.innerHTML;
}

// Send Emergency Alert
function sendEmergency() {

    let name = document.getElementById("name").value.trim();
    let location = document.getElementById("location").value.trim();
    let emergency = document.getElementById("emergency").value;
    let result = document.getElementById("result");

    if (name === "" || location === "") {
        result.innerHTML = "⚠ Please fill all required fields.";
        result.style.color = "orange";
        return;
    }

    let safeName = escapeHTML(name);
    let safeLocation = escapeHTML(location);
    let safeEmergency = escapeHTML(emergency);

    result.innerHTML =
        "🚨 Emergency Alert Sent Successfully!<br><br>" +
        "<b>Name:</b> " + safeName + "<br>" +
        "<b>Location:</b> " + safeLocation + "<br>" +
        "<b>Emergency:</b> " + safeEmergency;

    result.style.color = "green";
}

// Clear Form
function clearEmergency() {

    document.getElementById("name").value = "";
    document.getElementById("location").value = "";
    document.getElementById("emergency").selectedIndex = 0;
    document.getElementById("result").innerHTML = "";
}

// Current Date & Time
window.addEventListener("load", function () {

    let now = new Date();

    let date = now.toLocaleDateString();
    let time = now.toLocaleTimeString();

    let datetime = document.getElementById("datetime");

    if (datetime) {
        datetime.innerHTML =
            "Date: " + date + " | Time: " + time;
    }

});