import sqlite3

conn = sqlite3.connect("dhij.db")
cursor = conn.cursor()

cursor.execute("UPDATE users SET role = 'admin' WHERE username = ?", ("Imran khan",))
conn.commit()

print("Rows updated:", cursor.rowcount)

conn.close()