from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from keyboards.reply.choice_buttons import course_markup, simple_answer_markup, to_set_markup
from aiogram.types import ReplyKeyboardRemove
from loader import dp
from queries import insert_new_student, check_telegramdi_in_student_course, get_cid_by_name, join_to_course, \
    check_course_pass, insert_new_teacher, insert_new_teacher_course, leave_course, get_info_about_me, get_cid_by_tid, \
    get_list_of_student_from_cours, assign_grades, get_my_grades
from states import Registration, RegistrationTeacherOnCourse, LeaveCourse, GetGrades
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
                         "3)/infoaboutme - получить информацию о себе\n"
                         "4)/getmygrades получить оценки по предмету\n"
                         "5)/leavethecours - покинуть курс\n"
                         "*Команды для преподавателя:\n"
                         "1)/teacher - стать администратором курса\n"
                         "2)/liststudents - получить excel файл с списком студентов, для выставления оценок\n"
                         "3)/assigngrades - выставить оценки из файла пункта (2)\n"
                         "4)/getjurnal - получить журнал с оценками")


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


@dp.message_handler(Command("getmygrades"), state=None)
async def get_grades(message: types.Message):
    await message.reply("Оценки по какому предмету вы хотите получить?", reply_markup=course_markup)
    await GetGrades.Q1.set()


@dp.message_handler(state=GetGrades.Q1)
async def answer_q1(message: types.Message, state: FSMContext):
    try:
        answer = message.text
        cid = get_cid_by_name(answer)
        grades = get_my_grades(message.from_user.id, cid, 1)
        g = []
        for i in grades:
            g.append(i[3])
        strgrades = str(g)
        await message.answer("Ваши оценки " + strgrades, reply_markup=ReplyKeyboardRemove())
    except:
        await message.answer('Что-то пошло не так....')
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


@dp.message_handler(Command("liststudents"))
async def enter_test(message: types.Message):
    try:
        cid = get_cid_by_tid(message.from_user.id)
        list_of_students = get_list_of_student_from_cours(cid)
        list_of_surnames = []
        list_of_idcards = []
        list_of_groupnumbers = []
        list_of_grades = []
        for i in list_of_students:
            a = get_info_about_me(i[0])[0]
            list_of_surnames.append(a[2])
            list_of_idcards.append(a[3])
            list_of_groupnumbers.append(a[4])
            list_of_grades.append('')
        df = pd.DataFrame(
            {'Фамилия': list_of_surnames, 'Номер студенческого': list_of_idcards, 'Группа': list_of_groupnumbers,
             'Оценка': list_of_grades})
        df.to_excel(r"Оценки.xlsx")
        await message.answer("В папку проекта сохранен Excel файл 'Оценки', откройте его и выставите оценки, "
                             "после сохраните "
                             "изменения и вызовите команду '/assigngrades'")
    except:
        await message.answer('Что-то пошло не так...')


@dp.message_handler(Command("assigngrades"))
async def answer_q1(message: types.Message, state: FSMContext):
    try:
        df2 = pd.read_excel(r"Оценки.xlsx")
        grades = []
        for i in df2['Оценка']:
            grades.append(i)
        cid = get_cid_by_tid(message.from_user.id)
        list_of_students = get_list_of_student_from_cours(cid)
        for i in range(0, len(list_of_students)):
            try:
                if math.isnan(grades[i]):
                    assign_grades(list_of_students[i][0], cid, 0)
                else:
                    assign_grades(list_of_students[i][0], cid, grades[i])
            except:
                pass
        await message.answer('Оценки выставлены!')
    except:
        await message.answer('Не удалось найти файл с оценками')


@dp.message_handler(Command("getjurnal"))
async def enter_test(message: types.Message):
    try:
        cid = get_cid_by_tid(message.from_user.id)
        list_of_students = get_list_of_student_from_cours(cid)
        grades = []
        students_surnames = []
        students_idcards = []
        students_groups = []
        for i in list_of_students:
            g = []
            student = get_info_about_me(i[0])[0]
            students_surnames.append(student[2])
            students_idcards.append(student[3])
            students_groups.append(student[4])
            for j in get_my_grades(i[0], cid, 1):
                g.append(j[3])
            grades.append(g)
        lens = []
        for i in grades:
            lens.append(len(i))
        max_len = max(lens)
        for j in grades:
            if len(j) < max_len:
                while len(j) < max_len:
                    j.insert(0, 0)
        a = np.array(grades)
        df_grades = pd.DataFrame(a)
        df = pd.DataFrame(
            {'Фамилия': students_surnames, 'Номер студенческого': students_idcards, 'Группа': students_groups})
        answer = pd.merge(df, df_grades, left_index=True, right_index=True)
        answer.to_excel(r"Журнал.xlsx")
        await message.answer
    except:
        await message.answer('....')


@dp.message_handler()
async def bullshit(message: types.Message):
    await message.answer("Пиши по делу)")

# Вариант завершения 2
# await state.reset_state()

# Вариант завершения 3 - без стирания данных в data
# await state.reset_state(with_data=False)
