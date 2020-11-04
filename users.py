

class Student:
    def __init__(self, id, name, surname, group, email):
        self.id = id
        self.name = name
        self.surname = surname
        self.group = group
        self.email = email

    def as_query(self):
        return self.id, self.name, self.surname, self.group, self.email


class Teacher:
    def __int__(self, id, surname, name, patronymic, email):
        self.id = id
        self.surname = surname
        self.name = name
        self.patronymic = patronymic
        self.email = email

    def as_query(self):
        return self.id, self.surname, self.name, self.patronymic, self.email


class Admin:
    def __init__(self, id, admin_code):
        self.id = id
        self.admin_code = admin_code

    def as_query(self):
        return self.id, self.admin_code
