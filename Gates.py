import sqlite3
import tkinter
import tkinter.messagebox as tk
from tkinter.font import Font
from easygui import *
from tkinter import *
from turtle import *
import random

conn = sqlite3.connect('requests.db')
cur = conn.cursor()

def AdminLogin():
    message = "Enter Username and Password"
    title = "Admin Login"
    fieldnames = ["Username", "Password"]
    field = []
    field = multpasswordbox(message, title, fieldnames)
    if field[0] == 'admin' and field[1] == 'admin':
        tkinter.messagebox.showinfo("Admin Login", "Login Successfully")
        adminwindow()
    else:
        tk.showerror("Error info", "Incorrect username or password")


def StudentLogin():
    message = "Enter Student ID and Password"
    title = "Student Login"
    fieldnames = ["Student ID", "Password"]
    field = []
    field = multpasswordbox(message, title, fieldnames)

    for row in conn.execute('SELECT * FROM student'):
        if field[0] == row[0] and field[1] == row[3]:
            global login
            login = field[0]
            f = 1
            print("Success")
            tkinter.messagebox.showinfo("Student Login", "Login Successfully")
            StudentLoginWindow()
            break
    if not f:
        print("Invalid")
        tk.showerror("Error info", "Incorrect student id or password")

def Studentlogout():
    global login
    login = -1
    LoginWindow.destroy()


def StudentRequestStatus():
    global requestStatus
    requestStatus = []
    for i in conn.execute('SELECT * FROM status where student_id=?', login):
        requestStatus = i

    WindowStatus()


def StudentAllStatus():
    allStatus = Toplevel()
    txt = Text(allStatus)
    for i in conn.execute('SELECT * FROM status where student_id=?', login):
        txt.insert(INSERT, i)
        txt.insert(INSERT, '\n')

    txt.pack()


def StudentInformationWindow():
    studentInformation = Toplevel()
    txt = Text(studentInformation)
    for i in conn.execute('SELECT student_id,Name,ContactNumber FROM student where student_id=?', login):
        txt.insert(INSERT, i)
        txt.insert(INSERT, '\n')

    txt.pack()


def StudentAllInformationWindow():
    allStudentInformation = Toplevel()
    txt = Text(allStudentInformation)
    for i in conn.execute('SELECT student_id,Name,ContactNumber FROM student'):
        txt.insert(INSERT, i)
        txt.insert(INSERT, '\n')

    txt.pack()


def WindowStatus():
    StatusWindow = Toplevel()
    label_1 = Label(StatusWindow, text="Student ID=", fg="blue", justify=LEFT, font=("Calibri", 16))
    label_2 = Label(StatusWindow, text=requestStatus[1], font=("Calibri", 16))
    label_3 = Label(StatusWindow, text="Type=", fg="blue", font=("Calibri", 16), justify=LEFT)
    label_4 = Label(StatusWindow, text=requestStatus[2], font=("Calibri", 16))
    label_5 = Label(StatusWindow, text="Date=", fg="blue", font=("Calibri", 16), justify=LEFT)
    label_6 = Label(StatusWindow, text=requestStatus[3], font=("Calibri", 16))
    label_7 = Label(StatusWindow, text="end=", fg="blue", font=("Calibri", 16), justify=LEFT)
    label_8 = Label(StatusWindow, text=requestStatus[4], font=("Calibri", 16))
    label_9 = Label(StatusWindow, text="Status:", fg="blue", font=("Calibri", 16), justify=LEFT)
    label_10 = Label(StatusWindow, text=requestStatus[6], font=("Calibri", 16))
    label_11 = Label(StatusWindow, text="Request_id:", fg="blue", font=("Calibri", 16), justify=LEFT)
    label_12 = Label(StatusWindow, text=requestStatus[0], font=("Calibri", 16))
    label_11.grid(row=0, column=0)
    label_12.grid(row=0, column=1)
    label_1.grid(row=1, column=0)
    label_2.grid(row=1, column=1)
    label_3.grid(row=2, column=0)
    label_4.grid(row=2, column=1)
    label_5.grid(row=3, column=0)
    label_6.grid(row=3, column=1)
    label_7.grid(row=4, column=0)
    label_8.grid(row=4, column=1)
    label_9.grid(row=5, column=0)
    label_10.grid(row=5, column=1)




def apply():
    message = "Enter the following details "
    title = "Request Apply"
    fieldNames = ["Student ID", "Date", "Require?", "Reason"]
    fieldValues = []
    fieldValues = multenterbox(message, title, fieldNames)
    message1 = "Select type of request"
    title1 = "Type of Request"
    choices = ["Bonafide Certificate", "Study Certificate", "Authentication"]
    choice = choicebox(message1, title1, choices)
    requestid = random.randint(1, 1000)
    conn.execute("INSERT INTO status(request_id,student_id,request,Date1,Date2,days,status) VALUES (?,?,?,?,?,?,?)",
                 (requestid, fieldValues[0], choice, fieldValues[1], fieldValues[2], fieldValues[3], "Pending"))
    conn.commit()

def RequestApproval():
    message = "Enter Request_id"
    title = "Request approval"
    fieldNames = ["Request_id"]
    fieldValues = []
    fieldValues = multenterbox(message, title, fieldNames)
    message1 = "Approve/Deny"
    title1 = "Request approval"
    choices = ["approve", "deny"]
    choice = choicebox(message1, title1, choices)

    conn.execute("UPDATE status SET status = ? WHERE request_id= ?", (choice, fieldValues[0]))
    conn.commit()

    if choice == 'approve':
        print(0)
        cur.execute("SELECT request FROM status WHERE request_id=?", (fieldValues[0],))
        row = cur.fetchall()
        col = row

        for row in conn.execute("SELECT student_id FROM status WHERE request_id=?", (fieldValues[0],)):
            print(2)
            exampleId = row[0]

        for row in conn.execute("SELECT days FROM status WHERE request_id=?", (fieldValues[0],)):
            print(2)
            exampleDays = row[0]



def requestlist():
    requestlistwindow = Toplevel()
    txt = Text(requestlistwindow)
    for i in conn.execute('SELECT * FROM status'):
        txt.insert(INSERT, i)
        txt.insert(INSERT, '\n')

    txt.pack()


def registration():
    message = "Enter Details of Student"
    title = "Registration"
    fieldNames = ["Student ID", "Name", "Contact Number", "Password"]
    fieldValues = []
    fieldValues = multpasswordbox(message, title, fieldNames)
    while 1:
        if fieldValues == None: break
        errmsg = ""
        for i in range(len(fieldNames)):
            if fieldValues[i].strip() == "":
                errmsg = errmsg + ('"%s" is a required field.\n\n' % fieldNames[i])

        if errmsg == "": break


        fieldValues = multpasswordbox(errmsg, title, fieldNames, fieldValues)
    conn.execute("INSERT INTO student(student_id,Name,ContactNumber,Password) VALUES (?,?,?,?)",
                 (fieldValues[0], fieldValues[1], fieldValues[2], fieldValues[3]))


    conn.commit()


def StudentLoginWindow():
    # employee login window after successful login
    global LoginWindow
    LoginWindow = Toplevel()
    LoginWindow.wm_attributes('-fullscreen', '1')
    Background_Label = Label(LoginWindow, image=filename)
    Background_Label.place(x=0, y=0, relwidth=1, relheight=1)

    informationEmployee = Button(LoginWindow, text='Student information', command=StudentInformationWindow, bd=12, relief=GROOVE, fg="blue", bg="#FAEBD7",
                      font=("Calibri", 36, "bold"), pady=3)
    informationEmployee['font'] = BtnFont
    informationEmployee.pack(fill=X)

    submit = Button(LoginWindow, text='Submit Requests', command=apply, bd=12, relief=GROOVE, fg="blue", bg="#FAEBD7",
                      font=("Calibri", 36, "bold"), pady=3)
    submit['font'] = BtnFont
    submit.pack(fill=X)


    RequestApplicationStatus = Button(LoginWindow, text='Last Request Status', command=StudentRequestStatus, bd=12, relief=GROOVE, fg="blue", bg="#FAEBD7",
                      font=("Calibri", 36, "bold"), pady=3)
    RequestApplicationStatus['font'] = BtnFont
    RequestApplicationStatus.pack(fill=X)

    AllLeaveStatus = Button(LoginWindow, text='All Requests Status', command=StudentAllStatus, bd=12, relief=GROOVE, fg="blue", bg="#FAEBD7",
                      font=("Calibri", 36, "bold"), pady=3)
    AllLeaveStatus['font'] = BtnFont
    AllLeaveStatus.pack(fill=X)


    LogoutBtn = Button(LoginWindow, text='Logout', bd=12, relief=GROOVE, fg="red", bg="#FAEBD7",
                      font=("Calibri", 36, "bold"), pady=3, command=Studentlogout)
    LogoutBtn['font'] = BtnFont
    LogoutBtn.pack(fill=X)

    informationEmployee.pack()
    submit.pack()

    RequestApplicationStatus.pack()
    AllLeaveStatus.pack()
    LogoutBtn.pack()
    ExitBtn.pack()



def adminwindow():
    adminmainwindow = Toplevel()
    adminmainwindow.wm_attributes('-fullscreen', '1')
    Background_Label = Label(adminmainwindow, image=filename)

    Background_Label.place(x=0, y=0, relwidth=1, relheight=1)
    informationEmployee = Button(adminmainwindow, text='All Students information', command=StudentAllInformationWindow, bd=12, relief=GROOVE, fg="blue", bg="#FAEBD7",
                      font=("Calibri", 36, "bold"), pady=3)
    informationEmployee['font'] = BtnFont
    informationEmployee.pack(fill=X)



    LeaveListButton = Button(adminmainwindow, text='Request approval list', command=requestlist, bd=12, relief=GROOVE, fg="blue", bg="#FAEBD7",
                      font=("Calibri", 36, "bold"), pady=3)
    LeaveListButton['font'] = BtnFont
    LeaveListButton.pack(fill=X)

    ApprovalButton = Button(adminmainwindow, text='Approve Requests', command=RequestApproval, bd=12, relief=GROOVE, fg="blue", bg="#FAEBD7",
                      font=("Calibri", 36, "bold"), pady=3)
    ApprovalButton['font'] = BtnFont
    ApprovalButton.pack(fill=X)

    LogoutBtn = Button(adminmainwindow, text='Logout', command=adminmainwindow.destroy, bd=12, relief=GROOVE, fg="red",
                     bg="#FAEBD7",
                     font=("Calibri", 36, "bold"), pady=3)
    LogoutBtn['font'] = BtnFont
    LogoutBtn.pack(fill=X)

    informationEmployee.pack()
    LeaveListButton.pack()
    ApprovalButton.pack()
    ExitBtn.pack()


root = Tk()
root.wm_attributes('-fullscreen', '1')
root.title("Gates E-Application Services")

filename = PhotoImage(file="background2.gif")
background_label = Label(root, image=filename)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
BtnFont = Font(family='Calibri(Body)', size=20)
MainLabel = Label(root, text="Gates E-Application Services", bd=12, relief=GROOVE, fg="White", bg="gray",
                      font=("Calibri", 36, "bold"), pady=3)
MainLabel.pack(fill=X)
im = PhotoImage(file='login.gif')

AdminLgnBtn = Button(root, text='Admin login',  bd=12, relief=GROOVE, fg="blue", bg="#FAEBD7",
                      font=("Calibri", 36, "bold"), pady=3, command=AdminLogin)
AdminLgnBtn['font'] = BtnFont
AdminLgnBtn.pack(fill=X)


LoginBtn = Button(root, text='Student login', bd=12, relief=GROOVE, fg="blue", bg="#FAEBD7",
                      font=("Calibri", 36, "bold"), pady=3, command=StudentLogin)
LoginBtn['font'] = BtnFont
LoginBtn.pack(fill=X)


StudentRegistration = Button(root, text='Student registration', command=registration, bd=12, relief=GROOVE, fg="blue", bg="#FAEBD7",
                      font=("Calibri", 36, "bold"), pady=3)
StudentRegistration['font'] = BtnFont
StudentRegistration.pack(fill=X)

ExitBtn = Button(root, text='Exit', command=root.destroy, bd=12, relief=GROOVE, fg="red", bg="#FAEBD7",
                      font=("Calibri", 36, "bold"), pady=3)
ExitBtn['font'] = BtnFont
ExitBtn.pack(fill=X)
MainLabel.pack()
AdminLgnBtn.pack()
LoginBtn.pack()
StudentRegistration.pack()
ExitBtn.pack()


root.mainloop()


