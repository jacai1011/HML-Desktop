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
        # Create necessary folder and database file if they don't exist
        # folder_path = Path(self.db_folder)
        # db_path = Path(self.db_path)

        # if not folder_path.exists():
        #     folder_path.mkdir(parents=True)

        # if not db_path.exists():
        #     with open(self.db_path, "w"):
        #         pass

        # Connect to the database and create the tables if they don't exist
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
        sql = f"INSERT OR IGNORE INTO categories (category_name) VALUES ('Work'), ('Leisure'), ('Routine'), ('Self-Work')"
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
    
    # delete all at end of day
    def delete_all(self):
        delete_sql = "DELETE FROM tasks WHERE repeatable != 1;"
        self.insert_execute(sql=delete_sql)

        vacuum_sql = "VACUUM;"
        result = self.insert_execute(sql=vacuum_sql)

        return result

