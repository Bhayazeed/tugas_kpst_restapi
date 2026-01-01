import sqlite3

con = sqlite3.connect("data_monitor.db")
cur = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS data(" \
                "id_data TEXT NOT NULL PRIMARY KEY,"
                "service_name TEXT NOT NULL," \
                "cpu_usage FLOAT NOT NULL," \
                "memory_usage FLOAT NOT NULL," \
                "latency INTEGER NOT NULL," \
                "error_count INTEGER NOT NULL" 
")")

res = cur.execute("SELECT name FROM sqlite_master")
res.fetchone()

con.commit()