from tkinter import *
from tkinter.ttk import Combobox
from tkinter import PhotoImage
from subprocess import call
from time import strftime
from datetime import *
import datetime
from tkinter import messagebox

def login_window():
    main_screen.destroy()
    call(["python", "loginwindow.py"])

#date and time class
class DateTime:

    def __init__(f):
        print ('')

    def cafe_time(f):
        global time_open
        global time_close
        global number_of_pcs

        file = open('cafetime', 'r+')
        d = file.readlines()

        number_of_pcs = int(d[0])
        time_open = int(d[1])
        time_close=  int(d[2])

    def datetime_format(f):     #time and date drop-off choices
        #time 24 hour to 12 hour format
        for i in range (time_open, time_close+1):   # time open and time close (form cafe file)
            if i >= 12:
                if i == 12:
                    pc_time_info = str(i) + ' PM'
                else:
                    j = i - 12
                    pc_time_info = str(j) + ' PM'
            else:
                pc_time_info = str(i) + ' AM'
            to_time_list.append(pc_time_info)

        #weekdays and day format
        for i in range(7):
            date = datetime.datetime.today() + datetime.timedelta(days=i)
            date_list.append(str(date.strftime('%d'))+ ' • ' +date.strftime('%a'))
            FL_date.append(str(int(date.strftime('%d'))))

    def time_display(f):    #running date and time on screen
        #date and time format
        f.date_display1 = strftime('%a %d %b %Y')
        f.time_display1 = strftime('%I:%M:%S %p')
        #date counter
        date_fdisplay.config(text=f.date_display1)
        date_fdisplay.after(8600000, f.time_display)
        # time counter
        time_fdisplay.config(text=f.time_display1)
        time_fdisplay.after(1000, f.time_display)


class pc_reserve:

    def __init__(f):
        print ('')

    def varible_arr(f):
        global date_fl
        global stbtime
        global etbtime
        try:
            #if time_box0 != [] and time_box1 != [] and time_box2 != []:
            if time_box0.get()!='Date' and time_box1.get()!='From' and time_box2.get()!='To':
                date_f = time_box0.get()

                stbtime = int(time_box1.current())+time_open
                etbtime = int(time_box2.current())+time_open
                date_fl =date_f.replace(" • ", "-")

                la.pc_duplicatecheker()     #checking current date and time != previous date and time
            else:
                x = 'dt'
                f.error_move(x)
        except:
            x ='dt'
            f.error_move(x)

    def middle_screen(f):
        global time_fdisplay
        global date_fdisplay
        global time_box0
        global time_box1
        global time_box2

        # display list of choices (date and time)
        dt.datetime_format()

        # setting fonts #setting font for combobox listbox
        font = ('Mayeka Regular Demo', 11)
        main_screen.option_add('*TCombobox*Listbox.font',font)

        # computer terminals display
        Label(middle_frame, text='COMPUTER TERMINALS', font=font,
              bg=bg2).place(relx=0.01, rely=0.2)

        #basic instruction for first action
        Label(middle_frame, text='Please Select Date and Time first:', font=('Mayeka Regular Demo', 10),
              bg=bg2).place(relx=0.38, rely=0.25)

        # Date combobox
        time_box0 = Combobox(middle_frame, values=date_list, width=7,font=font, state=READABLE)
        time_box0.set('Date')
        time_box0.place(relx=0.595, rely=0.25)

        # from_time combobox
        time_box1 = Combobox(middle_frame, values=to_time_list, width=5,font=font, state=READABLE)
        time_box1.set('In')
        time_box1.place(relx=0.697, rely=0.25)

        # To Time Combobox
        time_box2 = Combobox(middle_frame, values=to_time_list, width=5,font=font, state=READABLE)
        time_box2.set('Out')
        time_box2.place(relx=0.778, rely=0.25)

        Label(middle_frame, text='-', font=font, bg=bg2).place(relx=0.765, rely=0.25) #dash between from and to

        #running date on screen
        date_fdisplay = Label(middle_frame, font=('Mayeka Regular Demo', 8), bg=bg4)
        date_fdisplay.place(relx=0.9, rely=0, width=100)

        # running time on screen
        time_fdisplay = Label(middle_frame, font=('Mayeka Regular Demo', 13), bg=bg4)
        time_fdisplay.place(relx=0.9, rely=0.46, width=100, height=25)

        #load button (refreshing pc)
        Go = Button(middle_frame, text='LOAD', font=('Mayeka Regular Demo', 9), width=6, bg='#AED9DF', relief=GROOVE,
                    command=f.varible_arr)
        Go.place(relx=0.85, rely=0.15, width=40, height=30)
        dt.time_display()

    def pc_screen(f):

        global PC
        global pc_area

        #logout button
        Button(bottom_frame, text='LOGOUT', font=('Mayeka Regular Demo', 11), bg='#8FBAC8',
               command=f.log_out_).place(relx=0.945, rely=0.95, anchor=S)
        #SCROLLBAL
        pc_area = Frame(bottom_frame, width=800, height=320)
        pc_area.place(relx=0.02, rely=0.05)

        canvas = Canvas(pc_area, width=800, height=320, borderwidth=0, highlightthickness=1.5,highlightbackground=bg2, bg=bg1)
        scroll = Scrollbar(pc_area, orient="vertical" ,command=canvas.yview)
        canvas.configure(yscrollcommand=scroll.set)

        # create a scrollbar
        can_frame = Frame(canvas,bg=bg1)
        canvas.grid()
        canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), anchor='nw', window= can_frame, width=800)
        scroll.grid(row=0, column=1, sticky='ns')

        row = int(number_of_pcs / 10)           #number of rows by dividing 10 (10pc per column)
        row_excess = int(number_of_pcs % 10)    #% of 10 (pc number at last)
        per_row = 10; line = 1                  #pc per column;  #counter

        for i in range(row):
            for j in range(per_row):
                Frame( can_frame, width=80, height=70, bg=bg1, highlightbackground='#CEE3F6',highlightthickness=1).grid(row=i, column=j)
                Label( can_frame, text=('PC', line), font=('Mayeka Regular Demo', 13), bg=bg1).grid(row=i, column=j,padx=0, pady=10,sticky='n')
                PC = Button(can_frame, text='RESERVE', width=6, font=('Mayeka Regular Demo', 9), bg='#AED9DF',relief=FLAT)

                PC.grid(row=i, column=j, padx=0, pady=7, sticky='s')
                PC.config(command=lambda PC=PC,x=line: [f.reserve_confirmation(PC,x)])  # command to reserve desire pc

                f.reserve_btn2(PC,line) #changing buton reserve to occupied

                line += 1               #PC Number counter

        for i in range(row_excess):     # row_excess % of 10
            Frame( can_frame, width=80, height=70, bg=bg1, highlightbackground=bg2,highlightthickness=1).grid(row=row + 1, column=i)
            Label( can_frame, text=('PC', line), font=('Mayeka Regular Demo', 13), bg=bg1).grid(row=row + 1, column=i, padx=0, pady=10, sticky='n')
            PC = Button( can_frame, text='RESERVE', width=6, font=('Mayeka Regular Demo', 9), bg=bg3,relief=FLAT)
            PC.grid(row=row + 1, column=i, padx=0, pady=7, sticky='s')
            PC['command'] = lambda PC=PC, x=line: [f.reserve_confirmation(PC, x)]   # command to reserve desire pc

            f.reserve_btn2(PC,line) #changing buttin reserve to occupied

            line += 1               #PC Number counter


    def reserve_btn2(f,PC,x):

        # changing colors of button, when pc is already occupied before
        if x in occupied_pc:
            PC["bg"] = bg5
            PC['text'] = 'OCCUPIED'     #turning reserve to occupied when pc already reserved
            PC['state'] = 'disabled'    #disabling, if user is blind
        else:
            PC["bg"] = bg3              #for relaoding, useful when user change date
            PC['text'] = 'RESERVE'

    def reserve_btn(f,PC,No):           # reserve for new
        global new_pc_number
        new_pc_number = No              # getting pc number for reservation
        la.pc_record()                  # recording pc date, time and pc number
        if PC['state'] == 'normal':     # changing pc state when user confirm
            PC["bg"] = bg5
            PC['text'] = 'OCCUPIED'
            PC['state'] = 'disabled'
        else:
            PC['state'] = "normal"      #actually this is for undo reservation, when user is careless


    def reserve_confirmation(f,PCC, x):
        #try and catch for errors
        try:
            if stbtime != '' and etbtime != '' and date_fl != '':   #date and time first, before reserve
                res_confirm = Toplevel(main_screen)                 #reserve confirmation
                res_confirm.geometry("300x150")
                res_confirm.geometry("+500+300")
                res_confirm.wm_iconbitmap('sq.ico')
                res_confirm.configure(bg='#EFFBFB')
                text = 'ARE YOU SURE YOU WANT \nTO RESERVE PC '+str(x)+'?'
                Label(res_confirm, text=text, font=('Mayeka Regular Demo', 11), bg='#EFFBFB').pack(pady=15)
                Button(res_confirm, text="Yes", font=('Mayeka Regular Demo', 11), bg='#8FBAC8', width=6,
                       command=lambda PC=PC: [f.reserve_btn(PCC,x), res_confirm.destroy()]).place(relx=0.20, rely=0.65,anchor=W)
                Button(res_confirm, text="Cancel", font=('Mayeka Regular Demo', 11), bg='#8FBAC8', width=6,
                       command=res_confirm.destroy).place(relx=0.80, rely=0.65, anchor=E)

        except :
            z = 'res'
            f.error_move(z)      #when user reserve without setting date and time


    def error_move(f,x):
        error_message = Toplevel(main_screen)
        error_message.geometry("350x150")
        error_message.geometry("+500+300")
        error_message.wm_iconbitmap('sq.ico')
        error_message.configure(bg='#EFFBFB')
        text = ''
        if x == 'res':                              #for reservation warning
            text = 'Please Set DATE and TIME First \nthen click LOAD'
        elif x == 'dt':                               #for date and time warning
            text = 'Set Date and Time Properly'

        Label(error_message, text=text, font=('Mayeka Regular Demo', 11),
              bg='#EFFBFB').place(relx=0.2, rely=0.25)
        Label(error_message, image=error_move, bg='#EFFBFB').place(relx=0.08, rely=0.20)
        Button(error_message, text="OK", font=('Mayeka Regular Demo', 11), bg='#8FBAC8', width=6,relief=GROOVE,
               command=error_message.destroy).pack(side='bottom', pady=25)

        #messagebox.showinfo("L A L A", text)

    def log_out_(f):
        log_out_screen = Toplevel(main_screen)
        log_out_screen.geometry("300x150")
        log_out_screen.geometry("+500+300")
        log_out_screen.wm_iconbitmap('sq.ico')
        log_out_screen.configure(bg='#EFFBFB')
        Label(log_out_screen, text='DO YOU WANT TO LOGOUT?', font=('Mayeka Regular Demo', 11), bg='#EFFBFB').pack(
            pady=25)
        Button(log_out_screen, text="Yes", font=('Mayeka Regular Demo', 11), bg='#8FBAC8', width=6,
               command=lambda: [login_window()]).place(relx=0.20, rely=0.65, anchor=W)
        Button(log_out_screen, text="Cancel", font=('Mayeka Regular Demo', 11), bg='#8FBAC8', width=6,
               command=log_out_screen.destroy).place(relx=0.80, rely=0.65, anchor=E)


class LALA:
    def __init__(f):
        global date_final
        global from_time_final
        global to_time_final
        global pc_num_final
        global from_time_int
        global to_time_int

    def pc_duplicatecheker(f):
        global occupied_pc
        occ_pc = []

        file = open('reserved', 'r+')
        d = file.readlines()           # lines inside file
        for i in d:
            s = i.split()
            if date_fl in s:
                for i in range(stbtime, etbtime): # time in to time out iteration
                    if str(i) in s:
                        k = int(s[1].strip('#'))
                        occ_pc.append(k)

        occupied_pc = list(set(occ_pc))  # removing duplicate numbers

        file.close()

        pc_area.destroy()   # refresing Computer Terminals (PC area)
        pc.pc_screen()      # refresing Computer Terminals (PC area)


    def pc_record(f):
        pc_num_final = str(new_pc_number)

        un = open('loginR', 'r')
        username_1 = un.readlines()[-1]
        username__ = username_1.split()
        file = open('reserved', "a")    #one file for all reserved shi
        file.write(date_fl + " ")
        file.write('#'+pc_num_final + " ") #pc number first
        file.write(username__[0] + " ")
        for i in range(stbtime, etbtime+1):#for time
            file.write(str(i) + ' ')
        file.write('\n')
        file.close()

    def remove_passeddate(f):
        #removes dates that are passed (range 1 week)
        today = date.today()
        yesterday2 = []
        for i in range(1, 7):
            yesterday = today - timedelta(days=i)
            yesterday2.append(str(yesterday.strftime('%d')) + '-' + yesterday.strftime('%a'))
        with open ('reserved','r') as file:
            lines = file.readlines()
        with open ('reserved','w') as file:
            for line in lines:
                s = line.split()
                if s[0] not in yesterday2:
                    file.write(line)


def upper_screen():
    #upper screen (titles)
    Label(top_frame, text='INTERNET CAFE RESERVATION', font=('Mayeka Regular Demo', 23), bg=bg1).place(relx=0.5, rely=0.5,anchor=CENTER)
    Label(top_frame, text='USER', font=('Mayeka Regular Demo', 12), bg=bg1).place(relx=0.001, rely=0.8, anchor=NW)

if __name__ == '__main__':

    #main screen
    main_screen = Tk()
    main_screen.wm_title('L A L A')
    main_screen.wm_iconbitmap('sq.ico')
    main_screen.geometry("1000x500")
    main_screen.geometry("+150+100")
    main_screen.resizable(width=False, height=False)
    error_move = PhotoImage(file="error.png")

    #all arround variables
    FL_date = []
    date_list = []
    to_time_list = []
    occupied_pc = []
    number_of_pcs =10
    bg1 = '#EFFBFB' #U blue
    bg2 = '#CEE3F6' #F blue
    bg3 = '#AED9DF' #blue green
    bg4 = '#A9D0F5' #blue
    bg5 = "#EFAFB4" #red
    bg6 = '#81F7D8'
    #primary frames
    top_frame = Frame(main_screen,width=1000, height=100,bg=bg1)
    top_frame.pack()
    middle_frame = Frame(main_screen, width=1000, height=40, bg=bg2)
    middle_frame.pack()
    bottom_frame = Frame(main_screen, width=1000, height=460, bg=bg1)
    bottom_frame.pack()

    dt = DateTime()
    pc = pc_reserve()
    la = LALA()
    upper_screen()              # top screen (contain titles)
    la.remove_passeddate()
    dt.cafe_time()
    pc.middle_screen()          # middle screen (commonly contian options)
    pc.pc_screen()              # pc area (computer terminals)

    mainloop()
