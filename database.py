import sqlite3


class Database:
    def __init__(self):
        self.db = sqlite3.connect("database.db")
        self.cursor = self.db.cursor()

    def create_table_users(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users(
                id INT,
                full_name VARCHAR(221),
                phone_number VARCHAR(221)
            )
        """)
        self.db.commit()

    def create_table_time(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS time(
                start_time VARCHAR(221),
                end_time VARCHAR(221),
                is_booked BOOLEAN
            )
        """)


    def add_time(self, start_time, end_time):
        self.cursor.execute("""
            INSERT INTO time(start_time, end_time, is_booked)
            VALUES (?, ?, ?)
        """, (start_time, end_time, False))

        self.db.commit()

    def add_user(self, id, full_name, phone_number):
        self.cursor.execute("""
            INSERT INTO users(id, full_name, phone_number)
            VALUES (?, ?, ?)
        """, (id, full_name, phone_number))

    def check_user(self, id):
        result = self.cursor.execute("""
            SELECT * FROM users 
            WHERE id = ?
        """, (id, )).fetchone()

        return result

    def get_all_aviable_time(self):
        result = self.cursor.execute("""
            SELECT * FROM time
            WHERE is_booked = 0 
        """)

        return result.fetchall()

    def book_slot(self,start_time,end_time):
        self.cursor.execute("""
            UPDATE time
            SET is_booked = 1
            WHERE start_time = ? AND end_time = ?
        """, (start_time,end_time))
        self.db.commit()

    def close_database(self):
        self.db.close()