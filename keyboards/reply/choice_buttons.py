from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

course_button1 = KeyboardButton('Python')
course_button2 = KeyboardButton('Mathematical Analysis')
course_button3 = KeyboardButton('Probability Theory')
course_button4 = KeyboardButton('Database Management')


course_markup = ReplyKeyboardMarkup(resize_keyboard=True).row(
    course_button1, course_button2, course_button3, course_button4
)


simple_answer_button1 = KeyboardButton('Да')
simple_answer_button2 = KeyboardButton('Нет')


simple_answer_markup = ReplyKeyboardMarkup(resize_keyboard=True).row(
    simple_answer_button1, simple_answer_button2
)


to_set_button1 = KeyboardButton('Выставить')
to_set_button2 = KeyboardButton('Отменить')


to_set_markup = ReplyKeyboardMarkup(resize_keyboard=True).row(
    to_set_button1, to_set_button2
)