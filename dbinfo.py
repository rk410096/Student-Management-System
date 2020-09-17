from sqlite3 import *

def getcon():
    con=connect(database='ducat.db')
    return con

def create_table():
    try:
        con=getcon()
        cur=con.cursor()
        cur.execute("create table students(stu_id int(2) primary key,stu_name text(50),stu_mob text(10),stu_email text(50),stu_course text(20),course_fee int(2),stu_amt int(2),reg_date date)")
        cur.execute("create table course(course_name text(20) primary key,course_fee int(2))")
        con.commit()
        con.close()
        print('table created...')
    except:
        print('table already exists')


def getnextid():
    con=getcon()
    cur=con.cursor()
    cur.execute("select max(stu_id) from students")
    sid=cur.fetchone()[0]
    if(sid==None):
        sid=1001
        return sid
    else:
        sid=sid+1
        return sid
    con.close()

