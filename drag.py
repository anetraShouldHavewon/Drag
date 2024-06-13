'''My Project'''
from flask import Flask, render_template, abort
import sqlite3

app = Flask(__name__)

def sql(fetchone, query, constraint):
    '''Executes sql queries based on whether they can be executed with a '''
    '''fetchone or fetchall. Gives one result if fetchone, gives a list of'''
    '''results if fetchall'''
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


def fetchall_info_list(fetch_query, query_condition, column_index):
    '''This function puts all the output from a fetchall query into a list'''
    fetchall_output = sql(False, fetch_query, query_condition)
    return_list = []
    for item in fetchall_output:
        return_list.append(item[column_index])
    return return_list


@app.route("/")
def home():
    season_description = sql(True, "SELECT description FROM Season WHERE name='Season 16'", None)[0]
    drag_queen_names = []
    for id in range(1, 5):  # change later to have minimum and maximum or random or most prominant
        drag_name = sql(True, "SELECT name FROM Drag_Queens WHERE id = ?", id)[0]
        drag_queen_names.append(drag_name)
    return render_template("home.html", drag_names=drag_queen_names, season_description=season_description, title="Home")


@app.route("/seasons")
def seasons():
    season_ids = fetchall_info_list("SELECT id FROM Season WHERE franchise_id = 1", None, 0)
    season_names = fetchall_info_list("SELECT name FROM Season WHERE franchise_id = 1", None, 0)
    franchise_names = fetchall_info_list("SELECT name FROM Franchises", None, 0)
    # INI change code to be more responsive with more seasons

    return render_template("seasons.html", season_ids=season_ids, season_names=season_names, franchise_names=franchise_names, title="Seasons")


@app.route("/season_info/<int:id>")
def season_info(id):
    # Leading users to the error 404 page when the id is larger or smaller than a certain amount
    max_season_id = sql(True, "SELECT MAX(id) FROM Season", None)[0]
    min_season_id = sql(True, "SELECT MIN(id) FROM Season", None)[0]
    if id > max_season_id or id < min_season_id:
        abort(404)        
    season_name = sql(True, "SELECT name FROM Season WHERE id = ?", id)[0]
    season_queens_ids = fetchall_info_list("SELECT Drag_Queen_Season.drag_queen_id, Drag_Queens.name FROM Drag_Queen_Season JOIN Drag_Queens ON Drag_Queen_Season.drag_queen_id = Drag_Queens.id WHERE Drag_Queen_Season.season_id = ?", id, 0)
    season_queens_name = fetchall_info_list("SELECT Drag_Queen_Season.drag_queen_id, Drag_Queens.name FROM Drag_Queen_Season JOIN Drag_Queens ON Drag_Queen_Season.drag_queen_id = Drag_Queens.id WHERE Drag_Queen_Season.season_id = ?", id, 1)
    season_episodes_ids = fetchall_info_list("SELECT id, name FROM Episodes WHERE season_id = ? ORDER BY season_order ASC", id, 0)
    season_episodes_names = fetchall_info_list("SELECT id, name FROM Episodes WHERE season_id = ? ORDER BY season_order ASC", id, 1)
    
    return render_template("season_info.html", season_name=season_name, season_queens_ids=season_queens_ids, season_queens_name=season_queens_name, season_episodes_ids=season_episodes_ids, season_episodes_names=season_episodes_names, title="Season Information")


@app.route("/drag_queens")
def drag_queens():
    # INI --> get the most recent season name/id
    # Leading users to the error 404 page when the id is larger or smaller than a certain amount
    max_drag_queen_id = sql(True, "SELECT MAX(id) FROM Drag_Queens", None)[0]
    min_season_id = sql(True, "SELECT MIN(id) FROM Drag_Queens", None)[0]
    if id > max_season_id or id < min_season_id:
        abort(404) 

    # Getting the names of the queens from the most recent season in a list
    drag_queens_info = sql(False, "SELECT Drag_Queen_Season.drag_queen_id, Drag_Queens.name FROM Drag_Queen_Season JOIN Drag_Queens ON Drag_Queen_Season.drag_queen_id = Drag_Queens.id WHERE Drag_Queen_Season.season_id = 1", None)
    drag_queen_ids = []
    drag_queen_names = []
    for queen in range(len(drag_queens_info)):
        drag_queen_ids.append(drag_queens_info[queen][0])
        drag_queen_names.append(drag_queens_info[queen][1])
        
    return render_template("drag_queens.html", drag_queen_ids=drag_queen_ids, drag_queen_names=drag_queen_names, title="Drag Queens")


@app.route("/drag_queen_info/<int:id>")
def drag_queen_info(id):
    drag_queen_info = sql(True, "SELECT * FROM Drag_Queens WHERE id = ?", id)
    name = drag_queen_info[1]
    specialty_skills = drag_queen_info[2]
    city = drag_queen_info[4]
    age = drag_queen_info[5]
    return render_template("drag_queen_info.html", name=name, specialty_skills=specialty_skills, city=city, age=age, drag_queen=drag_queen_info, title="Drag Queen Information")


@app.route("/episode_info/<int:id>")
def episode_info(id):
    episode_info = sql(True, "SELECT name, challenge_description FROM Episodes WHERE id = ?", id)
    episode_name = episode_info[0]
    episode_challenge_description = episode_info[1]
    episode_challenge_type = sql(True, "SELECT Maxi_Challenge_Type.name FROM Episodes JOIN Maxi_Challenge_Type ON Episodes.maxi_challenge_type_id = Maxi_Challenge_Type.id WHERE Episodes.id = ?", id)[0]
    episode_queens = fetchall_info_list("SELECT Drag_Queens.name, Placings.name FROM Drag_Queen_Episodes JOIN Drag_Queens ON Drag_Queen_Episodes.drag_queen_id = Drag_Queens.id JOIN Placings ON Drag_Queen_Episodes.placing_id = Placings.id WHERE episode_id = ?", id, 0)
    episode_placing_ids = fetchall_info_list("SELECT Drag_Queen_Episodes.placing_id FROM Drag_Queen_Episodes JOIN Drag_Queens ON Drag_Queen_Episodes.drag_queen_id = Drag_Queens.id JOIN Placings ON Drag_Queen_Episodes.placing_id = Placings.id WHERE episode_id = ?", id, 0)
   
    safe_queens = []
    immune = []
    winner = []
    top_2 = []
    eliminated = []
    bottom_2 = []

    for index in range(len(episode_queens)):
        if episode_placing_ids[index] == 4:
            safe_queens.append(episode_queens[index])
        if episode_placing_ids[index] == 1:
            immune.append(episode_queens[index])
        if episode_placing_ids[index] == 8:
            winner.append(episode_queens[index])
        if episode_placing_ids[index] == 7:
            top_2.append(episode_queens[index])
        if episode_placing_ids[index] == 2:
            eliminated.append(episode_queens[index])
        if episode_placing_ids[index] == 6:
            bottom_2.append(episode_queens[index])
    queen_rankings = [winner, top_2, safe_queens, bottom_2, eliminated, immune] 
    
    return render_template("episode_info.html", queen_rankings=queen_rankings, episode_name=episode_name, episode_challenge_description=episode_challenge_description, episode_challenge_type=episode_challenge_type, title="Episode Information")

@app.errorhandler(404)
def error(e):
    return render_template("404.html")
if __name__ == "__main__":
    app.run(debug=True)
