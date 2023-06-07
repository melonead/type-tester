import sqlite3


class Database:

    def __init__(self):
        self.connect()
    
    def connect(self):
        self.connection = sqlite3.connect("Typing.db")
        self.db_cursor = self.connection.cursor()
    
    def create_table(self):
        try:
            self.db_cursor.execute("""
            CREATE TABLE results (day text, month text, month_date text,
            time text, year text, speed integer)
            
            """)
        except sqlite3.OperationalError:
            pass
    
    def insert_row(self, day, month, month_date, time, year, speed):
        self.db_cursor.execute("""
        INSERT INTO results VALUES (?, ?, ?, ?, ?, ?)""", 
        (day, month, month_date, time, year, speed))
        self.commit()

    
    def commit(self):
        self.connection.commit()
        # self.connection.close()


db = Database()

'''
for d in db.db_cursor.execute("select * from results where speed < 50"):
    print(d)
'''