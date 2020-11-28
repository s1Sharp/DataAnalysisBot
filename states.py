from aiogram.dispatcher.filters.state import StatesGroup, State


class Registration(StatesGroup):
    Q1 = State()
    Q2 = State()
    Q3 = State()
    Q4 = State()


class RegisterForClasses(StatesGroup):
    Q1 = State()


class RegistrationTeacherOnCourse(StatesGroup):
    Q1 = State()
    Q2 = State()
    Q3 = State()
    Q4 = State()


class LeaveCourse(StatesGroup):
    Q1 = State()
    Q2 = State()

class GetGrades(StatesGroup):
    Q1 = State()
    Q2 = State()
    Q3 = State()
    Q4 = State()


class StudentStatForClass(StatesGroup):
    Q1 = State()

class GetTop5(StatesGroup):
    Q1 = State()