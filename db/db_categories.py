import sqlite3

# Database connection helper function
def get_db_connection():
    conn = sqlite3.connect('HML.db')
    conn.row_factory = sqlite3.Row  # Access rows as dictionaries
    return conn

# Example function to get all categories
def db_get_all_categories():
    conn = get_db_connection()
    categories = conn.execute('SELECT * FROM categories').fetchall()
    conn.close()
    return categories

# Example function to get a category by ID
def get_category_by_id(category_id):
    conn = get_db_connection()
    category = conn.execute('SELECT * FROM categories WHERE id = ?', (category_id,)).fetchone()
    conn.close()
    return category

# Example function to add a new category
def db_add_category(category):
    conn = get_db_connection()
    conn.execute('INSERT INTO categories (category) VALUES (?)', (category,))
    conn.commit()
    conn.close()

# Example function to delete a category by ID
def delete_category(category_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM categories WHERE id = ?', (category_id,))
    conn.commit()
    conn.close()
