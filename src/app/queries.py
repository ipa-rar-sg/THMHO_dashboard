def create_table(table_name, msg):
    '''
    Returns the query that creates the table <table_name> with dimensions
    (columns) based on the provided message <msg>.
    @param table_name: String of the name of the new table
    @param msg: Instance of class utils.MSG
    '''
    query = f'CREATE TABLE IF NOT EXISTS {table_name} (id serial PRIMARY KEY, date TIMESTAMP NOT NULL, '

    for i in range(msg.width):
        for j in range(msg.height):
            query += f'"({i},{j})" INT NOT NULL,'

    query = query[:-1] + ');'
    return query

def delete_table(table_name):
    '''
    Returns the query that deletes the table <table_name>
    @param table_name: String of the name of the table to delete
    '''
    query = f'DROP TABLE IF EXISTS {table_name};'
    return query

def insert_into_table(table_name, msg):
    '''
    Returns the query that inserts a new entry with the information stored
    on <msg> into the table <table_name>
    @param table_name: String of the name of the table
    @param msg: Instance of class utils.MSG which holds the info to insert
    '''
    query = f'INSERT INTO {table_name} VALUES (DEFAULT, %s, '
    query += '%s, ' * (msg.width*msg.height)
    query = query[:-2] + ');'
    return query

def select_from_table(table_name, limit=0):
    '''
    Returns the query that selects all fields from the table <table_name>, if
    <limit> not specified, then the query is for selecting all entries present
    in the table
    @param table_name: String of the name of the table to get entries from.
    @param limit: Maximum number of entries to return. Defaults to all.
    '''
    query = f'SELECT * FROM {table_name}'
    if limit:
        query += f' LIMIT {limit}'
    query += ';'
    return query

