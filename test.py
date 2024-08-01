import sqlite3, random, os

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

# https://stackoverflow.com/questions/13514509/search-sqlite-database-all-tables-and-columns
table_names = fetchall_info_list("SELECT name FROM sqlite_master WHERE type='table'", None, 0)
table_names.pop(0)
for table_name in table_names:
    print(table_name)
    tablename1 = cursor.execute("SELECT * FROM ?", (table_name,))
    print(tablename1)
    print(tablename1.description)


#for table_name in table_names:
    #table_columns[table_name]
#print(table_names)









