import sqlite3
from flask import Flask, request, render_template

app = Flask(__name__)







# --- Set up the database once, when the app starts ---
def init_db():
    conn = sqlite3.connect("emails.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS signups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

init_db()


def print_all_records():
    conn = sqlite3.connect("emails.db")
    rows = conn.execute("SELECT * FROM signups").fetchall()
    conn.close()

    if not rows:
        print("No records yet.")
        return

    print(f"{len(rows)} record(s):\n")
    for row in rows:
        print(row)


# --- Serve the landing page ---
@app.route("/")
def home():
    return render_template("frontend.html")

# --- Receive an email and store it ---
@app.route("/register", methods=["POST"])
def register():

    data = request.get_json()
    email = data["email"].strip().lower()
    print_all_records()

    if not email or "@" not in email:
        return {"status": "error", "message": "Invalid email"}, 400

    try:
        conn = sqlite3.connect("emails.db")
        conn.execute("INSERT INTO signups (email) VALUES (?)", (email,))
        conn.commit()
        conn.close()
    except sqlite3.IntegrityError:
        return {"status": "ok", "message": "Already registered"}
    return {"status": "ok", "message": "Registered"}






if __name__ == "__main__":
    app.run(debug=True)