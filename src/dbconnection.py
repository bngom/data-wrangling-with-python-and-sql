import pyodbc


class DBConnection(object):
    """Handle database connexion
    :arg
        driver: the db driver
        server : the hostname of the server
        database: the db name
        user: the db's username
        password: the db's password"""
    def __init__(self, driver, server, database, user, password):
        self.driver = driver
        self.server = server
        self.database = database
        self.user = user
        self.password = password
        self.dbconn = pyodbc.connect(
            'DRIVER={SQL Server};SERVER=' + self.server + ';DATABASE=' + self.database + '; UID = ' + self.user + '; PWD = ' + self.user + 'Trusted_Connection=yes')

    def get_connection(self):
        """creates new connection
        :returns a database object
        """
        return self.dbconn

    def execute_query(self, query):
        """execute query on db connection
        :arg
         query: The query to be executed
        :except pyodbc.ProgrammingError
         """
        conn = self.dbconn
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
            #result = cursor.fetchall()
            cursor.close()
        except pyodbc.ProgrammingError as e:
            raise("db error occured", e)


    # For explicitly opening database connection
    def __enter__(self):
        self.dbconn = self.get_connection()
        return self.dbconn

    # For explicitly closing database connection
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.dbconn.close()
