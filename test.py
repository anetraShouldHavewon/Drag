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
print(franchise_dict, franchise_ids)









