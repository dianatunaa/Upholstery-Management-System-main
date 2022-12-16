import os
from tkinter import *
import sqlite3

conn = sqlite3.connect("bens.db")
curr = conn.cursor()
   
login_screen = Tk()
login_screen.resizable(False, False)
login_screen.title("Login")
login_screen.geometry("500x300")
login_screen.configure(bg='#285A51')
username = StringVar()
password= StringVar()

def dbFunc():
    global conn, curr
    conn = sqlite3.connect("bens.db")
    curr = conn.cursor()

def LoginVerification():
    dbFunc()
    global user1
    user1 = username.get()
    pass1 = password.get()
    username_entry.delete(0, END)
    password_entry.delete(0, END)
    error_frame = Frame(login_screen)
    error_frame.pack(side = BOTTOM, fill=X)    
    curr.execute("""SELECT username FROM account""")
    fetchuser = curr.fetchall()
    users = [x[0] for x in fetchuser]
    er = Label(error_frame, fg = "red")
    if user1 == "" or pass1 == "":
        er.destroy()
        er = Label(error_frame, text = "Fill all entries.", fg = "red")
        er.pack()
    elif user1 in users:
        curr.execute("""SELECT password FROM account WHERE username = ?""", [user1])
        fetchpass = curr.fetchall()
        passs = [x[0] for x in fetchpass]
        if pass1 in passs:
            Authorization()
        else:
            er.destroy()
            er = Label(error_frame, text = "Incorrect Password.", fg = "red")
            er.pack()
    else:
        er.destroy()
        er = Label(error_frame, text = "User does not exist.", fg = "red")        
        er.pack()

def Authorization():
    dbFunc()
    curr.execute("""SELECT authority FROM account WHERE username = ?""", [user1])
    fetchautho = curr.fetchall()
    authorize = [x[0] for x in fetchautho]
    curr.close()
    conn.close()
    if authorize == ['Administrator']:
        login_screen.destroy()
        import bAdmin
    elif authorize == ['Project Coordinator']:
        login_screen.destroy()
        import bCoordinator
    elif authorize == ['Inventory Clerk']:
        login_screen.destroy()
        import bClerk

top_frame = Frame(login_screen, bg='#B0EFEF',)
top_frame.pack(side = TOP, pady=10, fill=X)
mid_frame = Frame(login_screen, bg='#285A51')
mid_frame.pack()

lbl_title = Label(top_frame, text="Ben's Canvas and General Upholstery\nManagement System.", font = ("Bahnschrift bold", 14), bg='#B0EFEF', fg ='#002A2A')
lbl_title.pack(fill=X)
    
lbl_instruct = Label(mid_frame, text="\nEnter your Username and Password.\n", font = ("Consolas", 11), bg='#285A51', fg ="#5A9899")
lbl_instruct.grid(row = 0, columnspan = 3)
lbl_username = Label(mid_frame, text="Username: ", font = ("Consolas", 12), bg='#285A51', fg ="#D8D2CC")
lbl_username.grid(row = 1, sticky = W)
lbl_password = Label(mid_frame, text="Password: ", font = ("Consolas", 12), bg='#285A51', fg ="#D8D2CC")
lbl_password.grid(row = 2, sticky = W)
    
username_entry = Entry(mid_frame, textvariable = username, width=30, font = ("Calibri", 12))
username_entry.grid(row = 1, pady=3, column = 1, sticky = W)
password_entry = Entry(mid_frame, textvariable = password, show= '*', width=30, font = ("Calibri", 12))
password_entry.grid(row = 2, column = 1, sticky = W)
btn_login = Button(mid_frame, text="Login", width=37, font = ("Bahnschrift bold", 12), command = LoginVerification)
btn_login.grid(row = 3, columnspan = 2, pady = 20)
login_screen.mainloop()
