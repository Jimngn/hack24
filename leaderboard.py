from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Initialize the database
def init_db():
    conn = sqlite3.connect("leaderboard.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS leaderboard (id INTEGER PRIMARY KEY, name TEXT, score INTEGER)")
    conn.commit()
    conn.close()

@app.route("/leaderboard", methods=["GET"])
def get_leaderboard():
    conn = sqlite3.connect("leaderboard.db")
    c = conn.cursor()
    c.execute("SELECT name, score FROM leaderboard ORDER BY score DESC LIMIT 10")
    scores = [{"name": row[0], "score": row[1]} for row in c.fetchall()]
    conn.close()
    return jsonify(scores)

@app.route("/leaderboard", methods=["POST"])
def add_score():
    name = request.json.get("name")
    score = request.json.get("score")
    conn = sqlite3.connect("leaderboard.db")
    c = conn.cursor()
    c.execute("INSERT INTO leaderboard (name, score) VALUES (?, ?)", (name, score))
    conn.commit()
    conn.close()
    return jsonify({"message": "Score added successfully"}), 201

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
