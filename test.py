import sqlite3, random, os
from werkzeug.security import generate_password_hash

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

class Table:
    def __init__(self, name):
        self.name = name

    def get_column_names(self):
        column_names_query = alt_sql(False, "PRAGMA table_info({table_name})".format(table_name=self.name))
        column_names = []
        for column in column_names_query:
            if column[5] != 1:
                column_name = column[1]
                column_names.append(column_name)
        return column_names
    
    def get_foreign_keys(self):
        foreign_key_info = alt_sql(False, "PRAGMA foreign_key_list({table_name})".format(table_name=self.name))
        if len(foreign_key_info) != 0:
            foreign_key_columns = alt_fetchall_info_list("PRAGMA foreign_key_list({table_name})".format(table_name=self.name), 3)
            foreign_key_tables = alt_fetchall_info_list("PRAGMA foreign_key_list({table_name})".format(table_name=self.name), 2)
            foreign_key_table_columns = {}
            for index, column in enumerate(foreign_key_columns):
                foreign_key_table = foreign_key_tables[index]
                foreign_key_datalist = alt_fetchall_info_list("SELECT name FROM {table_name}".format(table_name=foreign_key_table), 0)
                foreign_key_table_columns[column] = foreign_key_datalist

            return [foreign_key_table_columns,
                    foreign_key_columns,
                    foreign_key_tables]
        

# https://stackoverflow.com/questions/13514509/search-sqlite-database-all-tables-and-columns
table_names = fetchall_info_list("SELECT name FROM sqlite_master WHERE type='table'", None, 0)
table_names.pop(0)
table_columns_dict = {}
for table_name in table_names:
    table = Table(table_name)
    table_column_names = table.get_column_names()
    table_foreign_key_names = table.get_foreign_keys()
    table_columns_dict[table_name] = [table_column_names, 
                                      table_foreign_key_names]

table_name = table_names[8]
table_column_names = table_columns_dict[table_name][0]
if table_columns_dict[table_name][1] is not None:
    table_foreign_key_names = table_columns_dict[table_name][1][1]
    table_foreign_key_tables = table_columns_dict[table_name][1][2]
values = ["test"]
#for table_column in table_column_names:
    #if table_column in table_foreign_key_names:
        #index = table_foreign_key_names.index(table_column)
        #foreign_key_table = table_foreign_key_tables[index]

def sql_insert(table, column, value):
    connection = sqlite3.connect("drag_queen.db")
    cursor = connection.cursor()
    columns_string = ','.join(column)
    placeholders = ','.join(['?'] * len(value))
    value = tuple(value)
    query = f"INSERT INTO {table} ({columns_string}) VALUES({placeholders})"
    cursor.execute(query, value)
    connection.commit()
    connection.close()

id = 15
finale_lip_sync = sql(True, '''SELECT lip_sync_song FROM 
                              Grand_Finale_Episodes WHERE 
                              episode_id = ?''', id)[0]
finale_special_guest = sql(True, '''SELECT special_guest FROM 
                        Grand_Finale_Episodes WHERE 
                        episode_id = ?''', id)[0] 
winner_id = sql(True, '''SELECT winner FROM Grand_Finale_Episodes WHERE episode_id = ?''', id)[0]
winner_name = sql(True, '''SELECT name FROM Drag_Queens WHERE id = ?''', winner_id)[0]
queen_ids = fetchall_info_list('''SELECT drag_queen_id FROM Drag_Queen_Grand_Finale WHERE episode_id = ?''', id, 0)
queen_names = fetchall_info_list('''SELECT Drag_Queens.name FROM Drag_Queen_Grand_Finale JOIN Drag_Queens ON Drag_Queen_Grand_Finale.drag_queen_id = Drag_Queens.id WHERE episode_id = ?''', id, 0)
queen_performances = fetchall_info_list('''SELECT performance FROM Drag_Queen_Grand_Finale WHERE episode_id = ?''', id, 0)
listy = [id, winner_id]
winner_performance = sql(True, '''SELECT performance FROM Drag_Queen_Grand_Finale WHERE episode_id = ? AND drag_queen_id = ?''', listy)[0]
queen_names.remove(winner_name)
queen_performances.remove(winner_performance)

season_ids = fetchall_info_list("SELECT id FROM Seasons", None, 0)
print(season_ids)








