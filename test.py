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

def no_dash(table_name):
    split_name = [letter for letter in table_name]
    no_dash_name = []
    for letter in split_name:
        if letter != "_":
            no_dash_name.append(letter)
        else:
            no_dash_name.append(" ")
    no_dash_name = ''.join(no_dash_name)
    return no_dash_name

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
        no_dash_column_names = []
        for column in column_names:
            no_dash_column = no_dash(column)
            no_dash_column_names.append(no_dash_column)
        return [column_names, no_dash_column_names]
    
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
table_no_dash_names = list(map(no_dash, table_names))
table_columns_dict = {}
for table_name in table_names:
    table_nodashname = no_dash(table_name)
    table = Table(table_name)
    table_column_names = table.get_column_names()[0]
    table_column_nodashnames = table.get_column_names()[1]
    table_foreign_key_names = table.get_foreign_keys()
    table_columns_dict[table_name] = [table_column_names, 
                                      table_foreign_key_names,
                                      table_column_nodashnames] ##

table_name = table_names[0]
table_no_dash_name = table_no_dash_names[0] ##
table_column_names = table_columns_dict[table_name][0]
table_column_nodashnames = table_columns_dict[table_name][2] ##
if table_columns_dict[table_name][1] is not None:
    table_foreign_key_names = table_columns_dict[table_name][1][1]
    table_foreign_key_tables = table_columns_dict[table_name][1][2]
print(table_no_dash_name, table_column_nodashnames)
answer = "No"
for table_column in table_column_names:
    if table_column in table_foreign_key_names:
        index = table_foreign_key_names.index(table_column)
        foreign_key_table = table_foreign_key_tables[index]
        foreign_key_datalist = table_columns_dict[table_name][1][0][table_column]
        if answer not in foreign_key_datalist:
            print(f"This option is not available in the {table_column} field")
foreign_key_table = "Drag_Queens"
answer = "Rupaul's Drag Race: Season 15"
#answer = alt_sql(True, "SELECT id FROM %s WHERE name = '%s'" % (foreign_key_table, answer))[0]
# print(answer)
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

#dash_string = input("HEYY: ")

#print(no_dash(dash_string))
id = 30
episode_queens = fetchall_info_list('''SELECT Drag_Queens.name,
                                            Placings.name FROM
                                            Drag_Queen_Episodes JOIN
                                            Drag_Queens ON
                                            Drag_Queen_Episodes.drag_queen_id =
                                            Drag_Queens.id JOIN Placings ON
                                            Drag_Queen_Episodes.placing_id =
                                            Placings.id WHERE
                                            episode_id = ?''', id, 0)
episode_queens_ids = fetchall_info_list('''SELECT Drag_Queens.id,
                                        Placings.name FROM
                                        Drag_Queen_Episodes JOIN
                                        Drag_Queens ON
                                        Drag_Queen_Episodes.drag_queen_id
                                        = Drag_Queens.id JOIN Placings
                                        ON
                                        Drag_Queen_Episodes.placing_id
                                        = Placings.id WHERE episode_id
                                        = ?''', id, 0)
episode_placing_ids = fetchall_info_list('''SELECT
                                            Drag_Queen_Episodes.
                                            placing_id FROM
                                            Drag_Queen_Episodes
                                            JOIN Drag_Queens ON
                                            Drag_Queen_Episodes.
                                            drag_queen_id =
                                            Drag_Queens.id JOIN
                                            Placings ON
                                            Drag_Queen_Episodes.placing_id =
                                            Placings.id WHERE episode_id =
                                            ?''', id, 0)
# Ordering the queens in an episode based on their particular rank
# within the episode
# This is to ensure that the queens are shown in the correct order from
# the winner to the eliminated queens
safe_queens = {"drag_queen_ids": [], "drag_queen_names": []}
immune = {"drag_queen_ids": [], "drag_queen_names": []}
winner = {"drag_queen_ids": [], "drag_queen_names": []}
top_2 = {"drag_queen_ids": [], "drag_queen_names": []}
eliminated = {"drag_queen_ids": [], "drag_queen_names": []}
bottom_2 = {"drag_queen_ids": [], "drag_queen_names": []}
# Evaluate the positions of the queens for a particular episode and
# add their names and ids to particular dictionaries above
# as values
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
queen_rankings = [winner, top_2, safe_queens, bottom_2, eliminated,
                    immune]
print(queen_rankings[0]["drag_queen_ids"])






