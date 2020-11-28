import psycopg2

# не забыть поменять на системе
def connection():
    con = psycopg2.connect(
        database="pgbot",
        user="postgres",
        password="ZuzuZuzu",
        host="127.0.0.1",
        port="5432"
    )
    return con


def get_cid_by_name(cname):
    con = connection()
    cur = con.cursor()
    cur.execute("select cid from course where cname='{}'".format(cname))
    answer = cur.fetchall()
    con.close()
    return answer[0][0]


def check_telegramdi_in_student_course(sid, cid):
    con = connection()
    cur = con.cursor()
    cur.execute("select * from student_course where sid={student_course[0]!r} and cid={student_course[1]!r}".format(
        student_course=[sid, cid]))
    answer = cur.fetchall()
    con.close()
    return answer


def insert_new_student(sid, sname, ssurname, idcard, idgroup):
    con = connection()
    cur = con.cursor()
    sql_query = "insert into student (sid, sname, ssurname, idcard, idgroup) values ({student[0]!r}, {student[1]!r}, " \
                "{student[2]!r}, {student[3]!r}, {student[4]!r})".format(student=[sid, sname, ssurname, idcard, idgroup])
    cur.execute(sql_query)
    con.commit()
    con.close()


def join_to_course(sid, cid):
    con = connection()
    cur = con.cursor()
    sql_query = "insert into student_course (sid, cid) values ({student[0]!r}, {student[1]!r})".format(
        student=[sid, cid])
    cur.execute(sql_query)
    con.commit()
    con.close()


def insert_new_teacher(tid, tname, tsurname):
    con = connection()
    cur = con.cursor()
    sql_query = "insert into teacher (tid, tname, tsurname) values ({teacher[0]!r}, {teacher[1]!r}, {teacher[2]!r})".format(
        teacher=[tid, tname, tsurname])
    cur.execute(sql_query)
    con.commit()
    con.close()


def insert_new_teacher_course(tid, cid):
    con = connection()
    cur = con.cursor()
    sql_query = "insert into teacher_course (tid, cid) values ({teacher_course[0]!r}, {teacher_course[1]!r})".format(
        teacher_course=[tid, cid])
    cur.execute(sql_query)
    con.commit()
    con.close()


def check_course_pass(cname, cpass):
    con = connection()
    cur = con.cursor()
    cur.execute("select * from course where cname={course[0]!r} and cpass={course[1]!r}".format(
        course=[cname, cpass]))
    answer = cur.fetchall()
    con.close()
    return answer


def leave_course(sid, cid):
    con = connection()
    cur = con.cursor()
    sql_query = "delete from student_course where sid={} and cid={}".format(sid, cid)
    cur.execute(sql_query)
    con.commit()
    con.close()


def get_info_about_me(sid):
    con = connection()
    cur = con.cursor()
    cur.execute("select * from student where sid={}".format(sid))
    answer = cur.fetchall()
    con.close()
    return answer


def get_cid_by_tid(tid):
    con = connection()
    cur = con.cursor()
    cur.execute("select * from teacher_course where tid={}".format(tid))
    answer = cur.fetchall()
    con.close()
    return answer[0][1]


def get_list_of_student_from_cours(cid):
    con = connection()
    cur = con.cursor()
    cur.execute("select * from student_course where cid={}".format(cid))
    answer = cur.fetchall()
    con.close()
    return answer


def assign_grades(sid, cid, assessment):
    con = connection()
    cur = con.cursor()
    sql_query = "insert into journal(sid, cid, assessment) values ({journal[0]!r}, {journal[1]!r}, {journal[2]!r})".format(
        journal=[sid, cid, assessment])
    cur.execute(sql_query)
    con.commit()
    con.close()


def get_my_grades(sid, cid, option):
    con = connection()
    cur = con.cursor()
    if option == 1:
        cur.execute("select * from journal where cid={} and sid={}".format(cid, sid))
    else:
        cur.execute("select * from journal where cid={}".format(cid))
    answer = cur.fetchall()
    con.close()
    return answer




