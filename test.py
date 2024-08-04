import sqlite3, random, os

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
                    foreign_key_columns]
        

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

def sql_insert(table, column, value):
    connection = sqlite3.connect("drag_queen.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO {table}({columns}) VALUES (?)".format(table=table, column=column), ((value,)))
    connection.commit()
    connection.close()


table_name = table_names[6]
table_column_names = tuple(table_columns_dict[table_name][0])
print(table_column_names)
answer = 'Alyssa Edwards'
connection = sqlite3.connect("drag_queen.db")
cursor = connection.cursor()
cursor.execute("""INSERT INTO Drag_Queens(?, ?) VALUES (?, ?)""", ('hey', 'howareyou'))
connection.commit()
connection.close()

thing = sql(True, "SELECT * FROM Drag_Queens WHERE name = ?", answer)   
print(table_column_names)









