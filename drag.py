'''My Project'''
from flask import Flask, render_template, abort, request, session, redirect, flash
import sqlite3, random

app = Flask(__name__)
# The secret key is there so that the website can successfully encrypt stuff inside
# the sessions dictionary
app.config['SECRET_KEY'] = "Howdahailyougonnalovesomebodyelse" 

def sql(fetchone, query, constraint):
    '''Executes sql queries based on whether they can be executed with a '''
    '''fetchone or fetchall. Gives one result if fetchone, gives a list of'''
    '''results if fetchall'''
    connection = sqlite3.connect("drag_queen.db")
    cursor = connection.cursor()
    if constraint is None:
        if fetchone is True:
            result = cursor.execute(query).fetchone()
        if fetchone is False:  # if the query needs a fetchall
            result = cursor.execute(query).fetchall()
    elif type(constraint) is list:
        if fetchone is True:
            result = cursor.execute(query, (constraint)).fetchone()
        if fetchone is False: # if the query needs a fetchall
            result = cursor.execute(query, (constraint)).fetchall()
    else:
        if fetchone is True:
            result = cursor.execute(query, (constraint,)).fetchone()
        if fetchone is False:  # if the query needs a fetchall
            result = cursor.execute(query, (constraint,)).fetchall()

    return result

def alt_sql(fetchone, query):
    connection = sqlite3.connect("drag_queen.db")
    cursor = connection.cursor()
    if fetchone is True:
        result = cursor.execute(query).fetchone()
    if fetchone is False:  # if the query needs a fetchall
        result = cursor.execute(query).fetchall()

    return result

def alt_fetchall_info_list(fetch_query, column_index):
    fetchall_output = alt_sql(False, fetch_query)
    return_list = []
    for item in fetchall_output:
        return_list.append(item[column_index])
    return return_list

def fetchall_info_list(fetch_query, query_condition, column_index):
    '''This function puts all the output from a fetchall query into a list'''
    fetchall_output = sql(False, fetch_query, query_condition)
    return_list = []
    for item in fetchall_output:
        return_list.append(item[column_index])
    return return_list

def sql_insert(table, column, value):
    '''This function carries out all the insert queries'''
    connection = sqlite3.connect("drag_queen.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO %s %s VALUES %s" % (table, column, value))
    connection.commit()
    connection.close()


# Getting the maximum ids from the drag_queens table
max_drag_queen_id = sql(True, "SELECT MAX(id) FROM Drag_Queens", None)[0]

@app.route("/")
def home():
    # Getting the information latest season across all the franchises
    # in Drag Race
    franchise_ids = fetchall_info_list("SELECT id FROM Franchises", None, 0)
    franchise_names = fetchall_info_list("SELECT name FROM Franchises", None, 0)
    franchise_season_ids = []
    for id in franchise_ids:
        franchise_season_id = sql(True,'''SELECT id, MAX(release_year) 
                               FROM Seasons WHERE franchise_id = ?''',id)[0]
        franchise_season_ids.append(franchise_season_id)
    
    # Randomly drawing out the id and names of five drag queens
    drag_queen_names = ["Angeria Paris VanMicheals"]
    drag_queen_ids = [15]
    drag_queen_database_ids = fetchall_info_list("SELECT id FROM Drag_Queens", None, 0)
    for id in range(9):
        while True:
            # This loop is here to prevent multiple of the same
            # ids from appearing in the list
            random_id = random.choice(drag_queen_database_ids)
            if random_id not in drag_queen_ids:
                break
        drag_name = sql(True, '''SELECT name FROM 
                        Drag_Queens WHERE id = ?''', random_id)[0]
        drag_queen_names.append(drag_name)
        drag_queen_ids.append(random_id)


    return render_template("home.html",
                           drag_names=drag_queen_names,
                           drag_queen_ids=drag_queen_ids,
                           franchise_ids=franchise_ids,
                           franchise_names=franchise_names,
                           franchise_season_ids=franchise_season_ids,
                           title="Home")


@app.route("/seasons")
def seasons():
    # Getting the ids and names of the most recently released seasons
    latest_season_ids = fetchall_info_list('''SELECT id FROM Seasons WHERE
                                    release_year = (SELECT MAX(release_year)
                                    FROM Seasons)''', None, 0)
    latest_season_names = fetchall_info_list('''SELECT name FROM Seasons WHERE
                                    release_year = (SELECT MAX(release_year)
                                    FROM Seasons)''', None, 0)
    
    franchise_dict = {}

    franchise_names = fetchall_info_list("SELECT name FROM Franchises",
                                         None, 0)
    franchise_ids = fetchall_info_list("SELECT id FROM Franchises",
                                         None, 0)
    for index, franchise_id in enumerate(franchise_ids):
        season_ids = fetchall_info_list('''SELECT id FROM Seasons WHERE
                                      franchise_id = ?''', franchise_id, 0)
        season_names = fetchall_info_list('''SELECT name FROM Seasons WHERE
                                      franchise_id = ?''', franchise_id, 0)
        franchise_dict[franchise_names[index]] = [season_ids, season_names]
        
        
    return render_template("seasons.html",
                           latest_season_ids=latest_season_ids,
                           latest_season_names=latest_season_names,
                           franchise_dict=franchise_dict,
                           franchise_names=franchise_names,
                           franchise_ids=franchise_ids,
                           title="Seasons")


@app.route("/season_info/<int:id>")
def season_info(id):
    # Leading users to the error 404 page when the id is larger or smaller than a certain amount
    max_season_id = sql(True, "SELECT MAX(id) FROM Seasons", None)[0]
    if id > max_season_id or id < 1:
        abort(404)        
    season_name = sql(True, "SELECT name FROM Seasons WHERE id = ?", id)[0].upper()
    season_queens_ids = fetchall_info_list('''SELECT 
                                           Drag_Queen_Season.drag_queen_id 
                                           FROM Drag_Queen_Season JOIN 
                                           Drag_Queens ON 
                                           Drag_Queen_Season.drag_queen_id = 
                                           Drag_Queens.id WHERE 
                                           Drag_Queen_Season.season_id = ?''', 
                                           id, 0)
    season_queens_name = fetchall_info_list('''SELECT Drag_Queens.name FROM Drag_Queen_Season JOIN Drag_Queens ON Drag_Queen_Season.drag_queen_id = Drag_Queens.id WHERE Drag_Queen_Season.season_id = ?''', id, 0)
    season_episodes_ids = fetchall_info_list("SELECT id, name FROM Episodes WHERE season_id = ? ORDER BY season_order ASC", id, 0)
    season_episodes_names = fetchall_info_list("SELECT id, name FROM Episodes WHERE season_id = ? ORDER BY season_order ASC", id, 1)
    season_episodes_imgs = fetchall_info_list("SELECT img_link FROM Episodes WHERE season_id = ? ORDER BY season_order ASC", id, 0)
    
    return render_template("season_info.html", 
                           season_id=id,
                           season_name=season_name,
                           season_queens_ids=season_queens_ids,
                           season_queens_name=season_queens_name,
                           season_episodes_ids=season_episodes_ids,
                           season_episodes_names=season_episodes_names,
                           season_episodes_imgs=season_episodes_imgs,
                           title="Season Information")


@app.route("/drag_queens/<int:id>")
def drag_queens(id):
    # Redirecting to the 404 page when all ids that are not between
    # 0 and 3
    if id > 3 or id < 0:
        abort(404)

    def drag_queen_filter(constraint, filter):
        # Getting the ids and names of drag queens from a specific season
        if filter == 1:
            drag_queens_info = sql(False, '''SELECT 
                                Drag_Queen_Season.drag_queen_id,
                                Drag_Queens.name FROM Drag_Queen_Season
                                JOIN Drag_Queens ON 
                                Drag_Queen_Season.drag_queen_id =
                                Drag_Queens.id WHERE 
                                Drag_Queen_Season.season_id = ?''',
                                constraint)
            
        if filter == 2:
            drag_queens_info = sql(False, '''SELECT id, name FROM 
                                   Drag_Queens WHERE city = ?''',
                                   constraint)
        
        if filter == 3:
            drag_queens_info = sql(False, '''SELECT id, name FROM 
                                      Drag_Queens WHERE age 
                                      BETWEEN ? AND ?''', constraint)
            
        # Putting the ids and names of the queens into two different lists
        drag_queen_ids = []
        drag_queen_names = []
        for queen in range(len(drag_queens_info)):
            drag_queen_ids.append(drag_queens_info[queen][0])
            drag_queen_names.append(drag_queens_info[queen][1])

        return drag_queen_ids, drag_queen_names
    
    # The default page of drag queen info page
    if id == 0:
        # Getting the id of one the most recent seasons
        recent_season_id = sql(True, '''SELECT id, MAX(release_year) FROM 
                               Seasons''', None)[0]
        recent_season_name = sql(True, '''SELECT name, MAX(release_year) FROM 
                               Seasons''', None)[0]
                            
        # Getting the names and ids of the queens from the 
        # most recent season in a list
        recentdrag_queen_ids = drag_queen_filter(recent_season_id, 1)[0]
        recentdrag_queen_names = drag_queen_filter(recent_season_id, 1)[1]

        # Getting the names of famous contestants to come out of drag race
        famous_queen_ids = [15, 16, 19, 20, 22]
        famous_queen_names = []
        for queen_id in famous_queen_ids:
            queen_name = sql(True, '''SELECT name FROM Drag_Queens 
                             WHERE id = ?''', queen_id)[0]
            famous_queen_names.append(queen_name)

        return render_template("drag_queens.html", 
                               page_id=id,
                               season_name=recent_season_name,
                               drag_queen_ids=recentdrag_queen_ids, 
                               drag_queen_names=recentdrag_queen_names,
                               famous_queen_ids=famous_queen_ids,
                               famous_queen_names=famous_queen_names,
                               title="Drag Queens")

    else:
        # The next section codes for a page that allows users to 
        # filter drag queens by seasons 
        if id == 1:
            # Getting the names and ids of all the seasons
            # in the Drag Race franchise 
            season_ids = fetchall_info_list("SELECT id FROM Seasons", None, 0)
            headings = fetchall_info_list("SELECT name FROM Seasons", None, 0)
            drag_queens = {}

            # Getting the names and ids of the queens of each season 
            # within the Drag Race franchise
            for index, season_id in enumerate(season_ids):
                drag_queen_ids = drag_queen_filter(season_id, 1)[0]
                drag_queen_names = drag_queen_filter(season_id, 1)[1] 
                drag_queens[headings[index]] = [drag_queen_ids,
                                                drag_queen_names]
                
        # The next section codes for a page where drag queens are 
        # filtered by cities
        if id == 2:
            # Getting all the unique cities of origin of the drag queens
            headings = fetchall_info_list('''SELECT DISTINCT city 
                                        FROM Drag_Queens''', None, 0)
            drag_queens = {}

            # Getting the names and ids of drag queens for each 
            # unique city
            for city in headings:
                drag_queen_ids = drag_queen_filter(city, 2)[0]
                drag_queen_names = drag_queen_filter(city, 2)[1]
                drag_queens[city] = [drag_queen_ids, drag_queen_names]

        # The next section codes for a page where drag queens are 
        # filtered by age range
        if id == 3:
            age_ranges = [[20, 29], [30, 39], [40, 49]]
            headings = ["Younger Queens(20~30)", "Established Queens(30~40)",
                        "Wow She Stuck Around for Long(40~50)"]
            drag_queens = {}
            for index, age_range in enumerate(age_ranges):
                drag_queen_ids = drag_queen_filter(age_range, 3)[0]
                drag_queen_names = drag_queen_filter(age_range, 3)[1]
                drag_queens[headings[index]] = [drag_queen_ids, drag_queen_names]

        return render_template("drag_queens.html", 
                           page_id=id,
                           headings=headings,
                           drag_queens=drag_queens,
                           title="Drag Queens")




@app.route("/drag_queen_info/<int:id>")
def drag_queen_info(id):
    # Getting the names, specialty skills, city of origin and age of 
    # a particular drag queen
    drag_queen_info = sql(True, "SELECT * FROM Drag_Queens WHERE id = ?", id)
    # Leading users to the error 404 page when the query gives 
    # None result
    if drag_queen_info is None:
        abort(404)
    name = drag_queen_info[1]
    specialty_skills = drag_queen_info[2]
    description = drag_queen_info[3]
    city = drag_queen_info[4]
    age = drag_queen_info[5]
    iconic_quote = drag_queen_info[7]

    return render_template("drag_queen_info.html",
                           id=id,
                           name=name,
                           specialty_skills=specialty_skills,
                           city=city, age=age,
                           drag_queen=drag_queen_info,
                           iconic_quote=iconic_quote,
                           description=description,
                           title="Drag Queen Information")


@app.route("/episode_info/<int:id>")
def episode_info(id): 
    episode_info = sql(True, '''SELECT name, challenge_description, 
                       runway_theme, img_link FROM Episodes WHERE 
                       id = ?''', id)
    if episode_info is None:
        abort(404)
    episode_name = episode_info[0].upper()
    episode_challenge_description = episode_info[1]
    episode_runway_theme = episode_info[2]
    episode_img = episode_info[3]
    episode_challenge_type = sql(True, "SELECT Maxi_Challenge_Type.name FROM Episodes JOIN Maxi_Challenge_Type ON Episodes.maxi_challenge_type_id = Maxi_Challenge_Type.id WHERE Episodes.id = ?", id)[0]
    episode_queens = fetchall_info_list("SELECT Drag_Queens.name, Placings.name FROM Drag_Queen_Episodes JOIN Drag_Queens ON Drag_Queen_Episodes.drag_queen_id = Drag_Queens.id JOIN Placings ON Drag_Queen_Episodes.placing_id = Placings.id WHERE episode_id = ?", id, 0)
    episode_queens_ids = fetchall_info_list("SELECT Drag_Queens.id, Placings.name FROM Drag_Queen_Episodes JOIN Drag_Queens ON Drag_Queen_Episodes.drag_queen_id = Drag_Queens.id JOIN Placings ON Drag_Queen_Episodes.placing_id = Placings.id WHERE episode_id = ?", id, 0)
    episode_placing_ids = fetchall_info_list("SELECT Drag_Queen_Episodes.placing_id FROM Drag_Queen_Episodes JOIN Drag_Queens ON Drag_Queen_Episodes.drag_queen_id = Drag_Queens.id JOIN Placings ON Drag_Queen_Episodes.placing_id = Placings.id WHERE episode_id = ?", id, 0)
   
    safe_queens = {"drag_queen_ids": [],"drag_queen_names": []}
    immune = {"drag_queen_ids": [],"drag_queen_names": []}
    winner = {"drag_queen_ids": [],"drag_queen_names": []}
    top_2 = {"drag_queen_ids": [],"drag_queen_names": []}
    eliminated = {"drag_queen_ids": [],"drag_queen_names": []}
    bottom_2 = {"drag_queen_ids": [],"drag_queen_names": []}

    for index in range(len(episode_queens)):
        if episode_placing_ids[index] == 4:
            safe_queens["drag_queen_ids"].append(episode_queens_ids[index])
            safe_queens["drag_queen_names"].append(episode_queens[index])
        if episode_placing_ids[index] == 1:
            immune["drag_queen_ids"].append(episode_queens_ids[index])
            immune["drag_queen_names"].append(episode_queens[index])
        if episode_placing_ids[index] == 8:
            winner["drag_queen_ids"].append(episode_queens_ids[index])
            winner["drag_queen_names"].append(episode_queens[index])
        if episode_placing_ids[index] == 7:
            top_2["drag_queen_ids"].append(episode_queens_ids[index])
            top_2["drag_queen_names"].append(episode_queens[index])
        if episode_placing_ids[index] == 2:
            eliminated["drag_queen_ids"].append(episode_queens_ids[index])
            eliminated["drag_queen_names"].append(episode_queens[index])
        if episode_placing_ids[index] == 6:
            bottom_2["drag_queen_ids"].append(episode_queens_ids[index])
            bottom_2["drag_queen_names"].append(episode_queens[index])
    queen_rankings = [winner, top_2, safe_queens, bottom_2, eliminated, immune]
    
    return render_template("episode_info.html", 
                           queen_rankings=queen_rankings,
                           episode_name=episode_name,
                           episode_img=episode_img,
                           episode_runway_theme=episode_runway_theme,
                           episode_challenge_description=episode_challenge_description, 
                           episode_challenge_type=episode_challenge_type, 
                           title="Episode Information")


# Code for the login and logout route courtesy of Sir Steven Rodkiss
@app.route("/login", methods=["GET", "POST"])
def login():
    # if the user enters information into the form in login.html
    if request.method == "POST":
        username = request.form.get('user') # using .get allows you to get stuff using the name
        password = request.form.get('pass')
        correct_username = "anetraShouldHavewon"
        correct_password = "howyoudoinggorge12"
        if username == correct_username and password == correct_password:
            session['login'] = True
            flash("You have infiltrated my website")
        else:
            flash("Wrong username or password")
     
    return render_template("login.html",
                           title="Login")

@app.route("/admin/<int:id>", methods=["GET", "POST"])
def admin(id):
    # A class which stores the name, and two functions for an sql table
    if session['login'] is True:
        class Table:
            def __init__(self, name):
                self.name = name

            # Get the names of the columns of a table
            def get_column_names(self):
                column_names_query = alt_sql(False, "PRAGMA table_info({table_name})".format(table_name=self.name))
                column_names = []
                for column in column_names_query:
                    if column[5] != 1:
                        column_name = column[1]
                        column_names.append(column_name)
                return column_names
            
            # Get the names of the columns that contain any foreign keys
            # and the names of the tables the foreign key is from
            # and the 'name' row from the tables the foreign key is from
            def get_foreign_keys(self):
                foreign_key_info = alt_sql(False, "PRAGMA foreign_key_list({table_name})".format(table_name=self.name))
                if len(foreign_key_info) != 0:
                    foreign_key_columns = alt_fetchall_info_list('''PRAGMA foreign_key_list({table_name})'''.format(table_name=self.name), 3)
                    foreign_key_tables = alt_fetchall_info_list("PRAGMA foreign_key_list({table_name})".format(table_name=self.name), 2)
                    foreign_key_table_columns = {}
                    for index, column in enumerate(foreign_key_columns):
                        foreign_key_table = foreign_key_tables[index]
                        foreign_key_datalist = alt_fetchall_info_list("SELECT name FROM {table_name}".format(table_name=foreign_key_table), 0)
                        foreign_key_table_columns[column] = foreign_key_datalist

                    return [foreign_key_table_columns,
                            foreign_key_columns,
                            foreign_key_tables]
            

        # Code from https://stackoverflow.com/questions/13514509/search-sqlite-database-all-tables-and-columns
        # Creating a dictionary with table names as keys and the table's column
        # names and foreign key info as the values
        table_names = fetchall_info_list("SELECT name FROM sqlite_master WHERE type='table'", None, 0)
        table_names.pop(0)
        table_columns_dict = {}
        for table_name in table_names:
            table = Table(table_name)
            table_column_names = table.get_column_names()
            table_foreign_key_names = table.get_foreign_keys()
            table_columns_dict[table_name] = [table_column_names,
                                            table_foreign_key_names]
        
        # Dealing with the data from the form by putting the data inputted into their respective
        # columns in the database
        if request.method == "POST":
            table_name = table_names[id-1]
            table_column_names = table_columns_dict[table_name][0]
            if table_columns_dict[table_name][1] is not None:
                table_foreign_key_names = table_columns_dict[table_name][1][1]
                table_foreign_key_tables = table_columns_dict[table_name][1][2]
            values = []
            insert = True
            while insert:
                for table_column in table_column_names:
                    answer = request.form.get(table_column)
                    if len(answer) == 0:
                        flash(f"You have not entered anything into the {table_column} field.")
                        insert = False
                    else:
                        if table_column in table_foreign_key_names:
                            index = table_foreign_key_names.index(table_column)
                            foreign_key_table = table_foreign_key_tables[index]
                            answer = alt_sql(True, "SELECT id FROM %s WHERE name = '%s'" % (foreign_key_table, answer))[0]
                        values.append(answer)
            values = tuple(values)
            table_column_names = tuple(table_column_names)
            if insert:
                sql_insert(table_name, table_column_names, values)
    else:
        return redirect("/")
    return render_template("admin.html",
                           title="Admin",
                           table_info=table_columns_dict,
                           table_names=table_names,
                           table_id=id)
        
@app.route("/logout")
def logout():
    session['login'] = False
    return redirect("/")

@app.errorhandler(404)
def error(e):
    return render_template("404.html")

if __name__ == "__main__":
    app.run(debug=True)
