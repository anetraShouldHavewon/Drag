import sqlite3, random

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


max_drag_queen_id = sql(True, "SELECT MAX(id) FROM Drag_Queens", None)[0]
drag_queen_names = []
drag_queen_ids = []
for id in range(4):
    while True:
        random_id = random.randint(1, max_drag_queen_id)
        if random_id not in drag_queen_ids:
            break
    drag_name = sql(True, '''SELECT name FROM 
                    Drag_Queens WHERE id = ?''', random_id)[0]
    drag_queen_names.append(drag_name)
    drag_queen_ids.append(random_id)

print(drag_queen_names, drag_queen_ids)




