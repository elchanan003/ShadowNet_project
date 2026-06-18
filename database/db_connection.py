import mysql.connector


class DB_connection:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def get_connection(self):
        conn = mysql.connector.connect(
            host=self.host, user=self.user, password=self.password, database=self.database
        )

        return conn

    def create_database(self):
        conn = mysql.connector.connect(
            host=self.host, user=self.user, password=self.password
        )

        cur = conn.cursor()
        
        cur.execute(
        """
        CREATE DATABASE IF NOT EXISTS Intelligence_db                  
        """
        )

        cur.close()
        conn.close()


    def create_tables(self):
        with self.get_connection() as conn:
            with conn.cursor() as cur:

                sql_agents_table = """
                CREATE TABLE IF NOT EXISTS agents(
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(50) NOT NULL,
                specialty VARCHAR(50) NOT NULL,
                is_active BOOL DEFAULT TRUE,
                completed_missions INT DEFAULT 0,
                failed_missions INT DEFAULT 0,
                agent_rank ENUM('Junior', 'Senior', 'Commander')
                )
                """
                sql_missions_table = """
                CREATE TABLE IF NOT EXISTS missions(
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                description TEXT NOT NULL,
                location VARCHAR(255) NOT NULL,
                difficulty INT CHECK (difficulty BETWEEN 1 AND 10) NOT NULL,
                importance INT CHECK (importance BETWEEN 1 AND 10) NOT NULL,
                status VARCHAR(50) DEFAULT 'NEW',
                risk_level VARCHAR(50) NOT NULL, 
                assigned_agent_id INT NULL
                )
                """


                cur.execute(sql_agents_table)
                cur.execute(sql_missions_table)




db = DB_connection('localhost', 'root', 'root', 'Intelligence_db')