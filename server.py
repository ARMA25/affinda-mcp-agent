from mcp.server.fastmcp import FastMCP
import sqlite3

# Initialize the MCP Server
mcp = FastMCP("BusinessOpsAgent")

# TOOL 1: Check Inventory
@mcp.tool()
def check_stock(item_name: str) -> str:
    """Check the quantity of a specific item in the inventory."""
    conn = sqlite3.connect('business.db')
    cursor = conn.cursor()
    
    # We use SQL LIKE to find partial matches (e.g. "Potato" finds "Potato Sacks")
    cursor.execute("SELECT quantity FROM inventory WHERE item_name LIKE ?", (f"%{item_name}%",))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return f"We currently have {result[0]} units of {item_name}."
    else:
        return f"I couldn't find {item_name} in the inventory."

# TOOL 2: Add Inventory (Action)
@mcp.tool()
def add_stock(item_name: str, quantity: int) -> str:
    """Add new stock to the inventory."""
    conn = sqlite3.connect('business.db')
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
    # This keeps the server running so Claude can talk to it
    mcp.run()