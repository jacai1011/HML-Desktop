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

            sql_schedules = """
                CREATE TABLE IF NOT EXISTS schedules (
                    schedule_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category_id INTEGER,
                    title TEXT NOT NULL,
                    repeatable BOOLEAN,
                    start_time TIME UNIQUE,
                    end_time TIME UNIQUE,
                    duration TIME,
                    FOREIGN KEY (category_id) REFERENCES categories(category_id)
                );
            """
            self.cursor.execute(sql_schedules)
            
            sql_projects = """
                CREATE TABLE IF NOT EXISTS projects (
                    project_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    project_name TEXT UNIQUE,
                    project_color TEXT,
                    category_id INTEGER,
                    FOREIGN KEY (category_id) REFERENCES categories(category_id)
                );
            """
            self.cursor.execute(sql_projects)
            sql_task = """
                CREATE TABLE IF NOT EXISTS tasks (
                    task_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category_id INTEGER,
                    title TEXT NOT NULL,
                    project_id INTEGER,
                    FOREIGN KEY (category_id) REFERENCES categories(category_id),
                    FOREIGN KEY (project_id) REFERENCES projects(project_id)
                );
            """
            self.cursor.execute(sql_task)

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

    def get_category_by_id(self, category_id):
        sql = f"SELECT category_name FROM categories WHERE category_id LIKE '{category_id}'"
        result = self.search_one_execute(sql=sql)
        return result
    
    def insert_schedule(self, category_id, title, repeatable, start_time, end_time, duration):
        sql = f"""INSERT INTO schedules (category_id, title, repeatable, start_time, end_time, duration) 
                VALUES ('{category_id}', '{title}', '{repeatable}', '{start_time}', '{end_time}', '{duration}')""" 
        result = self.insert_execute(sql=sql)
        return result

    def get_all_schedules(self):
        sql = "SELECT schedule_id, category_id, title, repeatable, start_time, end_time, duration FROM schedules"
        result = self.search_all_execute(sql=sql)
        return result
    
    def get_current_schedule(self, time):
        sql = f"""
            SELECT schedule_id, category_id, title, repeatable, start_time, end_time, duration
            FROM schedules
            WHERE start_time <= '{time}' AND end_time > '{time}';
        """
        result = self.search_one_execute(sql=sql)
        return result
    
    def load_schedules(self):
        sql = "SELECT schedule_id, category_id, title, repeatable, start_time, end_time, duration FROM schedules ORDER BY start_time"
        result = self.search_all_execute(sql=sql)
        return result
    
    def insert_task(self, category_id, title, project_id):
        sql = f"""INSERT INTO tasks (category_id, title, project_id) 
                VALUES ('{category_id}', '{title}', '{project_id}')""" 
        result = self.insert_execute(sql=sql)
        return result
    
    def get_all_tasks_by_category(self, category_id):
        sql = f"SELECT task_id, category_id, title, project_id FROM tasks WHERE category_id = '{category_id}'"
        result = self.search_all_execute(sql=sql)
        return result
    
    def load_saved_tasks_by_project(self, category_id):
        sql = f"SELECT task_id, category_id, title, project_id FROM tasks WHERE category_id = '{category_id}' ORDER BY project_id"
        result = self.search_all_execute(sql=sql)
        return result
    
    def delete_task(self, task_id):
        sql = f"DELETE FROM tasks WHERE task_id = '{task_id}'"
        result = self.insert_execute(sql=sql)
        vacuum_sql = "VACUUM;"
        self.insert_execute(sql=vacuum_sql)
        return result
    
    def get_position(self, schedule_id):
        sql = f"""
            WITH RankedSchedules AS (
                SELECT schedule_id,
                    start_time,
                    ROW_NUMBER() OVER (ORDER BY start_time) AS position
                FROM schedules
            )
            SELECT position
            FROM RankedSchedules
            WHERE schedule_id = '{schedule_id}'
        """
        result = self.search_one_execute(sql=sql)
        return result

    def check_timeslot_taken(self, start_input, end_input):
        sql1= f"""
            SELECT start_time
            FROM schedules
            WHERE start_time < '{start_input}' AND end_time > '{start_input}';
        """
        result1 = self.search_one_execute(sql=sql1)
        
        sql2 = f"""
            WITH CheckTimeslot AS (
                SELECT start_time
                FROM schedules
                WHERE start_time > '{start_input}'
            )
            SELECT start_time
            FROM CheckTimeslot
            WHERE start_time < '{end_input}'
        """
        
        result2 = self.search_one_execute(sql=sql2)
        return result1, result2
    
    def delete_schedule(self, schedule_id):
        sql = f"DELETE FROM schedules WHERE schedule_id = '{schedule_id}'"
        result = self.insert_execute(sql=sql)
        vacuum_sql = "VACUUM;"
        self.insert_execute(sql=vacuum_sql)
        return result

    def insert_project(self, project_name, project_color, category_id):
        sql = f"""INSERT INTO projects (category_id, title, project_id) 
                VALUES ('{project_name}', '{project_color}', '{category_id}')""" 
        result = self.insert_execute(sql=sql)
        return result
    
    def get_all_projects_by_category(self, category_id):
        sql = f"SELECT project_name, project_color FROM projects WHERE category_id = '{category_id}'"
        result = self.search_all_execute(sql=sql)
        return result

    def delete_project(self, project_id):
        sql = f"DELETE FROM projects WHERE project_id = '{project_id}'"
        result = self.insert_execute(sql=sql)
        vacuum_sql = "VACUUM;"
        self.insert_execute(sql=vacuum_sql)
        return result
        
    # delete all at end of day
    def delete_all(self):
        delete_sql = "DELETE FROM schedules WHERE repeatable != 'True'"
        result = self.insert_execute(sql=delete_sql)

        vacuum_sql = "VACUUM;"
        self.insert_execute(sql=vacuum_sql)

        return result

