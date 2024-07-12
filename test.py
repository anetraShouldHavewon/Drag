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

id = 3
#thing = cursor.execute("SELECT id, name, age FROM Drag_Queens WHERE Drag_Queens.age BETWEEN ? AND ?", ([20, 30])).fetchall()
famous_queen_ids = [15, 16, 19, 20, 22]
famous_queen_names = []
for queen_id in famous_queen_ids:
    queen_name = sql(True, '''SELECT name FROM Drag_Queens 
                        WHERE id = ?''', queen_id)[0]
    famous_queen_names.append(queen_name)

print(famous_queen_names)









