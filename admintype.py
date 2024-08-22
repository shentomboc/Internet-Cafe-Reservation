from tkinter import *
import tkinter.ttk as ttk
from tkinter import PhotoImage
from tkinter.ttk import Combobox
from subprocess import call
import os
from time import strftime
from datetime import *
import datetime


def login_window():
    main_screen.destroy()
    call(["python", "loginwindow.py"])

class preview_:
    def __init__(f):
        f.entry_frame = Frame(bottom_frame)  # WHOLE FRAME FOR PREVIEW TEXT
        f.entry_frame.place(relx=0.010, rely=0.02)
        f.notebook = ttk.Notebook(f.entry_frame)  # NOTEBOOK, FOR TASK TABS
        f.notebook.grid()

        f.style = ttk.Style()
        f.style.configure('Treeview.Heading', font=fontt)
        f.style.configure("mystyle.Treeview", font=fontt)
        f.style.configure('TNotebook', font=fontt)
        f.style.configure('TNotebook.Tab', font=fontt)

        Label(f.notebook, text = 'Select to Remove', font=('Typo Grotesk', 10)).place(relx=0.895, rely=0.076,anchor=S)

    def refresh(f):
        f.res_frame.destroy()
        f.vac_frame.destroy()
        f.reserve_tab()
        f.vancant_tab()

    def reserve_tab(f):
        global tree
        cafe_time()
        ci.options_display()
        # notebook for task tab
        f.res_frame = Frame(f.notebook)                     # reserved frame
        f.res_frame.grid()
        f.notebook.add(f.res_frame, text='RESERVED PC')  # reserved tab in notebook

        # reserve tab body
        f.tree = ttk.Treeview(f.res_frame,height=17,style = "mystyle.Treeview")
        f.tree.grid()
        f.tree.bind('<<TreeviewSelect>>', f.select)
        
        f.tree.tag_configure('odd', background='#D8D8D8')
        f.tree.tag_configure('even', background='#E6E6E6')

        scroll = Scrollbar(f.res_frame, orient='vertical',command=f.tree.yview)
        f.tree.configure(yscrollcommand=scroll.set)
        scroll.grid(row=0, column=1, sticky='ns')

        f.tree['columns'] = ('1','2','3','4','5','6','7')
        f.tree['show'] = 'headings'

        f.tree.column('1', width=50)
        f.tree.column('2', width=150)
        f.tree.column('3', width=50)
        f.tree.column('4', width=120)
        f.tree.column('5', width=80)
        f.tree.column('6', width=80)
        f.tree.column('7', width=150)

        f.tree.heading('1', text='#')
        f.tree.heading('2', text='Date')
        f.tree.heading('3', text='PC #')
        f.tree.heading('4', text='Status')
        f.tree.heading('5', text='From')
        f.tree.heading('6', text='To')
        f.tree.heading('7', text='User Name')

        # if 24 run converter here
        #reserved pc from files
        c=1
        f.sorter()
        f.no_av(x='r')
        file = open('reserved', 'r+')
        d = file.readlines()  # lines inside file

        for i in d:
            s = i.split()
            s1 = f.converter_(int(s[3]))
            s2 = f.converter_(int(s[-1]))
            ii = ' '.join(i.split())
            ss = {'-': ' • ','#':'# ', "A": "  A", "P": "  P"}
            s[0] = s[0].translate(str.maketrans(ss))
            s1 = s1.translate(str.maketrans(ss))
            s2 = s2.translate(str.maketrans(ss))
            s3 = s[1].translate(str.maketrans(ss))
            f.tree.insert('', 'end', text=(ii), values=(c,s[0],s3,'RESERVED',s1,s2,s[2]))
            c+=1

    def no_av(f,x):
        if os.stat('reserved').st_size == 0:
            if x == 'v':
                text = 'All PC is Vacant!'
                fr = f.vac_frame
            if x == 'r':
                text = 'No Reserved PC'
                fr =f.res_frame
            Label(fr, text=text,font = ('Mayeka Regular Demo', 30),bg='white',fg='light gray').place(relx=0.285, rely=0.4)

    def vancant_tab(f):

        f.vac_frame = Frame(f.notebook)  # vacant frame INSIDE NOTEBOOK
        f.vac_frame.grid()
        f.notebook.add(f.vac_frame, text='VACANT PC')  # vacant tab in notebook

        tree = ttk.Treeview(f.vac_frame, height=17, style="mystyle.Treeview",columns=("Tags"))
        tree.column("Tags", anchor="e")
        tree.grid()

        tree.tag_configure('odd', background='#D8D8D8')
        tree.tag_configure('even', background='#E6E6E6')
        tree.bind('<<TreeviewSelect>>', f.selectt)

        scroll = Scrollbar(f.vac_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scroll.set)
        scroll.grid(row=0, column=1, sticky='ns')

        tree['columns'] = ('1', '2', '3', '4', '5', '6')
        tree['show'] = 'headings'

        tree.column('1', width=60)
        tree.column('2', width=150)
        tree.column('3', width=80)
        tree.column('4', width=130)
        tree.column('5', width=130)
        tree.column('6', width=130)

        tree.heading('1', text='#')
        tree.heading('2', text='Date')
        tree.heading('3', text='PC #')
        tree.heading('4', text='Status')
        tree.heading('5', text='From')
        tree.heading('6', text='To')

        # vacant pc's
        c = 1
        f.vacant_()
        f.no_av(x='v')
        for i in f.vacc_:
            s = i.split()
            s1 = f.converter_(int(s[2]))
            s2 = f.converter_(int(s[-1]))
            ss = {'-': ' • ','#':'# ', "A": "  A", "P": "  P"}
            s[0] = s[0].translate(str.maketrans(ss))
            s1 = s1.translate(str.maketrans(ss))
            s2 = s2.translate(str.maketrans(ss))
            s3 = s[1].translate(str.maketrans(ss))
            tree.insert('', 'end', text=('L' + str(c)), values=(c, s[0], s3, 'VACANT', s1, s2))
            c += 1

    def selectt(f,event):
        if 'rem_btn' in globals():
            rem_btn.destroy()

    def diselect(f,event):
        if len(f.tree.selection()) > 0:
            f.tree.selection_remove(f.tree.selection()[0])

    def select(f, event):
        for item in f.tree.selection():
            remname = f.tree.item(item,"text")
        global rem_btn

        rem_btn=Button(f.entry_frame,image=rem_icon, text=' VACANT PC',bg='white', font=font1, relief=FLAT,compound='left')
        rem_btn.place(relx=0.8899, rely=0.07,anchor=S)
        rem_btn['command']=lambda:[f.remove_btn(remname)]
        rem_btn.bind('<Enter>', f.pointed)
        rem_btn.bind('<Leave>', f.non_pointed)
        #rem_btn.after(2000, lambda: [rem_btn.destroy()])


    def remove_btn(f,remname):
        remove_screen = Toplevel(main_screen)
        remove_screen.geometry("300x150")
        remove_screen.geometry("+500+300")
        remove_screen.wm_iconbitmap('sq.ico')
        remove_screen.configure(bg=bg1)
        remove_screen.resizable(width=False, height=False)
        Label(remove_screen, text='Vacant this PC?', font=font1, bg=bg1).pack(
            pady=25)
        Button(remove_screen, text="Yes", font=font1, bg=bg3, width=6,
               command=lambda: [f.remove_res(remname),remove_screen.destroy()]).place(relx=0.20, rely=0.65, anchor=W)
        Button(remove_screen, text="Cancel", font=font1, bg=bg3, width=6,
               command=remove_screen.destroy).place(relx=0.80, rely=0.65, anchor=E)
        rem_btn.after(2000, lambda: [rem_btn.destroy()])

    def remove_res(f,un):
        f.delete()
        with open("reserved", "r") as fi:
            lines = fi.readlines()
        with open("reserved", "w") as fi:
            for line in lines:
                if un not in line:
                    fi.write(line)
        fi.close()
        cafe_time()
        ci.options_display()
        f.no_av(x='r')
        f.no_av(x='v')
        f.refresh()

    def pointed(f,e):
        try:
            rem_btn['background'] = '#848484'
        except:
            pass

    def non_pointed(f,e):
        try:
            rem_btn['background'] = 'white'
        except:
            pass

    def delete(f):
        f.no_av(x='r')
        selected_item = f.tree.selection()[0]  ## get selected item
        f.tree.delete(selected_item)

    def vacant_(f): #vacant3_
        f.vacc_ = []; week_ = []; pcp = []; res_ = []
        temp = ''; tt = ''
        ch = []; chh = []
        file = open('reserved', 'r')
        rese = file.readlines()
        for r in rese:
            rr = r.split()
            chh.append(rr[0])
            ch.append(rr[0]+' '+rr[1])
        for i in range(1, pc_no + 1):
            pcp.append('#' + str(i))
        for i in range(7):  # each days in a week
            date = datetime.datetime.today() + datetime.timedelta(days=i)
            temp_d = str(str(int(date.strftime('%d'))) + '-' + date.strftime('%a'))
            week_.append(temp_d)

        for j in week_:  # date comes first (scaning all dates in file line)
            for i in rese:
                word = i.split()
                if j == word[0]:
                    for k in pcp:  # pc day
                        temp = ''
                        if k == word[1]:
                            for h in range(ot_, ct_ + 1):  # pc time
                                if str(h) not in word:
                                    if temp != '':
                                        temp = temp + ' ' + str(h)
                                    else:
                                        temp = tt + ' ' + str(h)
                                        tt = ''
                                    if h == ct_:
                                        x=''
                                        res_.append(j+' '+k+' '+temp)

                                elif str(h) in word:
                                    if temp != '':
                                        temp = temp + ' ' + str(h)
                                        res_.append(j+' '+k+' '+temp)
                                        temp = ''
                                    else:
                                        tt = str(h)

                        else:
                            kk = j+' '+k
                            if kk not in ch:
                                x2 = j + ' ' + k + ' ' + str(ot_) + ' ' + str(ct_)
                                res_.append(x2)


                else:  # all pc vacant on that day
                    if j not in chh:
                        for p in range (1,pc_no+1):
                            x2 = j + ' ' + '#'+str(p) + ' ' + str(ot_) + ' ' + str(ct_)
                            res_.append(x2)
        vacc__ = list(dict.fromkeys(res_))
        f.vacc_ = sorted(vacc__)


    def datetime_format(f,o,c):  # time and date drop-off choices  # repeated
        # time 24 hour to 12 hour format
        for i in range(o,c):
            if i >= 12:
                if i == 12:
                    pc_time_info = str(i) + 'PM'
                if i == 24:
                    pc_time_info = '12' + 'AM'
                else:
                    j = i - 12
                    pc_time_info = str(j) + 'PM'
            else:
                pc_time_info = str(i) + 'AM'
            return pc_time_info


    def converter_(f,i):        # 24h to 12h
        if i >= 12:
            if i == 12:
                pc_time_info = str(i) + 'PM'
            elif i == 24:
                pc_time_info = '12' + 'AM'
            else:
                j = i - 12
                pc_time_info = str(j) + 'PM'
        else:
            pc_time_info = str(i) + 'AM'
        return pc_time_info

    def sorter(f):
        with open("reserved", "r") as f:
            line = f.readlines()
        with open("reserved", "w") as f:
            line.sort()
            for i in line:
                f.write(i)
        f.close()

class cafe_info:
    def __init__(f):
        print ('')

    def options_display(f):

        option_frame = Frame(bottom_frame, width=260, height=320, bg='white')
        option_frame.place(relx=0.729, rely=0.02)

        no_user = len(open('userslist').readlines())
        no_res = len(open('reserved').readlines())
        no_reh = rh_-(no_res*4)
        no_vac = (((ct_-ot_)*7)*pc_no)-no_reh

        Label(option_frame, text='CAFE INFO', font=fontt,bg='white').place(relx=0.4, rely=0)
        Label(option_frame, text=("Number of PC's:   "+str(pc_no)),font=fontt,bg='white').place(relx=0.01, rely=0.1)
        Label(option_frame, text=("CAFE Time:   "+ pv.converter_(ot_)+' - '+pv.converter_(ct_)), font=fontt,bg='white').place(relx=0.01, rely=0.2)
        Label(option_frame, text="(Weekly)", font=('Typo Grotesk', 8), bg='white').place(relx=0.01,rely=0.3)
        Label(option_frame, text=("Reserved Hours:   "+str(no_reh)+' hour/s'), font=fontt,bg='white').place(relx=0.01, rely=0.35)
        Label(option_frame, text=("Vacant Hours:   "+str(no_vac)+' hour/s'), font=fontt,bg='white').place(relx=0.01, rely=0.45)
        Label(option_frame, text=("# of User's:   "+str(no_user-1)), font=fontt,bg='white').place(relx=0.01, rely=0.60)
        Label(option_frame, text=("# of Reserved:   "+str(no_res)), font=fontt, bg='white').place(relx=0.01, rely=0.70)
        Button(bottom_frame, text='LOGOUT', font=font1, bg=bg3,
               command=f.log_out_).place(relx=0.952, rely=0.98, anchor=S)


    def log_out_(f):
        log_out_screen = Toplevel(main_screen)
        log_out_screen.geometry("300x150")
        log_out_screen.geometry("+500+300")
        log_out_screen.wm_iconbitmap('sq.ico')
        log_out_screen.configure(bg=bg1)
        log_out_screen.resizable(width=False, height=False)
        Label(log_out_screen, text='DO YOU WANT TO LOGOUT?', font=font1, bg=bg1).pack(
            pady=25)
        Button(log_out_screen, text="Yes", font=font1, bg=bg3, width=6,
               command=lambda: [login_window()]).place(relx=0.20, rely=0.65, anchor=W)
        Button(log_out_screen, text="Cancel", font=font1, bg=bg3, width=6,
               command=log_out_screen.destroy).place(relx=0.80, rely=0.65, anchor=E)


class cafe_option:

    def __init__(f):
        print ('')

    def pc_options(f):

        global time_fdisplay
        global date_fdisplay

        Cafe_info = Button(middle_frame,image=pc_icon, text=' CAFE OPTION',compound='left',
                           width=120, font=font1, bg=bg3, relief=GROOVE, command=f.cafe_info_)
        Cafe_info.place(relx=0.01, rely=0.21)

        users_btn = Button(middle_frame,image=user_icon, text=' USER\'S INFO',compound='left',
                           font=font1, width=110, bg=bg3, relief=GROOVE, command=f.user_info)
        users_btn.place(relx=0.15, rely=0.21)

        users_btn = Button(middle_frame, image=admin_icon, text='ADMIN', compound='left',
                           font=font1,bg=bg3, relief=GROOVE, command=f.admin)
        users_btn.place(relx=0.28, rely=0.21)
        users_btn = Button(middle_frame, image=ref_icon, compound='left',
                           font=font1, bg=bg3, relief=GROOVE, command=pv.refresh,height=20,width=20)
        users_btn.place(relx=0.365, rely=0.21)
        # running date on screen
        date_fdisplay = Label(middle_frame, font=('Mayeka Regular Demo', 8), bg=bg4)
        date_fdisplay.place(relx=0.9, rely=0, width=100)

        # running time on screen
        time_fdisplay = Label(middle_frame, font=('Mayeka Regular Demo', 13), bg=bg4)
        time_fdisplay.place(relx=0.9, rely=0.46, width=100, height=25)

        f.time_display()

    def time_display(f):    #running date and time on screen
        #date and time format
        date_display1 = strftime('%a %d %b %Y')
        time_display1 = strftime('%I:%M:%S %p')
        #date counter
        date_fdisplay.config(text=date_display1)
        date_fdisplay.after(8600000, f.time_display)
        # time counter
        time_fdisplay.config(text=time_display1)
        time_fdisplay.after(1000, f.time_display)

    def cafe_info_(f):
        global time_box01
        global time_box02
        global number_of_pcs
        global h24

        h24 = IntVar()
        number_of_pcs = StringVar()
        cafe_info_screen = Toplevel(main_screen)
        cafe_info_screen.geometry("350x200")
        cafe_info_screen.geometry("+500+250")
        cafe_info_screen.wm_iconbitmap('sq.ico')
        cafe_info_screen.configure(bg=bg1)
        cafe_info_screen.resizable(width=False, height=False)
        main_screen.option_add('*TCombobox*Listbox.font', font1)

        Label(cafe_info_screen, text='CAFE OPTION',font=('Mayeka Regular Demo', 14),bg=bg1).pack()
        Label(cafe_info_screen, text = "Number of PC's: ", font=font, bg=bg1).place(relx=0.05, rely=0.3)
        Label(cafe_info_screen, text="CAFE Time: ", font=font, bg=bg1).place(relx=0.05, rely=0.45)
        Label(cafe_info_screen, text="to", font=font, bg=bg1).place(relx=0.65, rely=0.45)

        E=Entry(cafe_info_screen,font=font, textvariable=number_of_pcs,width=6)
        E.place(relx=0.45, rely=0.305)
        E.insert(0, pc_no)
        # shop open time
        time_box01 = Combobox(cafe_info_screen, values=time_list, width=5, font=font1, state=READABLE)
        time_box01.set(time_list[ot_])
        time_box01.place(relx=0.45, rely=0.45)
        # shop close time
        time_box02 = Combobox(cafe_info_screen, values=time_list, width=5, font=font1, state=READABLE)
        time_box02.set(time_list[ct_])
        time_box02.place(relx=0.72, rely=0.45)

        Button(cafe_info_screen, text="Done", font=('Mayeka Regular Demo', 11), bg=bg3, width=6,
               command=lambda: [f.cafe_time_(),cafe_info_screen.destroy()]).place(relx=0.30, rely=0.8, anchor=W)
        Button(cafe_info_screen, text="Cancel", font=('Mayeka Regular Demo', 11), bg=bg3, width=6,
               command=cafe_info_screen.destroy).place(relx=0.53, rely=0.8, anchor=W)

        #call options for update

    def cafe_time_(f):
        number_of_pc = number_of_pcs.get()

        open_time = str(time_box01.current())
        close_time = str(time_box02.current())
        #if open_time != '-1' or close_time != '-1':
        file = open('cafetime', "w")
        file.write(number_of_pc + "\n")
        file.write(open_time + "\n")
        file.write(close_time)
        file.close()
        cafe_time()
        ci.options_display()

    def admin(f):
        admin_screen = Toplevel(main_screen)
        admin_screen.geometry("350x200")
        admin_screen.geometry("+500+250")
        admin_screen.wm_iconbitmap('sq.ico')
        admin_screen.configure(bg=bg1)
        admin_screen.resizable(width=False, height=False)

        global admin_pas
        global admin_un
        admin_un = StringVar()
        admin_pas = StringVar()

        file = open('userslist','r')
        d = file.readline()
        ad = d.split()
        Label(admin_screen, text=("Name:\t    "+ad[1]), bg=bg1, font=font1).place(x=41, y=30)
        Label(admin_screen, text="Username: ", bg=bg1, font=font1).place(x=41, y=60)
        Label(admin_screen, text="Password: ", bg=bg1, font=font1).place(x=41, y=90)

        username_login_entry = Entry(admin_screen, textvariable=admin_un, font=font1)
        username_login_entry.insert(END,ad[0])
        username_login_entry.place(x=130, y=60, height=23, width=150)

        password_login_entry = Entry(admin_screen, textvariable=admin_pas,font=font1)
        password_login_entry.insert(END,ad[2])
        password_login_entry.place(x=130, y=90, height=23, width=150)

        Button(admin_screen, text="Done", font=('Mayeka Regular Demo', 11), bg=bg3, width=6,
               command=lambda: [f.admin_name(),admin_screen.destroy()]).place(relx=0.30, rely=0.8, anchor=W)
        Button(admin_screen, text="Cancel", font=('Mayeka Regular Demo', 11), bg=bg3, width=6,
               command=admin_screen.destroy).place(relx=0.53, rely=0.8, anchor=W)

    def admin_name(f):
        un = admin_un.get()
        pw = admin_pas.get()
        with open("userslist") as f:
            lines = f.readlines()
        lines[0] =  (un+' admin '+pw+'\n')
        with open("userslist",'w') as f:
            f.writelines(lines)

    def user_info(f):

        f.user_info_screen = Toplevel(main_screen)
        f.user_info_screen.geometry("600x350")
        f.user_info_screen.geometry("+350+200")
        f.user_info_screen.wm_iconbitmap('sq.ico')
        f.user_info_screen.configure(bg=bg2)
        f.user_info_screen.resizable(width=False, height=False)
        Label(f.user_info_screen, text="USER'S INFO",font=('Typo Grotesk', 17), bg=bg2).grid()
        Label(f.user_info_screen, text="*Select User to Remove", font=('Typo Grotesk', 10), bg=bg2).place(x=0,y=14)
        user_info_frame = Frame(f.user_info_screen)
        user_info_frame.grid(row=1)

        f.tree = ttk.Treeview(user_info_frame, height=14, style="mystyle.Treeview")
        f.tree.grid(pady=5,padx=5)
        f.tree.bind('<<TreeviewSelect>>',f.select_user)

        #tree.tag_configure('odd', background='#D8D8D8')
        #tree.tag_configure('even', background='#E6E6E6')

        scroll = Scrollbar(user_info_frame, orient='vertical', command=f.tree.yview)
        f.tree.configure(yscrollcommand=scroll.set)
        scroll.grid(row=0, column=1, sticky='ns')

        f.tree['columns'] = ('1', '2', '3', '4', '5')
        f.tree['show'] = 'headings'

        f.tree.column('1', width=50)
        f.tree.column('2', width=180)
        f.tree.column('3', width=120)
        f.tree.column('4', width=120)
        f.tree.column('5', width=100)

        f.tree.heading('1', text='#')
        f.tree.heading('2', text='Name')
        f.tree.heading('3', text='Username')
        f.tree.heading('4', text='Password')
        f.tree.heading('5', text='Status')

        c = 1

        file = open('userslist', 'r+')
        d = file.readlines()  # lines inside file
        for i in d:
            s = i.split()
            x = f.active(s[0])
            if s[1] !='admin':
                x=f.active(s[0])
                f.tree.insert('', 'end', text=(s[0]), values=(str(c),s[0], s[1], s[2],x))
                c += 1
            else:
                pass

    def select_user(f, event):
        for item in f.tree.selection():
            remname = f.tree.item(item,"text")
        global rem_btn
        rem_btn=Button(f.user_info_screen,image=rem_icon, text=' Remove User', font=font1, relief=FLAT,compound='left')
        rem_btn.place(relx=0.86, rely=0.09,anchor=S)
        rem_btn['command']=lambda:[f.remove_btn(remname)]

        rem_btn.bind('<Enter>', pv.pointed)
        rem_btn.bind('<Leave>', pv.non_pointed)

    def remove_btn(f,remname):
        remove_screen = Toplevel(main_screen)
        remove_screen.geometry("300x150")
        remove_screen.geometry("+500+300")
        remove_screen.wm_iconbitmap('sq.ico')
        remove_screen.configure(bg=bg1)
        remove_screen.resizable(width=False, height=False)
        Label(remove_screen, text='REMOVE USER?', font=font1, bg=bg1).pack(
            pady=25)
        Button(remove_screen, text="Yes", font=font1, bg=bg3, width=6,
               command=lambda: [f.remove_user(remname),remove_screen.destroy()]).place(relx=0.20, rely=0.65, anchor=W)
        Button(remove_screen, text="Cancel", font=font1, bg=bg3, width=6,
               command=remove_screen.destroy).place(relx=0.80, rely=0.65, anchor=E)

    def delete(f):
        selected_item = f.tree.selection()[0]  ## get selected item
        f.tree.delete(selected_item)

    def remove_user(f,un):
        f.delete()
        with open("userslist", "r") as fi:
            lines = fi.readlines()
        with open("userslist", "w") as fi:
            for line in lines:
                word = line.split()
                if un not in word:
                    fi.write(line)
        f.remove_res(un)

    def remove_res(f,un):
        with open("reserved", "r") as fi:
            lines = fi.readlines()
        with open("reserved", "w") as fi:
            for line in lines:
                if un not in line:
                    fi.write(line)
        fi.close()
        cafe_time()
        ci.options_display()
        pv.no_av(x='r')
        pv.no_av(x='v')
        pv.refresh()

    def remove_passeddate(f):
        #removes dates that are passed (range 1 week)
        today = date.today()
        yesterday2 = []
        for i in range(1, 8):
            yesterday = today - timedelta(days=i)
            yesterday2.append(str(yesterday.strftime('%d')) + '-' + yesterday.strftime('%a'))
        with open ('reserved','r') as file:
            lines = file.readlines()
        with open ('reserved','w') as file:
            for line in lines:
                s = line.split()
                if s[0] not in yesterday2:
                    file.write(line)

    def active(f,un):
        r = open('reserved','r')
        re = r.readlines()
        line = ''.join(re)
        if un in line:
            return ('ACTIVE')
        else:
            return ('INACTIVE')


    def info(f):
        info = Toplevel(main_screen)
        info.geometry("400x250")
        info.geometry("+450+230")
        info.wm_iconbitmap('sq.ico')
        info.resizable(width=False, height=False)
        canv = Canvas(info, width=400, height=250)
        canv.pack()

        canv.create_image(0,0, image=bgI, anchor='nw')
        text = 'Hi!, My name is PIKAPI\n\nThank you for using this program!\n'
        bot_tx ='-Shane Tomboc'
        Label (canv, text = text,font=fontt, fg='white',bg='black').place(relx=0.1, rely=0.1)
        Label(canv, text=bot_tx, font=fontt1, fg='white', bg='black').place(relx=0.46, rely=0.88)

def upper_screen():
    # upper screen (titles)
    Label(top_frame, text='INTERNET CAFE RESERVATION', font=('Mayeka Regular Demo', 23), bg=bg1).place(relx=0.5, rely=0.5,
                                                                                        anchor=CENTER)
    Label(top_frame, text='ADMIN', font=('Mayeka Regular Demo', 12), bg=bg1).place(relx=0.001, rely=0.55, anchor=NW)
    Button(top_frame, image=inf_icon, bg = bg1, relief=FLAT, command = co.info).place(relx=0.977,rely=0)

def cafe_time():    # cafe setted time
    global pc_no
    global ot_
    global ct_
    global rh_
    file = open('cafetime', 'r')
    d = file.readlines()
    pc_no = int(d[0])
    ot_ = int(d[1])
    ct_ = int(d[2])
    file.close()


    file = open("reserved", "r")
    data = file.read()
    words = data.split()
    rh_ = len(words)      # no of reserved pc



if __name__ == '__main__':
    # main screen
    main_screen = Tk()
    main_screen.wm_title('L A L A')
    main_screen.wm_iconbitmap('sq.ico')
    main_screen.geometry("1000x500")
    main_screen.geometry("+170+100")
    main_screen.resizable(width=False, height=False)
    # all arround variables
    FL_date = []
    date_list = []
    occupied_pc = []
    pc_icon = PhotoImage(file="pcb.png")
    user_icon = PhotoImage(file="userb.png")
    admin_icon = PhotoImage(file="admin.png")
    rem_icon = PhotoImage(file="rem.png")
    inf_icon = PhotoImage(file="info.png")
    ref_icon = PhotoImage(file="ref.png")
    bgI = PhotoImage(file='bg.png')
    bg1 = '#D8D8D8'  # U gray   #background
    bg2 = '#BDBDBD'  # F gray   #for middle frame
    bg3 = '#848484'  # D gray   #for button
    bg4 = '#A4A4A4'  # blue     #for time
    bg5 = "#EFAFB4"  # red #for changed button
    # main frames
    top_frame = Frame(main_screen, width=1000, height=50, bg=bg1)
    top_frame.pack()
    middle_frame = Frame(main_screen, width=1000, height=40, bg=bg2)
    middle_frame.pack()
    bottom_frame = Frame(main_screen, width=1000, height=460, bg=bg1)
    bottom_frame.pack()

    font = ('Mayeka Regular Demo', 12)
    font1 = ('Mayeka Regular Demo', 11)
    fontt = ('Typo Grotesk', 12)
    fontt1 = ('Typo Grotesk', 11)

    time_list = ['12 AM','1 AM', '2 AM', '3 AM', '4 AM', '5 AM',
                 '6 AM', '7 AM', '8 AM', '9 AM', '10 AM', '11 AM',
                 '12 PM', '1 PM', '2 PM', '3 PM', '4 PM', '5 PM',
                 '6 PM', '7 PM', '8 PM', '9 PM', '10 PM', '11 PM','12AM']

    pv = preview_()
    ci = cafe_info()
    co = cafe_option()
    cafe_time()
    upper_screen()
    co.remove_passeddate()
    pv.reserve_tab()
    pv.vancant_tab()
    ci.options_display()
    co.pc_options()

    mainloop()

# NO TIMER IN VC PC BUTTON w/ TRYEX