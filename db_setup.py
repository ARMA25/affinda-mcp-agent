import sqlite3

def init_db():
    # Connect to a file named 'business.db'. It will be created if it doesn't exist.
    conn = sqlite3.connect('business.db')
    c = conn.cursor()
    
    # Create the inventory table
    c.execute('''CREATE TABLE IF NOT EXISTS inventory
                 (item_name TEXT, quantity INTEGER, price REAL)''')
    
    # Check if table is empty so we don't double-add data
    c.execute('SELECT count(*) FROM inventory')
    if c.fetchone()[0] == 0:
        items = [
            ('Potato Sacks', 5, 25.00),
            ('Shawarma Meat', 10, 50.00),
            ('Soda Cans', 100, 1.50),
            ('Napkins', 20, 5.00)
        ]
        c.executemany('INSERT INTO inventory VALUES (?,?,?)', items)
        print("Added dummy data to database.")
    else:
        print("Database already exists.")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()