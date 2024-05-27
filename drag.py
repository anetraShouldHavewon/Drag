'''My Project'''
from flask import Flask, render_template
import sqlite3
connection = sqlite3.connect("drag_queen.db")
cursor = connection.cursor()

app = Flask(__name__)
@app.route("/home")
def home():
    return render_template("drag_queens.html", title = "Drag Queens")

@app.route("/seasons")
def seasons():
    return render_template("drag_queens.html", title = "Drag Queens")

@app.route("/season_info")
def season_info():
    return render_template("drag_queens.html", title = "Drag Queens")

@app.route("/drag_queens")
def drag_queens():
    return render_template("drag_queens.html", title = "Drag Queens")

@app.route("/drag_queen_info/<int:id>")
def drag_queen_info(id):
    drag_queen_info = cursor.execute("SELECT * FROM Drag_Queens WHERE id = ?", (id,))
    print(drag_queen_info)
    return render_template("drag_queen_info.html", title = "Drag Queen Information")

@app.route("/episode_info")
def episode_info():
    return render_template("drag_queens.html", title = "Drag Queens")

if __name__ == "__main__":
    app.run(debug=True)
