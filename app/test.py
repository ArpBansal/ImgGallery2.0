import sqlite3
from datetime import datetime
import os
# Connect to the SQLite database
conn = sqlite3.connect('test.db')
cursor = conn.cursor()

# Create the image_indexing table
# cursor.execute("""
#     CREATE TABLE IF NOT EXISTS image_indexing (
#         id INTEGER PRIMARY KEY,
#         timestamp TEXT,
#         path TEXT
#     )
# """)
# cursor.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON image_indexing (timestamp)")
# # Insert example entries
# cursor.execute("INSERT INTO image_indexing (timestamp, path) VALUES ('2024-08-12 16:30:12.4556', '/path/to/image1.png')")
# cursor.execute("INSERT INTO image_indexing (timestamp, path) VALUES ('2024-08-12 16:35:00', '/path/to/image2.png')")
# cursor.execute("INSERT INTO image_indexing (timestamp, path) VALUES ('2024-08-12 16:34:00.100', '/path/to/image3.png')")
# time = datetime.fromtimestamp(os.path.getmtime("app/IMG_1540.JPG"))
# cursor.execute("""INSERT INTO image_indexing (timestamp, path) VALUES (?, ?)""", (time, "path/to/imageak.png"))
# conn.commit()
cursor.execute("SELECT * FROM image_indexing ORDER BY timestamp DESC")

# Query to retrieve entries sorted by timestamp
rows = cursor.fetchall()

conn.close()

for row in rows:
    print(row)

# Close the connection
import sqlite3

def get_table_schema(db_path, table_name):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Using PRAGMA table_info
    cursor.execute(f"PRAGMA table_info({table_name})")
    table_info = cursor.fetchall()
    
    # Using sqlite_schema
    cursor.execute(f"SELECT sql FROM sqlite_schema WHERE name = '{table_name}'")
    schema_info = cursor.fetchone()
    
    conn.close()
    
    return table_info, schema_info


# db_path = 'test.db'
# table_name = 'image_indexing'
# table_info, schema_info = get_table_schema(db_path, table_name)

# print("Table Info (PRAGMA table_info):")
# for column in table_info:
#     print(column)

# print("\nSchema Info (sqlite_schema):")
# print(schema_info[0])
