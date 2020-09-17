from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from dbinfo import *
from datetime import datetime
import re
create_table()

win=Tk()
win.state('zoomed')
win.configure(bg='powder blue')
win.title('Ducat')
win.resizable(width=False,height=False)

lbl_title=Label(win,text='Ducat Student Management System',font=('',40,'bold'),bg='powder blue',fg='red')
lbl_title.pack()


'''=================variable======================'''
v_fname=StringVar()
v_phoneno=StringVar()
v_email=StringVar()
#v_course=StringVar()


'''=========function for validating the mobile_no.================'''
def validate_phoneno(user_phoneno):
    if user_phoneno.isdigit():
        return True
    elif user_phoneno is "":
        return True
    else:
        messagebox.showinfo("info","only digits apply")
        return False
'''========================function for validating the email_id========='''
def isValidEmail(user_email):
    if len(user_email)>7:
        if re.match("^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$",user_email)!=None:
            return True
        return False
    else:
        messagebox.showinfo("info","not valid email id")
        return False
'''=============all field validation======='''
def validateAll():
    if v_fname.get()=="":
        messagebox.showinfo("info","enter fullname")
    elif v_phoneno.get()=="":
        messagebox.showinfo("info","enter phone no")
    elif len(v_phoneno.get())!=10:
        messagebox.showinfo("info","enter 10 digit phone no")
    elif v_email.get()=="":
        messagebox.showinfo("info","enter email id to process")
    #elif v_course.get()=="" or v_course.get()=="Select your course":
        #messagebox.showinfo("info","enter your course")
    elif v_email.get()!="":
        status=isValidEmail(v_email.get())
        if(status):
            messagebox.showinfo("info","enter registered succsess")
    else:
        messagebox.showinfo("info","user registerde succsess")


def due_amt_db(e):
    sid=int(e.get())
    con=getcon()
    cur=con.cursor()
    cur.execute("select course_fee,stu_amt from students where stu_id=?",(sid,))
    row=cur.fetchone()
    if(row==None):
        messagebox.showwarning("balance","Student does not exist on this id")
    else:   
        messagebox.showinfo("Balance",f"Due Amount : {row[0]-row[1]}")    
    con.close()
def deposit_fee_db(e1,e2):
    sid=int(e1.get())
    amt=int(e2.get())
    con=getcon()
    cur=con.cursor()
    cur.execute("select course_fee,stu_amt from students where stu_id=?",(sid,))
    row=cur.fetchone()
    if(row==None):
        messagebox.showwarning("Fee Deposit",'Student does not exist on this id')
    else:
        if(row[1]<row[0]):
            if(row[0]>=(amt+row[1])):
                cur.execute("update students set stu_amt=stu_amt+? where stu_id=?",(amt,sid))
                messagebox.showinfo("Fee Deposit",'Fee Deposited')
                con.commit()
            else:
                messagebox.showinfo("Fee Deposit",'Deposited amount is not valid')
        else:
            messagebox.showwarning("Fee Deposit",'Already fullpaid')
    con.close()
def update_stu_db(e1,e2,e3,e4,e5):
    sid=e1.get()
    name=e2.get()
    mob=e3.get()
    email=e4.get()
    course=e5.get()
    print(sid,name,mob,email,course)
    con=getcon()
    cur=con.cursor()
    cur.execute("""update students set stu_name=?, stu_mob=?, stu_email=?, stu_course=? where stu_id=?""",(name,mob,email,course,sid))
    con.commit()
    con.close()
    messagebox.showinfo("Update Student","Student Record Updated...")

def search_stu_db(frm,e):
    sid=int(e.get())
    con=getcon()
    cur=con.cursor()
    cur.execute("select stu_id,stu_name,stu_mob,stu_course,course_fee from students where stu_id=?",(sid,))
    row=cur.fetchone()
    if(row==None):
        messagebox.showwarning("Student Search","Student Id does not exit")
    else:
        details="Id\tName\tMobile\tCourse\tCourse fee\n"
        details=details+f"{str(row[0])}\t{row[1]}\t{row[2]}\t{row[3]}\t{row[4]}"
        messagebox.showinfo("Student Search",details)
        option=messagebox.askyesno("Update Student", message="Do you want to update student?")
        if(option==True):
            updatescreen(frm,sid)
            
def reg_db(e1,e2,e3,e4,e5,e6):
    validateAll()
    name=e1.get()
    mob=e2.get()
    email=e3.get()
    course=e4.get()
    fee=int(e5.get())
    amt=int(e6.get())
    if(amt>fee):
        messagebox.showwarning('Student Reg','amount must be equal or less than course fee')
        return
    dt=datetime.now().date()
    sid=getnextid()
    con=getcon()
    cur=con.cursor()
    cur.execute("insert into students values(?,?,?,?,?,?,?,?)",(sid,name,mob,email,course,fee,amt,dt))
    con.commit()
    messagebox.showinfo('Student Reg',f'Student Registered Successfully With Id:{sid} ')
    e1.delete(0,END)
    e2.delete(0,END)
    e3.delete(0,END)
    e4.delete(0,END)
    e5.delete(0,END)
    e6.delete(0,END)
    
    e1.focus()

def course_db(e1,e2):
    name=e1.get()
    fee=int(e2.get())
    con=getcon()
    cur=con.cursor()
    cur.execute("insert into course values(?,?)",(name,fee))
    con.commit()
    messagebox.showinfo('Course Add',f'Course Added Successfully With Name:{name} ')
    e1.delete(0,END)
    e2.delete(0,END)
    e1.focus()
    
def reset(e1,e2):
    e1.delete(0,END)
    e2.delete(0,END)
    e1.focus()


def logout(frm):
    frm.destroy()
    homescreen()

def login(frm,e1,e2):
    u=e1.get()
    p=e2.get()
    if(len(u)==0 or len(p)==0):
        messagebox.showwarning('Warning','Username or Password can not be empty ')
    else:
        if(u=='admin' and p=='admin'):
            messagebox.showinfo('Success','Welcome,Admin')
            frm.destroy()
            welcomescreen()
        else:
            messagebox.showerror('Error','Invalid Username or Password')



def back(frm):
    frm.destroy()
    welcomescreen()

def coursescreen(wfrm):
    wfrm.destroy()
    frm=Frame(win,bg='pink')
    frm.place(x=0,y=100,relwidth=1,relheight=1)

    lbl_add=Label(frm,text='ADD COURSE DETAILS',font=('',20,'bold'),bg='pink')
    lbl_add.pack()

    btn_logout=Button(frm,command=lambda:logout(frm),text='logout',font=('',15,'bold'),bd=5,width=8)
    btn_logout.place(relx=.9,y=10)

    btn_back=Button(frm,command=lambda:back(frm),text='back',font=('',15,'bold'),bd=5,width=8)
    btn_back.place(x=10,y=10)

    lbl_cname=Label(frm,text='Course Name:',font=('',20,'bold'),bg='pink')
    lbl_cname.place(relx=.3,rely=.1)
    entry_cname=Entry(frm,font=('',15,'bold'),bd=5)
    entry_cname.place(relx=.47,rely=.1)
    entry_cname.focus()

    lbl_fee=Label(frm,text='Course Fee:',font=('',20,'bold'),bg='pink')
    lbl_fee.place(relx=.3,rely=.2)
    entry_fee=Entry(frm,font=('',15,'bold'),bd=5)
    entry_fee.place(relx=.47,rely=.2)

    btn_reg=Button(frm,text='Add',command=lambda:course_db(entry_cname,entry_fee),font=('',15,'bold'),bd=5,width=8)
    btn_reg.place(relx=.4,rely=.3)

    btn_reset=Button(frm,command=lambda:reset(entry_cname,entry_fee),text='reset',font=('',15,'bold'),bd=5,width=8)
    btn_reset.place(relx=.55,rely=.3)

def registerscreen(wfrm):
    wfrm.destroy()
    frm=Frame(win,bg='pink')
    frm.place(x=0,y=100,relwidth=1,relheight=1)

    lbl_welcome=Label(frm,text='Welcome:Admin',font=('',20,'bold'),bg='pink')
    lbl_welcome.place(x=10,y=10)

    btn_logout=Button(frm,command=lambda:logout(frm),text='logout',font=('',15,'bold'),bd=5,width=8)
    btn_logout.place(relx=.9,y=10)

    btn_back=Button(frm,command=lambda:back(frm),text='back',font=('',15,'bold'),bd=5,width=8)
    btn_back.place(x=10,y=50)

    lbl_name=Label(frm,text='Student Name:',font=('',20,'bold'),bg='pink')
    lbl_name.place(relx=.3,rely=.1)
    entry_name=Entry(frm,textvariable=v_fname,font=('',15,'bold'),bd=5)
    entry_name.place(relx=.47,rely=.1)
    entry_name.focus()

    lbl_mob=Label(frm,text='Student Mob:',font=('',20,'bold'),bg='pink')
    lbl_mob.place(relx=.3,rely=.2)
    entry_mob=Entry(frm,textvariable=v_phoneno,font=('',15,'bold'),bd=5)
    entry_mob.place(relx=.47,rely=.2)
    #=======register callback fun=====
    valid_phoneno=win.register(validate_phoneno)
    entry_mob.config(validate="key",validatecommand=(valid_phoneno,"%P"))
    
    lbl_email=Label(frm,text='Student Email:',font=('',20,'bold'),bg='pink')
    lbl_email.place(relx=.3,rely=.3)
    entry_email=Entry(frm,textvariable=v_email,font=('',15,'bold'),bd=5)
    entry_email.place(relx=.47,rely=.3)
    
    lbl_course=Label(frm,text='Course Name:',font=('',20,'bold'),bg='pink')
    lbl_course.place(relx=.3,rely=.4)
    entry_course=ttk.Combobox(frm, 
                            values=[
                                    "Python", 
                                    "Python+Django",
                                    "Python+ML",
                                    "Python+ML+AI"],font=('',14,'bold'))
    entry_course.place(relx=.47,rely=.4)

    lbl_fee=Label(frm,text='Course Fee:',font=('',20,'bold'),bg='pink')
    lbl_fee.place(relx=.3,rely=.5)
    entry_fee=Entry(frm,font=('',15,'bold'),bd=5)
    entry_fee.place(relx=.47,rely=.5)

    lbl_amt=Label(frm,text='Amount:',font=('',20,'bold'),bg='pink')
    lbl_amt.place(relx=.3,rely=.6)
    entry_amt=Entry(frm,font=('',15,'bold'),bd=5)
    entry_amt.place(relx=.47,rely=.6)
    
    btn_reg=Button(frm,text='Register',command=lambda:reg_db(entry_name,entry_mob,entry_email,entry_course,entry_fee,entry_amt),font=('',15,'bold'),bd=5,width=8)
    btn_reg.bind(validate_phoneno) 
    btn_reg.place(relx=.4,rely=.7)

    btn_reset=Button(frm,text='reset',font=('',15,'bold'),bd=5,width=8)
    btn_reset.place(relx=.55,rely=.7)


def updatescreen(wfrm,sid):
    wfrm.destroy()
    frm=Frame(win,bg='pink')
    frm.place(x=0,y=100,relwidth=1,relheight=1)

    lbl_welcome=Label(frm,text='Welcome:Admin',font=('',20,'bold'),bg='pink')
    lbl_welcome.place(x=10,y=10)

    btn_logout=Button(frm,command=lambda:logout(frm),text='logout',font=('',15,'bold'),bd=5,width=8)
    btn_logout.place(relx=.9,y=10)

    btn_back=Button(frm,command=lambda:back(frm),text='back',font=('',15,'bold'),bd=5,width=8)
    btn_back.place(x=10,y=50)

    con=getcon()
    cur=con.cursor()
    cur.execute("select stu_id,stu_name,stu_mob,stu_email,stu_course,course_fee,stu_amt from students where stu_id=?",(sid,))
    row=cur.fetchone()
    con.close()
    print(row)

    lbl_name=Label(frm,text='Student Name:',font=('',20,'bold'),bg='pink')
    lbl_name.place(relx=.3,rely=.1)
    entry_name=Entry(frm,font=('',15,'bold'),bd=5)
    entry_name.place(relx=.47,rely=.1)
    entry_name.insert(0,row[1])
    entry_name.focus()

    lbl_mob=Label(frm,text='Student Mob:',font=('',20,'bold'),bg='pink')
    lbl_mob.place(relx=.3,rely=.2)
    entry_mob=Entry(frm,font=('',15,'bold'),bd=5)
    entry_mob.place(relx=.47,rely=.2)
    entry_mob.insert(0,row[2])

    lbl_email=Label(frm,text='Student Email:',font=('',20,'bold'),bg='pink')
    lbl_email.place(relx=.3,rely=.3)
    entry_email=Entry(frm,font=('',15,'bold'),bd=5)
    entry_email.place(relx=.47,rely=.3)
    entry_email.insert(0,row[3])
    
    lbl_course=Label(frm,text='Course Name:',font=('',20,'bold'),bg='pink')
    lbl_course.place(relx=.3,rely=.4)
    entry_course=ttk.Combobox(frm, 
                            values=[
                                    f"{row[4]}",
                                    "Python", 
                                    "Python+Django",
                                    "Python+ML",
                                    "Python+ML+AI"],font=('',14,'bold'))
    entry_course.current(0)
    entry_course.place(relx=.47,rely=.4)
    
    lbl_id=Label(frm,text='Student Id:',font=('',20,'bold'),bg='pink')
    lbl_id.place(relx=.3,rely=.5)
    entry_id=Entry(frm,font=('',15,'bold'),bd=5)
    entry_id.place(relx=.47,rely=.5)
    entry_id.insert(0,sid)
    entry_id.config(state='readonly')

    lbl_amt=Label(frm,text='Amount Deposited:',font=('',20,'bold'),bg='pink')
    lbl_amt.place(relx=.3,rely=.6)
    entry_amt=Entry(frm,font=('',15,'bold'),bd=5)
    entry_amt.place(relx=.47,rely=.6)
    entry_amt.insert(0,row[6])
    entry_amt.config(state='readonly')

    btn_update=Button(frm,text='Update',command=lambda:update_stu_db(entry_id,entry_name,entry_mob,entry_email,entry_course),font=('',15,'bold'),bd=5,width=8)
    btn_update.place(relx=.4,rely=.7)

    btn_reset=Button(frm,text='reset',font=('',15,'bold'),bd=5,width=8)
    btn_reset.place(relx=.55,rely=.7)


def searchscreen(wfrm):
    wfrm.destroy()
    frm=Frame(win,bg='pink')
    frm.place(x=0,y=100,relwidth=1,relheight=1)

    lbl_welcome=Label(frm,text='Welcome:Admin',font=('',20,'bold'),bg='pink')
    lbl_welcome.place(x=10,y=10)

    btn_logout=Button(frm,command=lambda:logout(frm),text='logout',font=('',15,'bold'),bd=5,width=8)
    btn_logout.place(relx=.9,y=10)

    btn_back=Button(frm,command=lambda:back(frm),text='back',font=('',15,'bold'),bd=5,width=8)
    btn_back.place(x=10,y=50)

    lbl_name=Label(frm,text='Student Id:',font=('',20,'bold'),bg='pink')
    lbl_name.place(relx=.3,rely=.1)
    entry_name=Entry(frm,font=('',15,'bold'),bd=5)
    entry_name.place(relx=.47,rely=.1)
    entry_name.focus()

    
    btn_reg=Button(frm,text='Search',command=lambda:search_stu_db(frm,entry_name),font=('',15,'bold'),bd=5,width=8)
    btn_reg.place(relx=.4,rely=.2)

    btn_reset=Button(frm,command=lambda:reset(entry_name,entry_name),text='reset',font=('',15,'bold'),bd=5,width=8)
    btn_reset.place(relx=.55,rely=.2)


def depositscreen(wfrm):
    wfrm.destroy()
    frm=Frame(win,bg='pink')
    frm.place(x=0,y=100,relwidth=1,relheight=1)

    lbl_welcome=Label(frm,text='Welcome:Admin',font=('',20,'bold'),bg='pink')
    lbl_welcome.place(x=10,y=10)

    btn_logout=Button(frm,command=lambda:logout(frm),text='logout',font=('',15,'bold'),bd=5,width=8)
    btn_logout.place(relx=.9,y=10)

    btn_back=Button(frm,command=lambda:back(frm),text='back',font=('',15,'bold'),bd=5,width=8)
    btn_back.place(x=10,y=50)

    lbl_name=Label(frm,text='Student Id:',font=('',20,'bold'),bg='pink')
    lbl_name.place(relx=.3,rely=.1)
    entry_sid=Entry(frm,font=('',15,'bold'),bd=5) 
    entry_sid.place(relx=.47,rely=.1)
    entry_sid.focus()

    lbl_amt=Label(frm,text='Amount:',font=('',20,'bold'),bg='pink')
    lbl_amt.place(relx=.3,rely=.2)
    entry_amt=Entry(frm,font=('',15,'bold'),bd=5)
    entry_amt.place(relx=.47,rely=.2)
    entry_amt.focus()
    
    btn_reg=Button(frm,text='Deposit',command=lambda:deposit_fee_db(entry_sid,entry_amt),font=('',15,'bold'),bd=5,width=8)
    btn_reg.place(relx=.4,rely=.3)

    btn_reset=Button(frm,text='reset',font=('',15,'bold'),bd=5,width=8)
    btn_reset.place(relx=.55,rely=.3)




def dueamountscreen(wfrm):
    wfrm.destroy()
    frm=Frame(win,bg='pink')
    frm.place(x=0,y=100,relwidth=1,relheight=1)

    lbl_welcome=Label(frm,text='Welcome:Admin',font=('',20,'bold'),bg='pink')
    lbl_welcome.place(x=10,y=10)

    btn_logout=Button(frm,command=lambda:logout(frm),text='logout',font=('',15,'bold'),bd=5,width=8)
    btn_logout.place(relx=.9,y=10)

    btn_back=Button(frm,command=lambda:back(frm),text='back',font=('',15,'bold'),bd=5,width=8)
    btn_back.place(x=10,y=50)

    lbl_name=Label(frm,text='Student Id:',font=('',20,'bold'),bg='pink')
    lbl_name.place(relx=.3,rely=.1)
    entry_sid=Entry(frm,font=('',15,'bold'),bd=5)
    entry_sid.place(relx=.47,rely=.1)
    entry_sid.focus()
   
    btn_reg=Button(frm,text='Submit',command=lambda:due_amt_db(entry_sid),font=('',15,'bold'),bd=5,width=8)
    btn_reg.place(relx=.4,rely=.2)

    btn_reset=Button(frm,command=lambda:reset(entry_sid,entry_sid),text='reset',font=('',15,'bold'),bd=5,width=8)
    btn_reset.place(relx=.55,rely=.2)



def welcomescreen():
    frm=Frame(win,bg='pink')
    frm.place(x=0,y=100,relwidth=1,relheight=1)

    lbl_welcome=Label(frm,text='Welcome:Admin',font=('',20,'bold'),bg='pink')
    lbl_welcome.place(x=10,y=10)

    btn_logout=Button(frm,command=lambda:logout(frm),text='logout',font=('',15,'bold'),bd=5,width=8)
    btn_logout.place(relx=.9,y=10)

    btn_reg=Button(frm,text='Register New Student',command=lambda:registerscreen(frm),font=('',15,'bold'),bd=5,width=18)
    btn_reg.place(relx=.4,y=70)

    btn_search=Button(frm,text='Search Student',command=lambda:searchscreen(frm),font=('',15,'bold'),bd=5,width=18)
    btn_search.place(relx=.4,y=170)

    btn_update=Button(frm,text='Deposit Fee',command=lambda:depositscreen(frm),font=('',15,'bold'),bd=5,width=18)
    btn_update.place(relx=.4,y=270)

    btn_bal=Button(frm,text='Due Amount',command=lambda:dueamountscreen(frm),font=('',15,'bold'),bd=5,width=18)
    btn_bal.place(relx=.4,y=270)

    btn_cou=Button(frm,command=lambda:coursescreen(frm),text='Add Course',font=('',15,'bold'),bd=5,width=18)
    btn_cou.place(relx=.4,y=350)
def homescreen():
    frm=Frame(win,bg='pink')
    frm.place(x=0,y=100,relwidth=1,relheight=1)

    lbl_user=Label(frm,text='Username:',font=('',20,'bold'),bg='pink')
    lbl_user.place(x=500,y=100)

    lbl_pass=Label(frm,text='Password:',font=('',20,'bold'),bg='pink')
    lbl_pass.place(x=500,y=150)

    entry_user=Entry(frm,font=('',15,'bold'))
    entry_user.place(x=680,y=100)
    entry_user.focus()

    entry_pass=Entry(frm,font=('',15,'bold'),show='*')
    entry_pass.place(x=680,y=150)
    
    btn_login=Button(frm,command=lambda:login(frm,entry_user,entry_pass),text='login',font=('',15,'bold'),bd=5,width=8)
    btn_login.place(x=600,y=220)

    btn_reset=Button(frm,command=lambda:reset(entry_user,entry_pass),text='reset',font=('',15,'bold'),bd=5,width=8)
    btn_reset.place(x=780,y=220)

    
homescreen()
win.mainloop() 
