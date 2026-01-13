from mcp.server.fastmcp import FastMCP
import sqlite3
import os

# Initialize the MCP Server
mcp = FastMCP("BusinessOpsAgent")

# --- PRO FIX: ALWAYS FIND THE DATABASE ---
# Get the directory where THIS script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Build the full path to the database
DB_PATH = os.path.join(BASE_DIR, 'business.db')

@mcp.tool()
def check_stock(item_name: str) -> str:
    """Check the quantity of a specific item in the inventory."""
    # Use the absolute path (DB_PATH) instead of just 'business.db'
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Check if table exists first (to avoid crashes if DB is empty)
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='inventory'")
    if not cursor.fetchone():
        conn.close()
        return "Error: The inventory table does not exist. Please run db_setup.py."

    cursor.execute("SELECT quantity FROM inventory WHERE item_name LIKE ?", (f"%{item_name}%",))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return f"We currently have {result[0]} units of {item_name}."
    else:
        return f"I couldn't find {item_name} in the inventory."

@mcp.tool()
def add_stock(item_name: str, quantity: int) -> str:
    """Add new stock to the inventory."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT quantity FROM inventory WHERE item_name LIKE ?", (f"%{item_name}%",))
    exists = cursor.fetchone()
    
    if exists:
        new_qty = exists[0] + quantity
        cursor.execute("UPDATE inventory SET quantity = ? WHERE item_name LIKE ?", (new_qty, f"%{item_name}%"))
        msg = f"Updated. Added {quantity} to {item_name}. New total: {new_qty}."
    else:
        cursor.execute("INSERT INTO inventory (item_name, quantity, price) VALUES (?, ?, 0)", (item_name, quantity))
        msg = f"Created new item {item_name} with quantity {quantity}."
        
    conn.commit()
    conn.close()
    return msg

if __name__ == "__main__":
    mcp.run()