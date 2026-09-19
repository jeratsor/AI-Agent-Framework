import sqlite3


DB_FILE = "data/data.db"


connection = sqlite3.connect(DB_FILE)

cursor = connection.cursor()

cursor.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type='table'
    ORDER BY name
""")

tables = cursor.fetchall()

print("\nTables in database:")
print("-------------------")

for table in tables:
    print(table[0])

connection.close()