import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO dados (timestamp_sync, timestamp_collected, received_value) VALUES (?, ?, ?)",
            ('1684318975' '1684318977', '47.0')
            )

connection.commit()
connection.close()