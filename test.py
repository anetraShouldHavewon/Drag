import sqlite3, random

connection = sqlite3.connect("drag_queen.db")
cursor = connection.cursor()
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


def fetchall_info_list(fetch_query, query_condition, column_index):
    '''This function puts all the output from a fetchall query into a list'''
    fetchall_output = sql(False, fetch_query, query_condition)
    return_list = []
    for item in fetchall_output:
        return_list.append(item[column_index])
    return return_list

def drag_queen_filter(constraint_id, filter):
        # Getting the ids and names of drag queens from a specific season
        if filter == 1:
            drag_queens_info = sql(False, '''SELECT 
                                Drag_Queen_Season.drag_queen_id,
                                Drag_Queens.name FROM Drag_Queen_Season
                                JOIN Drag_Queens ON 
                                Drag_Queen_Season.drag_queen_id =
                                Drag_Queens.id WHERE 
                                Drag_Queen_Season.season_id = ?''',
                                constraint_id)
            
        if filter == 2:
            drag_queens_info = sql(False, '''SELECT id, name FROM 
                                   Drag_Queens WHERE city = ?''',
                                   constraint_id)
            
        if filter == 3:
            drag_queens_info = sql(False, '''SELECT id, name FROM 
                                      Drag_Queens WHERE age 
                                      BETWEEN ? AND ?''', constraint_id)
            
        # Putting the ids and names of the queens into two different lists
        drag_queen_ids = []
        drag_queen_names = []
        for queen in range(len(drag_queens_info)):
            drag_queen_ids.append(drag_queens_info[queen][0])
            drag_queen_names.append(drag_queens_info[queen][1])

        return drag_queen_ids, drag_queen_names

episode_queens = fetchall_info_list("SELECT Drag_Queens.name, Placings.name FROM Drag_Queen_Episodes JOIN Drag_Queens ON Drag_Queen_Episodes.drag_queen_id = Drag_Queens.id JOIN Placings ON Drag_Queen_Episodes.placing_id = Placings.id WHERE episode_id = ?", 1, 0)
episode_queens_ids = fetchall_info_list("SELECT Drag_Queens.id, Placings.name FROM Drag_Queen_Episodes JOIN Drag_Queens ON Drag_Queen_Episodes.drag_queen_id = Drag_Queens.id JOIN Placings ON Drag_Queen_Episodes.placing_id = Placings.id WHERE episode_id = ?", 1, 0)
episode_placing_ids = fetchall_info_list("SELECT Drag_Queen_Episodes.placing_id FROM Drag_Queen_Episodes JOIN Drag_Queens ON Drag_Queen_Episodes.drag_queen_id = Drag_Queens.id JOIN Placings ON Drag_Queen_Episodes.placing_id = Placings.id WHERE episode_id = ?", 1, 0)
   
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
print(queen_rankings)









