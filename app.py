from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

# Database connection
def get_db():
    conn = sqlite3.connect("quiz.db")
    conn.row_factory = sqlite3.Row
    return conn

# Home/Login
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username=? AND password=?",
                          (username, password)).fetchone()

        if user:
            session["user"] = username
            return redirect("/quiz")
        else:
            return "Invalid Login"

    return render_template("login.html")


# Register
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        db = get_db()
        db.execute("INSERT INTO users(username, password) VALUES(?, ?)",
                   (username, password))
        db.commit()
        return redirect("/")

    return render_template("register.html")


# Quiz Page
@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    db = get_db()
    questions = db.execute("SELECT * FROM questions").fetchall()

    if request.method == "POST":
        score = 0
        for q in questions:
            selected = request.form.get(str(q["id"]))
            if selected == q["answer"]:
                score += 1

        return render_template("result.html", score=score, total=len(questions))

    return render_template("quiz.html", questions=questions)


# Run App
if __name__ == "__main__":
    app.run(debug=True)