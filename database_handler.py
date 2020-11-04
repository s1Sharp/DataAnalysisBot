import sqlite3
from logger import LOGGER


class DataBaseHandler:
    def __init__(self, database_name):
        self.database_name = database_name
        self.connection = sqlite3.connect(database_name, check_same_thread=False)
        self.cursor = self.connection.cursor()
        LOGGER.log("DataBase: "+database_name+" connected.")

    def get_database_info(self):
        return self.cursor.execute('''select * from sqlite_master;''').fetchall()

    def select_all(self, table_name):
        return self.cursor.execute(f'''select * from {table_name};''').fetchall()

    def add_student(self, student):
        self.cursor.execute(f"""INSERT INTO student(id_user, name, surname, id_group, mail)
                         VALUES (?,?,?,?,?);""", student.as_query())

    def add_teacher(self, teacher):
        self.cursor.execute(f"""INSERT INTO teacher(id_user, name, surname, mail)
                        VALUES (?,?,?,?);""", teacher.as_query())

    def add_admin(self, admin):
        self.cursor.execute(f"""INSERT INTO admin(id_user, password)
                                VALUES (?,?);""", admin.as_query())

