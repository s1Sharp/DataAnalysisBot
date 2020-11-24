from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from keyboards.reply.choice_buttons import course_markup, simple_answer_markup, to_set_markup
from aiogram.types import ReplyKeyboardRemove
from loader import dp
from queries import insert_new_student, check_telegramdi_in_student_course, get_cid_by_name, join_to_course, \
    check_course_pass, insert_new_teacher, insert_new_teacher_course, leave_course, get_info_about_me
from states import Registration, RegistrationTeacherOnCourse, LeaveCourse
from states import RegisterForClasses
import pandas as pd
import math
import numpy as np


@dp.message_handler(Command('start'))
async def start(message: types.Message):
    await message.answer("Привет, я бот-журнал!)\nДля списка команд нажми /help")


@dp.message_handler(Command('help'))
async def start(message: types.Message):
    await message.answer("*Команды для студентов:\n"
                         "1)/reg - Начать регистрацию пользователя\n"
                         "2)/jointhecourse - поступить на курс\n"       
                         "3)/infoaboutme - получить информацию о себе\n"        #в разработке
                         "4)/getmygrades получить оценки по предмету\n"         #в разработке
                         "5)/leavethecours - покинуть курс\n"
                         "*Команды для преподавателя:\n"
                         "1)/teacher - стать администратором курса\n")          #в разработке


@dp.message_handler(Command("reg"), state=None)
async def enter_test(message: types.Message):
    await message.answer("Введите свое имя")
    await Registration.Q1.set()


@dp.message_handler(state=Registration.Q1)
async def answer_q1(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(answer1=answer)
    await message.answer("Введите свою фамилию")
    await Registration.next()


@dp.message_handler(state=Registration.Q2)
async def answer_q2(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(answer2=answer)
    await message.answer("Введите номер своего студенческого билета")
    await Registration.next()


@dp.message_handler(state=Registration.Q3)
async def answer_q3(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(answer3=answer)
    await message.answer("Введите номер группы")
    await Registration.next()


@dp.message_handler(state=Registration.Q4)
async def answer_q4(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if data.get("answer1").isalpha() and data.get("answer2").isalpha() and data.get("answer3").isdigit():
        answer1 = data.get("answer1")
        answer2 = data.get("answer2")
        answer3 = int(data.get("answer3"))
        answer4 = message.text
        answer5 = message.from_user.id
        try:
            insert_new_student(answer5, answer1, answer2, answer3, answer4)
            await message.answer("Успешная регистрация!")
        except:
            await message.answer("С этого аккаунта уже была произведена регистрация!")
    else:
        await message.answer("Вы ввели неверные данные")

    await state.finish()


@dp.message_handler(Command("jointhecourse"), state=None)
async def enter_test(message: types.Message):
    await message.reply("Выберете курс", reply_markup=course_markup)
    await RegisterForClasses.Q1.set()


@dp.message_handler(state=RegisterForClasses.Q1)
async def answer_q1(message: types.Message, state: FSMContext):
    answer = message.text
    try:
        cid = get_cid_by_name(answer)
        check = check_telegramdi_in_student_course(message.from_user.id, cid)
        if check:
            await message.answer("Вы уже записаны на курс!", reply_markup=ReplyKeyboardRemove())
        else:
            try:
                join_to_course(message.from_user.id, cid)
                await message.answer("Вы записаны на курс " + answer, reply_markup=ReplyKeyboardRemove())
            except:
                await message.answer("Сначала зарегистрируйся в системе! Введи /reg",
                                     reply_markup=ReplyKeyboardRemove())
    except:
        await message.answer("Попробуйте еще раз", reply_markup=ReplyKeyboardRemove())
    await state.finish()


@dp.message_handler(Command("infoaboutme"))
async def enter_test(message: types.Message):
    info = get_info_about_me(message.from_user.id)[0]
    await message.answer("{student[0]!r} {student[1]!r}\nНомер студенческого: {student[2]!r}\n" \
                         "Группа: {student[3]!r}".format(student=[info[1], info[2], info[3], info[4]]).replace("'", ''))


@dp.message_handler(Command("leavethecours"), state=None)
async def enter_test(message: types.Message):
    await message.reply("Какой курс вы хотите покинуть?", reply_markup=course_markup)
    await LeaveCourse.Q1.set()


@dp.message_handler(state=LeaveCourse.Q1)
async def answer_q1(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(answer1=answer)
    await message.answer("Вы уверены, что хотите покинуть курс " + answer + "?\nЭто повлечет за собой удаление ваших "
                                                                            "оценок на курсе",
                         reply_markup=simple_answer_markup)
    await LeaveCourse.next()


@dp.message_handler(state=LeaveCourse.Q2)
async def answer_q2(message: types.Message, state: FSMContext):
    answer = message.text
    data = await state.get_data()
    answer1 = data.get("answer1")
    if answer == 'Да':
        try:
            cid = get_cid_by_name(answer1)
            leave_course(message.from_user.id, cid)
            await message.answer('Вы покинули курс {}!'.format(answer1), reply_markup=ReplyKeyboardRemove())
        except:
            await message.answer('Что-то пошло не так....', reply_markup=ReplyKeyboardRemove())
    await state.finish()


# -------------------------------------------------------------------------------------------------------------


@dp.message_handler(Command("teacher"), state=None)
async def enter_test(message: types.Message):
    await message.reply("Выберете курс", reply_markup=course_markup)
    await RegistrationTeacherOnCourse.Q1.set()


@dp.message_handler(state=RegistrationTeacherOnCourse.Q1)
async def answer_q1(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(answer1=answer)
    await message.answer("Введите имя", reply_markup=ReplyKeyboardRemove())
    await RegistrationTeacherOnCourse.next()


@dp.message_handler(state=RegistrationTeacherOnCourse.Q2)
async def answer_q2(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(answer2=answer)
    await message.answer("Введите фамилию")
    await RegistrationTeacherOnCourse.next()


@dp.message_handler(state=RegistrationTeacherOnCourse.Q3)
async def answer_q3(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(answer3=answer)
    await message.answer("Введите пароль от курса")
    await RegistrationTeacherOnCourse.next()


@dp.message_handler(state=RegistrationTeacherOnCourse.Q4)
async def answer_q1(message: types.Message, state: FSMContext):
    data = await state.get_data()
    answer1 = data.get("answer1")
    answer2 = data.get("answer2")
    answer3 = data.get("answer3")
    answer = message.text
    try:
        check = check_course_pass(answer1, answer)
        if check:
            insert_new_teacher(message.from_user.id, answer2, answer3)
            insert_new_teacher_course(message.from_user.id, get_cid_by_name(answer1))
            await message.answer("Вы стали администратором курса " + answer1)
        else:
            await message.answer("Вы ввели неверный пароль")
    except:
        await message.answer("Не балуйся)")
    await state.finish()


@dp.message_handler()
async def bullshit(message: types.Message):
    await message.answer("Пиши по делу)")

# Вариант завершения 2
# await state.reset_state()

# Вариант завершения 3 - без стирания данных в data
# await state.reset_state(with_data=False)
