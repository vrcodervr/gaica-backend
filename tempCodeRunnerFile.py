from flask import Flask, render_template, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "gaica_secret_key"

# ---------------- Home ---------------- #

@app.route("/")
def home():
    return render_template("index.html")

# ---------------- Login ---------------- #

@app.route("/login")
def login():
    return render_template("login.html")

# ---------------- Register ---------------- #

@app.route("/register")
def register():
    return render_template("register.html")

# ---------------- Dashboard ---------------- #

@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect(url_for("login"))

    return render_template("dashboard.html")

# ---------------- Logout ---------------- #

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("home"))

# ---------------- AI Chat ---------------- #

@app.route("/chat")
def chat():

    if "user" not in session:
        return redirect(url_for("login"))

    return render_template("chatbot.html")

# ---------------- Scam Detection ---------------- #

@app.route("/scam")
def scam():

    if "user" not in session:
        return redirect(url_for("login"))

    return render_template("scam.html")

# ---------------- Fake News ---------------- #

@app.route("/fake-news")
def fake_news():

    if "user" not in session:
        return redirect(url_for("login"))

    return render_template("fake_news.html")

# ---------------- Emergency ---------------- #

@app.route("/emergency")
def emergency():

    if "user" not in session:
        return redirect(url_for("login"))

    return render_template("emergency.html")

# ---------------- Admin ---------------- #

@app.route("/admin")
def admin():

    return render_template("admin.html")

# ---------------- Main ---------------- #

if __name__ == "__main__":
    app.run(debug=True)