import datetime

class Database:
    use_database: bool
    db_config: dict
    print_mode: int

    def initialize(use_database: bool, db_config: dict, print_mode: int) -> None:
        Database.print_mode = print_mode
        Database.use_database = use_database
        if Database.use_database:
            Database.db_config = db_config
        Database.log("Database.initialize ended",0)

    
    def log(text: str, criticality=0):
        if criticality < Database.print_mode:
            return
        
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        crit_char = ""
        match criticality:
            case 1:
                crit_char = "~"
            case 2:
                crit_char = "*"
            case 3: 
                crit_char = "!"
            case _:
                crit_char = ""

        print(f"[{now}] {crit_char}\t{text}")


    def connect_to_mysql(config, attempts=3, delay=2):
        import mysql.connector
        import time
        attempt = 1
        while attempt < attempts + 1:
            try:
                return mysql.connector.connect(**config)
            except (mysql.connector.Error, IOError) as err:
                if (attempts is attempt):
                    # Attempts to reconnect failed; returning None
                    Database.log(f"Failed to connect, exiting without a connection: {err}",3)
                    return None
                Database.log(f"Connection failed: {err}. Retrying ({attempt}/{attempts-1})...",2)
                # progressive reconnect delay
                time.sleep(delay ** attempt)
                attempt += 1
        return None
    

    def run_query_return_rows(select_statement: str, arguments: tuple = ()):
        connection = Database.connect_to_mysql(Database.db_config)
        if connection and connection.is_connected():
            data = []
            try:
                with connection.cursor(buffered=True) as cursor:
                    Database.log(f"QUERY:({select_statement}) PARAM:{arguments}",0)
                    cursor.execute(select_statement, arguments)
            finally:
                connection.close()
            return cursor.fetchall()
        else:
            Database.log(f"Failed to call ({select_statement})",3)
            return []
        

    def call_procedure_return_scalar(procedure: str, arguments: tuple):
        connection = Database.connect_to_mysql(Database.db_config)
        connection.autocommit = True
        if connection and connection.is_connected():
            try:
                with connection.cursor() as cursor:
                    Database.log(f"SP:({procedure}) PARAM:{arguments}",0)
                    cursor.callproc(procedure, arguments)
                    
            finally:
                connection.close()
            Database.log(f"  SP returned rowcount={cursor.rowcount}",0)
            return cursor.rowcount
        else:
            Database.log(f"Failed to call ({procedure})",3)
            return 0