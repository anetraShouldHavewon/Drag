import sqlite3

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

def fetchall_info_list(fetch_query, query_condition, column_index):
    '''This function puts all the output from a fetchall query into a list'''
    fetchall_output = sql(False, fetch_query, query_condition)
    return_list = []
    for item in fetchall_output:
        return_list.append(item[column_index])
    return return_list

episode_queens = fetchall_info_list("SELECT Drag_Queens.name, Placings.name FROM Drag_Queen_Episodes JOIN Drag_Queens ON Drag_Queen_Episodes.drag_queen_id = Drag_Queens.id JOIN Placings ON Drag_Queen_Episodes.placing_id = Placings.id WHERE episode_id = ?", 1, 0)
episode_placings = fetchall_info_list("SELECT Drag_Queens.name, Placings.name FROM Drag_Queen_Episodes JOIN Drag_Queens ON Drag_Queen_Episodes.drag_queen_id = Drag_Queens.id JOIN Placings ON Drag_Queen_Episodes.placing_id = Placings.id WHERE episode_id = ?", 1, 1)
episode_placing_ids = fetchall_info_list("SELECT Drag_Queen_Episodes.placing_id FROM Drag_Queen_Episodes JOIN Drag_Queens ON Drag_Queen_Episodes.drag_queen_id = Drag_Queens.id JOIN Placings ON Drag_Queen_Episodes.placing_id = Placings.id WHERE episode_id = 1", None, 0)
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

print(safe_queens, immune, winner, top_2, eliminated, bottom_2)






