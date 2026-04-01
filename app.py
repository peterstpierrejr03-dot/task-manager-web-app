from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect("tasks.db")
    conn.row_factory = sqlite3.Row
    return conn

conn = get_db_connection()
conn.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT NOT NULL
)
""")
conn.close()

@app.route("/", methods=["GET", "POST"])
def home():
    conn = get_db_connection()

    if request.method == "POST":
        task = request.form["task"]
        conn.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
        conn.commit()

    tasks = conn.execute("SELECT * FROM tasks").fetchall()
    conn.close()

    return render_template("index.html", tasks=tasks)

@app.route("/delete/<int:id>")
def delete(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM tasks WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
