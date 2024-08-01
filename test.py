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

def alt_sql(fetchone, query):
    connection = sqlite3.connect("drag_queen.db")
    cursor = connection.cursor()
    if fetchone is True:
        result = cursor.execute(query).fetchone()
    if fetchone is False:  # if the query needs a fetchall
        result = cursor.execute(query).fetchall()

    return result

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
            #foreign_key_tables = []
            #foreign_key_table_columns = []
            #for info in foreign_key_info:
                #foreign_key_columns.append(info[3])
                #foreign_key_tables.append(info[2])
                #foreign_key_table_columns.append(info[4])

            return [foreign_key_columns]
        

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

print(table_columns_dict["Drag_Queen_Episodes"][1])











