import sqlite3

connection = sqlite3.connect("data/sample.db")

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS employees (

    employee_id INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    department TEXT,
    salary REAL

)
""")

employees = [

    (1, "Alice", "Smith", "Finance", 72000),
    (2, "Bob", "Johnson", "IT", 85000),
    (3, "Charlie", "Brown", "HR", 61000),
    (4, "Diana", "Jones", "Operations", 79000)

]

cursor.executemany(

    """
    INSERT OR REPLACE INTO employees
    VALUES (?, ?, ?, ?, ?)
    """,

    employees

)

connection.commit()

connection.close()

print("Database created successfully.")