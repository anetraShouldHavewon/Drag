'''My Project'''
from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def sql(fetchone, query, constraint):
    '''Executes sql queries based on whether they can be executed with a fetchone or fetchall'''
    '''Gives one result if fetchone, gives a list of results if fetchall'''
    connection = sqlite3.connect("drag_queen.db")
    cursor = connection.cursor()
    if constraint is None:
        if fetchone is True:
            result = cursor.execute(query).fetchone()
        if fetchone is False: # if the query needs a fetchall
            result = cursor.execute(query).fetchall()
    else:
        if fetchone is True:
            result = cursor.execute(query, (constraint,)).fetchone()
        if fetchone is False: # if the query needs a fetchall
            result = cursor.execute(query, (constraint,)).fetchall()

    return result

@app.route("/")
def home():
    season_description = sql(True, "SELECT description FROM Season WHERE name = 'Season 16'", None)[0]
    drag_queen_names = []
    for id in range(1, 5): # change later to have minimum and maximum or random or most prominant
        drag_name = sql(True, "SELECT name FROM Drag_Queens WHERE id = ?", id)[0]
        drag_queen_names.append(drag_name)
    return render_template("home.html", drag_names = drag_queen_names, season_description = season_description, title = "Drag Queens")

@app.route("/seasons")
def seasons():
    return render_template("drag_queens.html", title = "Drag Queens")

@app.route("/season_info")
def season_info():
    return render_template("drag_queens.html", title = "Drag Queens")

@app.route("/drag_queens")
def drag_queens():
    # INI --> get the most recent season name/id
    # Getting the names of the queens from the most recent season in a list
    drag_queens_info = sql(False, "SELECT Drag_Queen_Season.drag_queen_id, Drag_Queens.name FROM Drag_Queen_Season JOIN Drag_Queens ON Drag_Queen_Season.drag_queen_id = Drag_Queens.id WHERE Drag_Queen_Season.season_id = 1", None)
    drag_queen_ids = []
    drag_queen_names = []
    for queen in range(len(drag_queens_info)):
        drag_queen_ids.append(drag_queens_info[queen][0])
        drag_queen_names.append(drag_queens_info[queen][1])
        
    return render_template("drag_queens.html", drag_queen_ids = drag_queen_ids, drag_queen_names = drag_queen_names, title = "Drag Queens")

@app.route("/drag_queen_info/<int:id>")
def drag_queen_info(id):
    drag_queen_info = sql(True, "SELECT * FROM Drag_Queens WHERE id = ?", id)
    name = drag_queen_info[1]
    specialty_skills = drag_queen_info[2]
    city = drag_queen_info[4]
    age = drag_queen_info[5]
    return render_template("drag_queen_info.html", name = name, specialty_skills = specialty_skills, city = city, age = age, drag_queen = drag_queen_info, title = "Drag Queen Information")

@app.route("/episode_info")
def episode_info():
    return render_template("drag_queens.html", title = "Drag Queens")

if __name__ == "__main__":
    app.run(debug=True)
