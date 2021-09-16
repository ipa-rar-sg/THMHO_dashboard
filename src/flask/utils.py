from datetime import datetime
import os
import psycopg2
import yaml

_config = {
    'dbname': os.environ.get('POSTGRES_DB'),
    'user': os.environ.get('POSTGRES_USER'),
    'password': os.environ.get('POSTGRES_PASSWORD'),
    'host': 'postgres'
}


class MSG:
    '''
    Class for parsing and storing message information from the ROS yaml
    formated messages.
    '''

    def __init__(self, msg):
        '''
        Parses the msg YAML file into a python class
        @param msg: String path of the yaml file to parse
        '''
        _msg = None
        with open(msg) as f:
            _msg = yaml.load(f, yaml.Loader)
        self.date = datetime.now().isoformat()
        self.width = _msg['info']['width']
        self.height = _msg['info']['height']
        self.data = _msg['data']


class PSQL:
    '''
    Class for executing PSQL commands based on the arguments provided within
    the config dictionary to create the connection to the Postgres database.
    '''

    def __init__(self, config):
        '''
        @param config: Python dictionary with values necessary to connect
        to the database. Keywords required: dbname, user, password, host
        '''
        self.config = config

    def exec_query(self, query, *args):
        '''
        Executes the provided query in the connection based on the instance's
        configuration, and formats it with provided args.
        @param query: String with the query to execute, all values to be
        formated must be specified with the %s indicator.
        @param args: List of values of the variables to replace in the query,
        if any.
        @return: Message indicating the success or failure of the query
        execution.
        '''
        try:
            with psycopg2.connect(**self.config) as conn:
                with conn.cursor() as curs:
                    curs.execute(query, args)
            return 'Query executed successfully\n'
        except Exception as e:
            return f'Execution failed, due to following error: {e}\n'


psql = PSQL(_config)
