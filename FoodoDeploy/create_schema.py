import sqlite3  # ✅ Import SQLite

# ✅ Step 1: Connect to SQLite Database (Creates vendor.db if it doesn't exist)
conn = sqlite3.connect("vendor.db")
cursor = conn.cursor()

# ✅ Step 2: Create "vendor" Table (for vendor accounts)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS vendor (
        id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Unique Vendor ID
        username TEXT UNIQUE NOT NULL,         -- Unique Username
        password TEXT NOT NULL                 -- Vendor Password (hashed in real apps)
    )
""")

# ✅ Step 3: Create "vendor_items" Table (for vendor products)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS vendor_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Unique Item ID
        vendor_id INTEGER NOT NULL,            -- Reference to vendor.id
        item_name TEXT NOT NULL,               -- Name of the food item
        item_price REAL NOT NULL,              -- Price of the food item
        FOREIGN KEY (vendor_id) REFERENCES vendor(id) ON DELETE CASCADE
    )
""")

# ✅ Step 4: Commit Changes & Close Connection
conn.commit()
conn.close()

print("✅ Database schema created successfully!")
