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

drag_queen_names = []
for id in range(1,5):
        drag_name = sql(True, "SELECT name FROM Drag_Queens WHERE id = ?", id)[0]
        drag_queen_names.append(drag_name)

x = sql(False, "SELECT Drag_Queens.name FROM Drag_Queen_Season JOIN Drag_Queens ON Drag_Queen_Season.drag_queen_id = Drag_Queens.id WHERE Drag_Queen_Season.season_id = 1", None)
drag_queen_names = []
for queen in range(len(x)):
    drag_queen_names.append(x[queen][0])
print(drag_queen_names)