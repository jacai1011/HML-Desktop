import sqlite3
from pathlib import Path

class DatabaseHandler:
    def __init__(self):
        # Database setup
        self.db_folder = "./db"
        self.db_path = f"{self.db_folder}/HML.db"
        self.connection = None
        self.cursor = None

    def init_database(self):
        self.connector()
        try:
            # Create categories table if it doesn't exist
            sql_categories = """
                CREATE TABLE IF NOT EXISTS categories (
                    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category_name TEXT UNIQUE
                );
            """
            self.cursor.execute(sql_categories)

            # Create tasks table if it doesn't exist
            sql_tasks = """
                CREATE TABLE IF NOT EXISTS tasks (
                    task_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category_id INTEGER,
                    title TEXT NOT NULL,
                    repeatable BOOLEAN,
                    start_time TIME UNIQUE,
                    end_time TIME UNIQUE,
                    duration TIME,
                    FOREIGN KEY (category_id) REFERENCES categories(category_id)
                );
            """
            self.cursor.execute(sql_tasks)

            # Commit changes to the database
            self.connection.commit()

        except Exception as e:
            self.connection.rollback()
            print(e)

        finally:
            # Close the cursor and connection
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()

    def connector(self):
        # Establish a connection to the SQLite database
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()

    def insert_execute(self, sql):
        self.connector()
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()
            print(f"{e}")
            return e
        finally:
            self.cursor.close()
            self.connection.close()

    def search_one_execute(self, sql):
        self.connector()
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
            return result
        except Exception as e:
            print(f"{e}")
            return None
        finally:
            self.cursor.close()
            self.connection.close()

    def search_all_execute(self, sql):
        self.connector()
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            return result
        except Exception as e:
            print(f"{e}")
            return None
        finally:
            self.cursor.close()
            self.connection.close()
            
    def insert_categories(self):
        sql = f"INSERT OR IGNORE INTO categories (category_name) VALUES ('Work'), ('Leisure'), ('Routine'), ('Productivity')"
        result = self.insert_execute(sql=sql)
        return result
    
    def get_category_id(self, category):
        sql = f"SELECT category_id FROM categories WHERE category_name LIKE '{category}'"
        result = self.search_one_execute(sql=sql)
        return result
    
    def insert_task(self, category_id, title, repeatable, start_time, end_time, duration):
        sql = f"""INSERT INTO tasks (category_id, title, repeatable, start_time, end_time, duration) 
                VALUES ('{category_id}', '{title}', '{repeatable}', '{start_time}', '{end_time}', '{duration}')""" 
        result = self.insert_execute(sql=sql)
        return result

    def get_all_tasks(self):
        sql = "SELECT task_id, category_id, title, repeatable, start_time, end_time, duration FROM tasks"
        result = self.search_all_execute(sql=sql)
        return result

    def load_tasks(self):
        sql = "SELECT task_id, category_id, title, repeatable, start_time, end_time, duration FROM tasks ORDER BY start_time"
        result = self.search_all_execute(sql=sql)
        return result

    def get_position(self, task_id):
        sql = f"""
            WITH RankedTasks AS (
                SELECT task_id,
                    start_time,
                    ROW_NUMBER() OVER (ORDER BY start_time) AS position
                FROM tasks
            )
            SELECT position
            FROM RankedTasks
            WHERE task_id = '{task_id}'
        """
        result = self.search_one_execute(sql=sql)
        return result

    def check_timeslot_taken(self, start_input, end_input):
        sql1= f"""
            SELECT start_time
            FROM tasks
            WHERE start_time < '{start_input}' AND end_time > '{start_input}';
        """
        result1 = self.search_one_execute(sql=sql1)
        
        sql2 = f"""
            WITH CheckTimeslot AS (
                SELECT start_time
                FROM tasks
                WHERE start_time > '{start_input}'
            )
            SELECT start_time
            FROM CheckTimeslot
            WHERE start_time < '{end_input}'
        """
        
        result2 = self.search_one_execute(sql=sql2)
        return result1, result2
    
    def delete_task(self, task_id):
        sql = f"DELETE FROM tasks WHERE task_id = '{task_id}'"
        result = self.insert_execute(sql=sql)
        vacuum_sql = "VACUUM;"
        self.insert_execute(sql=vacuum_sql)
        return result
    
    # delete all at end of day
    def delete_all(self):
        delete_sql = "DELETE FROM tasks WHERE repeatable != 'True'"
        result = self.insert_execute(sql=delete_sql)

        vacuum_sql = "VACUUM;"
        self.insert_execute(sql=vacuum_sql)

        return result

