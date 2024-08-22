from tkinter import *
from tkinter import PhotoImage
from datetime import *
from subprocess import call
import os


def reservation_():
    root.destroy()
    call(["python", "reservationwindow.py"])

def admin():
    root.destroy()
    call(["python", "admintype.py"])

def register():

    global name
    global username
    global password

    global username_entry
    global password_entry
    global name_entry

    username = StringVar()
    password = StringVar()
    name = StringVar()

    register_screen.configure(bg='#0B3861')
    font_format = ('Mayeka Regular Demo', 10)
    bg_color = '#0B243B'
    Label(register_screen, text='', bg='#0B3861').pack()
    Label(register_screen, text='WELCOME', bg='#0B3861', fg='white', font=('Timeline', 20)).pack()
    Label(register_screen, text='', bg='#0B3861').pack()
    Canvas(register_screen, width=300, height=230, bg=bg_color, bd=0, highlightthickness=0).pack()
    Label(register_screen, text='REGISTER', bg=bg_color, fg='white', font=('Mayeka Regular Demo', 13)).place(x=41, y=105)
    Label(register_screen, text="Name: ", bg=bg_color, fg='white', font=font_format).place(x=41, y=130)
    name_entry = Entry(register_screen, textvariable=name, font=font_format)
    name_entry.place(x=45, y=150, height=23, width=210)
    Label(register_screen, text="Username: ", bg=bg_color, fg='white', font=font_format).place(x=41, y=173)
    username_entry = Entry(register_screen, textvariable=username, font=font_format)
    username_entry.place(x=45, y=193, height=23, width=210)
    Label(register_screen, text="Password: ", bg=bg_color, fg='white', font=font_format).place(x=41, y=216)
    password_entry = Entry(register_screen, textvariable=password, show='•')
    password_entry.place(x=45, y=236, height=23, width=210)
    Button(register_screen, text="REGISTER", font=font_format, bg='#0B3861', fg='white', borderwidth=0,command=register_user).place(relx=0.5, rely=0.91, anchor=CENTER, width=210)
    al_acc=Button(register_screen, text='Already Have Account', bg=bg_color, fg='white', font=('Mayeka Regular Demo', 7),width=17, borderwidth=0)
    al_acc['command']=lambda: [ root.destroy(),main_screen()]
    al_acc.place(relx=0.64, rely=0.96)


def login():

    global username_verify
    global password_verify

    username_verify = StringVar()
    password_verify = StringVar()

    global username_login_entry
    global password_login_entry

    global username_error
    global password_error

    login_screen.configure(bg='#0B3861')
    font_format = ('Mayeka Regular Demo', 10)
    bg_color = '#0B243B'
    Label(login_screen, text='', bg='#0B3861').pack()
    Label(login_screen, text='WELCOME', bg='#0B3861', fg='white', font=('Timeline', 20)).pack()
    Label(login_screen, text='', bg='#0B3861').pack()
    Canvas(login_screen, width=300, height=210, bg=bg_color, bd=0, highlightthickness=0).pack()
    Label(login_screen, text='LOGIN', bg=bg_color, fg='white', font=('Mayeka Regular Demo', 13)).place(x=41, y=105)
    Label(login_screen, text="Username: ", bg=bg_color, fg='white', font=font_format).place(x=41, y=135)
    username_login_entry = Entry(login_screen, textvariable=username_verify, font=font_format)
    username_login_entry.place(x=45, y=155, height=23, width=210)
    Label(login_screen, text="Password: ", bg=bg_color, fg='white', font=font_format).place(x=41, y=180)
    password_login_entry = Entry(login_screen, textvariable=password_verify, show='•')
    password_login_entry.place(x=45, y=200, height=23, width=210)
    cre_acc=Button(login_screen, text='Create Account', bg=bg_color, fg='white', font=('Mayeka Regular Demo', 7), width=12,borderwidth=0)
    cre_acc['command'] = lambda: [register(), login_screen.destroy()]
    cre_acc.place(relx=0.73, rely=0.95)
    Button(login_screen, text="LOGIN", font=font_format, bg='#0B3861', fg='white', borderwidth=0,command=login_verify).place(relx=0.5, rely=0.86, anchor=CENTER, width=210)
    admin_f()

def register_user():
    user_list = []
    name_info = name.get()
    username_info = str(username.get())
    password_info = str(password.get())
    file = open('userslist','r')
    line = file.readlines()
    for i in line:
        s = i.split()
        user_list.append(s[1])

    if ' ' in username_info:
        x = 'Invalid Username'
        register_cond(x)

        username_entry.delete(0, END)
        password_entry.delete(0, END)
        name_entry.delete(0, END)
    elif username_info not in user_list:
        if len(password_info) >= 5:
            file = open('userslist', "a")
            file.write(username_info + " ")
            file.write(name_info + " ")
            file.write(password_info + "\n")
            file.close()
            x = "Account Created!"
            register_cond(x)
        else:
            x = "Password is Short"
            register_cond(x)

    else:
        x = 'Username Already Exist'
        register_cond(x)


    username_entry.delete(0, END)
    password_entry.delete(0, END)
    name_entry.delete(0, END)
    name_entry.delete(0, END)
    file.close()


def register_cond(x):
    registered = Label(register_screen, text=x, fg="white", bg='#0B243B',font=('Mayeka Regular Demo', 10))
    registered.place(relx=0.5, rely=0.85, anchor=CENTER, width=210)
    registered.after(500, lambda: registered.destroy())
# Implementing event on login button

def admin_f():
    list_of_files = os.listdir()  # Accessing Files
    if 'userslist' not in list_of_files:
        file = open('userslist', 'a')
        file.write("admin admin admin\n")
        file.close()
    if 'reserved' not in list_of_files:
        file = open('reserved', 'a')
        file.close()

def login_verify():
    username1 = username_verify.get()
    password1 = password_verify.get()
    us=[]
    file = open('userslist', "r")
    users = file.readlines()
    for i in users:
        s=i.split()
        us.append(s[0])
        if username1 == s[0]:
            if password1 == s[2]:
                login_success = Label(login_screen, text="Login Success!", fg="white", bg='#0B243B',font=('Mayeka Regular Demo', 10))
                login_success.place(relx=0.5, rely=0.79, anchor=CENTER, width=210)
                login_record(username1)
                if s[1] == 'admin':   #admin name cant ba change only username and password
                    login_success.after(200, lambda: [admin()])
                else:
                    login_success.after(200, lambda: [reservation_()])

            elif password1 != s[2]:
                x = 'pass'
                error_iconS(x)
                password_login_entry.delete(0, END)
                break

    if username1 not in us:
        x = 'user'
        error_iconS(x)
        username_login_entry.delete(0, END)
        password_login_entry.delete(0, END)


def error_iconS(x):
    global username_eror
    username_error = Label(login_screen, image=error_icon, bg='#0B243B')
    if x=='pass':
        username_error.place(x=260, y=201)
    elif x == 'user':
        username_error.place(x=260, y=156)
    username_error.after(1000, lambda: username_error.destroy())

def login_record(un):
    username_ = un
    file = open('loginR', "a")
    file.write(username_ + " \n")
    file.close()

# Designing Main(first) window

def main_screen():
    global root
    global error_icon

    root = Tk()
    root.wm_title(' L A L A')
    root.wm_iconbitmap('sq.ico')
    root.geometry("530x350")
    root.geometry("+400+150")
    root.configure(bg='#0B3861')
    error_icon = PhotoImage(file='warning.png')

    global login_screen
    global register_screen
    login_screen = Frame(root)
    register_screen = Frame(root)

    for frame in (login_screen, register_screen):
        frame.pack()

    login()
    #register()

    root.mainloop()

main_screen()