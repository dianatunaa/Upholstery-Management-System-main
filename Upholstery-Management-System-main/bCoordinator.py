from tkinter import *
from tkinter import ttk
from datetime import datetime
from datetime import date
import tkinter.messagebox as tkMessageBox
import chart_studio.plotly as py
import plotly.figure_factory as ff
import plotly
import sqlite3

main = Tk()
main.title("Ben's Management System")
main.geometry('1000x700')
main.resizable(False, False)
main.configure(bg = '#B6E0DC')

tab_parent = ttk.Notebook(main)
tab1 = Frame(tab_parent, bg = '#B6E0DC')
tab2 = Frame(tab_parent, bg = '#79DC78')
tab3 = Frame(tab_parent, bg = '#78B3DD')

pic_monitor = PhotoImage(file = r'D:\Users\Diane\Desktop\Upholstery-Management-System-main\monitor.png')
pic_inventory = PhotoImage(file = r'"D:\Users\Diane\Desktop\Upholstery-Management-System-main\inv.png"')
pic_customer = PhotoImage(file = r'"D:\Users\Diane\Desktop\Upholstery-Management-System-main\cust.png"')

tab_parent.add(tab1, text = "Project Monitor", image = pic_monitor, compound = LEFT)
tab_parent.add(tab2, text = "Inventory", image = pic_inventory, compound = LEFT)
tab_parent.add(tab3, text = "Customer Archive", image = pic_customer, compound = LEFT)
tab_parent.pack(expand = 1, fill = 'both')

#Project
proj_id = StringVar()
cust_id = StringVar()
fname = StringVar()
lname = StringVar()
contact_no = StringVar()
address = StringVar()

start_date = StringVar()
end_date = StringVar()
desc = StringVar()
pay_stat = StringVar()
woodworking = IntVar()
welding = IntVar()
sewing = IntVar()
delivery = StringVar()

#Progress
progress_pay = IntVar()
progress_woodworking = IntVar()
progress_welding = IntVar()
progress_sewing = IntVar()
progress_delivery = IntVar()

#Inventory
prod_id = StringVar()
prod_name = StringVar()
mat_type = StringVar()
color = StringVar()
distinction = StringVar()
in_stock = IntVar()
quant_type = StringVar()
price = IntVar()
status = StringVar()

inventory_search = StringVar()
cust_search = StringVar()
acc_search = StringVar()

def dbFunc():
    global conn, curr
    conn = sqlite3.connect('bens.db')
    curr = conn.cursor()

def IntValidation(ent):
    print(ent.isdigit())
    return ent.isdigit()
 
#################################################################ProjectMonitor#################################################################
################################################################################################################################################
def MonitorDisplay():
    dbFunc()
    curr.execute("""SELECT projID, status FROM project WHERE status != 'Archive'""")
    fetch = curr.fetchall()
    for data in fetch:
        monitor_tree.insert('', 'end', values=(data))
    curr.close()
    conn.close()
#--------------------------------------  
def MonitorGantt():
    gantt_value = []
    dbFunc()
    curr.execute("""SELECT projID FROM project WHERE status != 'Archive'""")
    fetch_projID = curr.fetchall()
    list_projID = [x[0] for x in fetch_projID]
    for projID in list_projID:
        start_date = str()
        end_date = str()
        status = str()
        curr.execute("""SELECT startDate FROM project WHERE projID = ?""", [projID])
        start = curr.fetchall()
        list_start = [x[0] for x in start]
        for x in list_start:
            start_date+= x
        curr.execute("""SELECT endDate FROM project WHERE projID = ?""", [projID])
        end = curr.fetchall()
        list_end = [x[0] for x in end]
        for x in list_end:
            end_date+= x
        curr.execute("""SELECT status FROM project WHERE projID = ?""", [projID])
        stat = curr.fetchall()
        list_status = [x[0] for x in stat]
        for x in list_status:
            status+= x
        gantt_value.append(dict(Task = projID, Start = start_date, Finish = end_date, Resource = status))

    fig = ff.create_gantt(gantt_value, index_col = 'Resource', show_colorbar = True, group_tasks = True)
    plotly.offline.plot(fig, filename='gantt-chart.html')
    curr.close()
    conn.close()
#--------------------------------------            
def MonitorTable(c):
    global count
    count = c
    project = []
    materials = []
    materials2 = []
    customer = []
    progress = []
    mats = str()
    if not monitor_tree.selection() or count == 1:
        print("ERROR")
    else:
        count+=1
        global monitor_table_frame
        monitor_table_frame = Frame(tab1, bg = '#ffffff')
        monitor_table_frame.pack(side = TOP, fill=X)
        info_frame = LabelFrame(monitor_table_frame, text = "Project Details", bg = '#ffffff', font = ('Consolas', 12))
        info_frame.pack(side = TOP, fill = X, pady = 10)
        table_frame = Frame(monitor_table_frame, bg = '#ffffff')
        table_frame.pack(side = TOP, fill = X, pady = 20)
        curItem = monitor_tree.focus()
        contents =(monitor_tree.item(curItem))
        selecteditem = contents['values']
        dbFunc()
        curr.execute("""SELECT * FROM project WHERE projID = ?""", (selecteditem[0],))
        fetch1 = curr.fetchall()
        for x in fetch1[0]:
            project.append(x)
        curr.execute("""SELECT COUNT(prodID) FROM materials WHERE projID LIKE ?""", (selecteditem[0],))
        n = curr.fetchall()
        if n == 1:
            curr.execute("""SELECT prodName FROM materials WHERE projID LIKE ?""", (selecteditem[0],))
            name = [item[0] for item[0] in curr.fetchall()]
            curr.execute("""SELECT quantity FROM materials WHERE projID LIKE ?""", (selecteditem[0],))
            quantity = [item[0] for item[0] in curr.fetchall()]
            curr.execute("""SELECT quantType FROM materials WHERE projID LIKE ?""", (selecteditem[0],))
            qtype = [item[0] for item[0] in curr.fetchall()]
            for x in range(0,len(name)):
                mats+=(name[x] + ", " + str(quantity[x]) + " " + qtype[x] + "\n\t")            
        else:
            curr.execute("""SELECT prodName FROM materials WHERE projID LIKE ?""", (selecteditem[0],))
            name = [item[0] for item in curr.fetchall()]
            curr.execute("""SELECT quantity FROM materials WHERE projID LIKE ?""", (selecteditem[0],))
            quantity = [item[0] for item in curr.fetchall()]
            curr.execute("""SELECT quantType FROM materials WHERE projID LIKE ?""", (selecteditem[0],))
            qtype = [item[0] for item in curr.fetchall()]
            for x in range(0,len(name)):
                mats+=(name[x] + ", " + str(quantity[x]) + " " + qtype[x] + "\n\t")
        curr.execute("""SELECT * FROM customer WHERE projID = ?""", (selecteditem[0],))
        fetch3 = curr.fetchall()
        for x in fetch3[0]:
            customer.append(x)
        curr.execute("""SELECT * FROM progress WHERE projID = ?""", (selecteditem[0],))
        fetch4 = curr.fetchall()
        for x in fetch4[0]:
            progress.append(x)
        curr.close()
        conn.close()
        txt_customer = "Customer: " + customer[1] + "\t" + customer[3] + ", " + customer[4]
        txt_date = "Start Date: " + project[2] + "\nCompletion Date: " + project[3]
        txt_desc = "Description: " + project[4]
        txt_materials = "Materials: " + mats
        lbl_customer = Label(info_frame, text = txt_customer, bg = '#ffffff', font = ("Consolas", 14))
        lbl_customer.grid(row = 0, sticky = W)
        lbl_date = Label(info_frame, text = txt_date, bg = '#ffffff', font = ("Consolas", 14))
        lbl_date.grid(row = 1, sticky = W)
        lbl_desc = Label(info_frame, text = txt_desc, bg = '#ffffff', font = ("Consolas", 14))
        lbl_desc.grid(row = 2, sticky = W)
        lbl_materials = Label(info_frame, text = txt_materials, bg = '#ffffff', font = ("Consolas", 14))
        lbl_materials.grid(row = 3, sticky = W)

        payment_status = Label(table_frame, text = "Payment Option", bg = '#99ccff', font = ("Consolas", 14), borderwidth = 3, width = 15, relief = GROOVE)
        payment_status.grid(row = 0, column = 0, ipadx = 15, ipady = 17)
        assembly = Label(table_frame, text = "Assembly Requirements", bg = '#99ccff', font = ("Consolas", 14), borderwidth = 3, width = 42, relief = GROOVE)
        assembly.grid(row = 0, column = 1, columnspan = 3, ipadx = 16, ipady = 17)
        delivery = Label(table_frame, text = "Order Status", bg = '#99ccff', font = ("Consolas", 14), borderwidth = 3, width = 12, relief = GROOVE)
        delivery.grid(row = 0, column = 4, ipadx = 15, ipady = 17)
        
        if project[6] == 0:
            twood = "N/A"
        elif project[6] == 1:
            twood = "Woodworking"
        if project[7] == 0:
            tweld = "N/A"
        elif project[7] == 1:
            tweld = "Welding"
        if project[8] == 0:
            tsew = "N/A"
        elif project[8] == 1:
            tsew = "Sewing"
        if progress[1] == 1 or project[5] == 'Fullpayment':
            cstat = '#00ff00'
        elif progress[1] == 0:
            cstat = '#ff0000'
        if progress[2] == 0:
            cwood = '#ff0000'
        elif progress[2] == 1:
            cwood = '#00ff00'
        if progress[3] == 0:
            cweld = '#ff0000'
        elif progress[3] == 1:
            cweld = '#00ff00'
        if progress[4] == 0:
            csew = '#ff0000'
        elif progress[4] == 1:
            csew = '#00ff00'
        if progress[5] == 0:
            cdelivery = '#ff0000'
        elif progress[5] == 1:
            cdelivery = '#00ff00'
        ent_payment_status = Label(table_frame, text = project[5], font = ("Consolas", 14), bg = cstat, borderwidth = 3, width = 15, height = 8, relief = GROOVE)
        ent_payment_status.grid(row = 1, column = 0, ipadx = 15)
        ent_assembly_woodworking = Label(table_frame, text = twood, font = ("Consolas", 14), bg = cwood, borderwidth = 3, width = 13, height = 8, relief = GROOVE)
        ent_assembly_woodworking.grid(row = 1, column = 1, ipadx = 8)
        ent_assembly_welding = Label(table_frame, text = tweld, font = ("Consolas", 14), bg = cweld, borderwidth = 3, width = 13, height = 8, relief = GROOVE)
        ent_assembly_welding.grid(row = 1, column = 2, ipadx = 8)
        ent_assembly_sewing = Label(table_frame, text = tsew, font = ("Consolas", 14), bg = csew, borderwidth = 3, width = 13, height = 8, relief = GROOVE)
        ent_assembly_sewing.grid(row = 1, column = 3, ipadx = 8)
        ent_delivery = Label(table_frame, text = project[9], font = ("Consolas", 14), bg = cdelivery, borderwidth = 3, width = 12, height = 8, relief = GROOVE)
        ent_delivery.grid(row = 1, column = 4, ipadx = 15)
#--------------------------------------
def MonitorRefresh(c):
    global count
    count = c
    count = 0
    monitor_table_frame.destroy()
    monitor_tree.delete(*monitor_tree.get_children())
    MonitorDisplay()

#--------------------------------------      
def MonitorAdd():
    global add_proj, ent_fname, ent_lname, ent_address, ent_contact, start_date_year, start_date_month, start_date_day, end_date_year, end_date_month, end_date_day
    add_proj = Toplevel()
    add_proj.title("New Project")
    add_proj.geometry("400x630")
    add_proj.resizable(False, False)
    add_proj.lift()
    add_proj.attributes("-topmost", True)
    add_proj.grab_set()

    dbFunc()
    curr.execute("""SELECT COUNT(DISTINCT customerID) FROM customer""")
    fetch = curr.fetchone()
    n = int(1)
    for x in fetch:
            n+=x
    n2 = str(n)
    cust_id.set("#CUS"+ n2.zfill(6))
    n = int(1)
    curr.execute("""SELECT COUNT(*) FROM project""")
    fetch = curr.fetchone()
    for x in fetch:
            n+=x
    n2 = str(n)
    proj_id.set("#PROJ"+ n2.zfill(6))
    fname.set("")
    lname.set("")
    contact_no.set("")
    address.set("")
    start_date.set("")
    end_date.set("")
    desc.set("")
    pay_stat.set("")
    delivery.set("")
    curr.close()
    conn.close()
    
    int_val = add_proj.register(IntValidation)
    top_add = Frame(add_proj, relief = SOLID, bg = '#ffffff')
    top_add.pack(side = TOP, pady = 10, fill = 'both')
    customer_frame = LabelFrame(add_proj, text = "Customer Information", width = 30)
    customer_frame.pack(side = TOP, fill = 'both', expand = 'yes', padx = 10, pady = 10)
    project_frame = LabelFrame(add_proj, text = "Project Information", width=30)
    project_frame.pack(side=TOP, fill = 'both', expand = 'yes', padx = 10)
    btn_frame = Frame(add_proj, pady = 20)
    btn_frame.pack(side = TOP)
    
    lbl_text = Label(top_add, text = "Add New Project", font = ('Consolas', 14), bg = '#ffffff')
    lbl_text.pack(padx = 5, fill = X)
    btn_exist = Button(customer_frame, text = "Existing Customer", relief = FLAT, overrelief = SUNKEN, bg = '#B6E0DC', font = ('Consolas', 11), command = ExistingCustomer, width = 30)
    btn_exist.grid(row = 0, columnspan = 2, pady = 5)
    lbl_cust_no = Label(customer_frame, text="Customer ID: ", bd=5)
    lbl_cust_no.grid(row = 1, sticky = W, padx = 20)  
    lbl_fname = Label(customer_frame, text="First Name: ", bd=5)
    lbl_fname.grid(row = 2, sticky=W, padx = 20)
    lbl_lname = Label(customer_frame, text="Last Name: ", bd=5)
    lbl_lname.grid(row = 3, sticky=W, padx = 20)
    lbl_address = Label(customer_frame, text="Address: ", bd=5)
    lbl_address.grid(row = 4, sticky=W, padx = 20)
    lbl_contact = Label(customer_frame, text="Contact No: ", bd=5)
    lbl_contact.grid(row = 5, sticky=W, padx = 20)
    ent_cust_id = Entry(customer_frame, textvariable = cust_id, width = 35, state = 'disable')
    ent_cust_id.grid(row = 1, column = 1, pady = 5)
    ent_fname = Entry(customer_frame, textvariable = fname, width = 35)
    ent_fname.grid(row = 2, column = 1, pady = 5)
    ent_lname = Entry(customer_frame, textvariable = lname, width = 35)
    ent_lname.grid(row = 3, column = 1, pady = 5)
    ent_address = Entry(customer_frame, textvariable = address, width = 35)
    ent_address.grid(row = 4, column = 1, pady = 5)
    ent_contact = Entry(customer_frame, textvariable = contact_no, width = 35, validate = "key", validatecommand = (int_val, '%S'))
    ent_contact.grid(row = 5, column = 1, pady = 5)

    lbl_proj_no = Label(project_frame, text = "Project ID: ", bd = 5)
    lbl_proj_no.grid(row = 0, sticky = W, padx = 5)
    lbl_start_date = Label(project_frame, text = "Start Date: ", bd = 5)
    lbl_start_date.grid(row = 1, sticky = W, padx = 5)
    lbl_end_date = Label(project_frame, text = "Target Completion Date: ", bd = 5)
    lbl_end_date.grid(row = 2, sticky = W, padx = 5)
    lbl_desc = Label(project_frame, text = "Description: ", bd = 5)
    lbl_desc.grid(row = 3, sticky = W, padx = 5)
    lbl_pay_stat = Label(project_frame, text="Payment Status: ", bd = 5)
    lbl_pay_stat.grid(row = 4, sticky = W, padx = 5)
    lbl_assembly = Label(project_frame, text="Assembly Requirements: ", bd = 5)
    lbl_assembly.grid(row = 5, sticky = W, padx = 5)
    lbl_delivery = Label(project_frame, text="Delivery Option: ", bd = 5)
    lbl_delivery.grid(row = 8, sticky = W, padx = 5)

    ent_proj_id = Entry(project_frame, textvariable = proj_id, width = 30, state = 'disable')
    ent_proj_id.grid(row = 0, column = 1, columnspan = 3, sticky = W)

    start_date_month = Spinbox(project_frame, values = ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "Decemeber"), width = 10, validatecommand = (int_val, '%S'), state = 'readonly') 
    start_date_month.grid(row = 1, column = 1, pady = 1, sticky = W)
    start_date_day = Spinbox(project_frame, values = ("01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"), width = 3, validatecommand = (int_val, '%S'), state = 'readonly') 
    start_date_day.grid(row = 1, column = 2, pady = 1, sticky = W)
    start_date_year = Spinbox(project_frame, from_= 2020, to = 2100 , width = 5, validatecommand = (int_val, '%S'), state = 'readonly') 
    start_date_year.grid(row = 1, column = 3, pady = 1, sticky = W)

    end_date_month = Spinbox(project_frame, values = ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "Decemeber"), width = 10, validatecommand = (int_val, '%S'), state = 'readonly') 
    end_date_month.grid(row = 2, column = 1, pady = 1, sticky = W)
    end_date_day = Spinbox(project_frame, values = ("01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"), width = 3, validatecommand = (int_val, '%S'), state = 'readonly') 
    end_date_day.grid(row = 2, column = 2, pady = 1, sticky = W)
    end_date_year = Spinbox(project_frame, from_= 2020, to = 2100 , width = 5, validatecommand = (int_val, '%S'), state = 'readonly') 
    end_date_year.grid(row = 2, column = 3, pady = 1, sticky = W)

    ent_desc = Entry(project_frame, textvariable = desc, width = 30)
    ent_desc.grid(row = 3, column = 1, columnspan = 3, sticky = W)
    ent_pay = ttk.Combobox(project_frame, width = 27, textvariable = pay_stat, state = 'readonly')
    ent_pay['values'] = ("Downpayment", "Fullpayment")
    ent_pay.grid(row = 4, column = 1, columnspan = 3, sticky = W)
    
    ent_wood = Checkbutton(project_frame, text = "Woodworking", variable = woodworking)
    ent_wood.grid(row = 5, column = 1, columnspan = 3, sticky = W)
    ent_weld = Checkbutton(project_frame, text = "Welding", variable = welding)
    ent_weld.grid(row = 6, column = 1, columnspan = 3, sticky = W)
    ent_sew = Checkbutton(project_frame, text ="Sewing", variable = sewing)
    ent_sew.grid(row = 7, column = 1, columnspan = 3, sticky = W)
    
    ent_delivery = ttk.Combobox(project_frame, width = 27, textvariable = delivery, state = 'readonly')
    ent_delivery['values'] = ("Delivery", "Pick-up")
    ent_delivery.grid(row = 8, column = 1, columnspan = 3, sticky = W)

    btn_cancel = Button(btn_frame, text = "Cancel", relief = FLAT, overrelief = SUNKEN, bg = '#B6E0DC', font = ('Consolas', 11), command = add_proj.destroy, width = 20)
    btn_cancel.grid(row = 0, padx = 5)
    btn_add = Button(btn_frame, text = "Save", relief = FLAT, overrelief = SUNKEN, bg = '#B6E0DC', font = ('Consolas', 11), width = 20, command = MonitorAddValidate)
    btn_add.grid(row = 0, column = 1, padx = 5)

def MonitorAddValidate():
    months = {'January':'01',
              'February':'02',
              'March':'03',
              'April':'04',
              'May':'05',
              'June':'06',
              'July':'07',
              'August':'08',
              'September':'09',
              'October':'10',
              'November':'11',
              'Decemebr':'12'}
    startmonth = months.get(start_date_month.get())
    endmonth = months.get(end_date_month.get())
    start_date = start_date_year.get() + "-" + startmonth + "-" + start_date_day.get()
    end_date = end_date_year.get() + "-" + endmonth + "-" + end_date_day.get()
    d1 = datetime.strptime(start_date, '%Y-%m-%d')
    d2 = datetime.strptime(end_date, '%Y-%m-%d')
    if proj_id.get() == "" or cust_id.get() == "" or fname.get() == "" or lname.get() == "" or contact_no.get() == "" or address.get() == "" or start_date == "" or end_date == "" or desc.get() == "" or pay_stat.get() == "" or woodworking.get() == "" or welding.get() == "" or sewing.get() == "" or delivery.get() == "":
        add_proj.grab_release()
        error = tkMessageBox.showerror('Error', 'Invalid, Fill all entries')
    elif d1>=d2:
        add_proj.grab_release()
        error = tkMessageBox.showerror('Error', 'Invalid Date')        
    elif woodworking.get() == 0 and welding.get() == 0 and sewing.get() == 0:
        add_proj.grab_release()
        error = tkMessageBox.showerror('Error', 'Invalid, Choose atleast one Assembly Requirement')        
    else:
        dbFunc()
        transaction_date = date.today()
        curr.execute("""INSERT INTO customer VALUES(?, ?, ?, ?, ?, ?, ?)""", (str(proj_id.get()), str(cust_id.get()), str(transaction_date), str(fname.get()), str(lname.get()), str(address.get()), str(contact_no.get())))
        conn.commit()
        curr.execute("""INSERT INTO project VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (str(proj_id.get()), str(cust_id.get()), str(start_date), str(end_date), str(desc.get()), str(pay_stat.get()), int(woodworking.get()), int(welding.get()), int(sewing.get()), str(delivery.get()), str("In Progress")))
        conn.commit()
        curr.execute("""INSERT INTO progress VALUES(?, ?, ?, ?, ?, ?)""", (str(proj_id.get()), int(0), int(0), int(0), int(0), int(0),))
        conn.commit()
        curr.close()
        conn.close()
        add_proj.destroy()
        InvRefresh()
        AddMats()
    add_proj.grab_set()

def ExistingCustomer():
    add_proj.grab_release()
    main.lift()
    main.attributes("-topmost", True)
    global material_tree
    tab_parent.add(tab1, text = "Project Monitor", image = pic_monitor, compound = LEFT, state = 'disable')
    tab_parent.add(tab2, text = "Inventory", image = pic_inventory, compound = LEFT, state = 'disable')
    tab_parent.add(tab3, text = "Customer Archive", image = pic_customer, compound = LEFT, state = 'normal')
    tab_parent.add(tab4, text = "Manage Accounts", image = pic_account, compound = LEFT, state = 'disable')
    tab_parent.select(tab_id = tab3)
    cust_btn_select.configure(state = 'normal')
    cust_btn_back.configure(state = 'normal')

def ExistingCustomerSelect():
    if not cust_tree.selection():
       print("ERROR")
    else:
        customer = []
        curItem = cust_tree.focus()
        contents =(cust_tree.item(curItem))
        selecteditem = contents['values']
        dbFunc()
        curr.execute("""SELECT * FROM customer WHERE customerID = ?""", (selecteditem[1],))
        fetch1 = curr.fetchall()
        for x in fetch1[0]:
            customer.append(x)
        cust_id.set(customer[1])
        fname.set(customer[3])
        lname.set(customer[4])
        address.set(customer[5])
        contact_no.set(customer[6])
        ent_fname.configure(state = 'disable')
        ent_lname.configure(state = 'disable')
        ent_address.configure(state = 'disable')
        ent_contact.configure(state = 'disable')
        add_proj.lift()
        add_proj.grab_set()
        add_proj.attributes("-topmost", True)
        tab_parent.add(tab1, text = "Project Monitor", image = pic_monitor, compound = LEFT, state = 'normal')
        tab_parent.add(tab2, text = "Inventory", image = pic_inventory, compound = LEFT, state = 'normal')
        tab_parent.add(tab3, text = "Customer Archive", image = pic_customer, compound = LEFT, state = 'normal')
        tab_parent.add(tab4, text = "Manage Accounts", image = pic_account, compound = LEFT, state = 'normal')
        tab_parent.select(tab_id = tab1)
        curr.close()
        conn.close()
        cust_btn_select.configure(state = 'disable')
        cust_btn_back.configure(state = 'disable')
        
def ExistingCustomerBack():
    add_proj.lift()
    add_proj.grab_set()
    add_proj.attributes("-topmost", True)
    tab_parent.add(tab1, text = "Project Monitor", image = pic_monitor, compound = LEFT, state = 'normal')
    tab_parent.add(tab2, text = "Inventory", image = pic_inventory, compound = LEFT, state = 'normal')
    tab_parent.add(tab3, text = "Customer Archive", image = pic_customer, compound = LEFT, state = 'normal')
    tab_parent.add(tab4, text = "Manage Accounts", image = pic_account, compound = LEFT, state = 'normal')
    tab_parent.select(tab_id = tab1)
    cust_btn_select.configure(state = 'disable')
    cust_btn_back.configure(state = 'disable')

def MatsDisplay():
    dbFunc()
    curr.execute("""SELECT * FROM materials WHERE projID = ?""", (str(proj_id.get()),))
    fetch = curr.fetchall()
    for data in fetch:
        material_tree.insert('', 'end', values=(data))
    curr.close()
    conn.close()
    
def AddMats():
    add_proj.grab_release()
    global material_tree, add_material
    tab_parent.add(tab1, text = "Project Monitor", image = pic_monitor, compound = LEFT, state = 'disable')
    tab_parent.add(tab2, text = "Inventory", image = pic_inventory, compound = LEFT, state = 'normal')
    tab_parent.add(tab3, text = "Customer Archive", image = pic_customer, compound = LEFT, state = 'disable')
    tab_parent.add(tab4, text = "Manage Accounts", image = pic_account, compound = LEFT, state = 'disable')
    tab_parent.select(tab_id = tab2)
    inventory_btn_add.configure(state = 'disable')
    inventory_btn_edit.configure(state = 'disable')
    inventory_btn_delete.configure(state = 'disable')
    inventory_btn_select.configure(state = 'normal')
    inventory_btn_done.configure(state = 'normal')
    
    add_material = Toplevel()
    add_material.title("Add Materials")
    add_material.geometry("350x400")
    add_material.resizable(False, False)
    add_material.lift()
    add_material.attributes("-topmost", True)
    material_scrollbarx = Scrollbar(add_material, orient = HORIZONTAL)
    material_scrollbary = Scrollbar(add_material, orient = VERTICAL)
    material_tree = ttk.Treeview(add_material, columns = ('ProjectID', 'ProductID', 'ProductName', 'Price', 'Quantity', 'QuantityType'), selectmode = "extended", height = 100, yscrollcommand = material_scrollbary.set, xscrollcommand = material_scrollbarx.set)
    material_scrollbary.config(command = material_tree.yview)
    material_scrollbary.pack(side = RIGHT, fill = Y)
    material_scrollbarx.config(command = material_tree.xview)
    material_scrollbarx.pack(side = BOTTOM, fill = X)
    material_tree.heading('ProjectID', text = "Project ID",anchor=W)
    material_tree.heading('ProductID', text = "Product ID",anchor=W)
    material_tree.heading('ProductName', text = "Product Name",anchor=W)
    material_tree.heading('Price', text = "Price",anchor=W)
    material_tree.heading('Quantity', text = "Quantity",anchor=W)
    material_tree.heading('QuantityType', text = "",anchor=W)
    material_tree.column('#0', stretch = NO, minwidth = 0, width = 0)
    material_tree.column('#1', stretch = NO, minwidth = 0, width = 0)
    material_tree.column('#2', width = 100)
    material_tree.column('#3', width = 100)
    material_tree.column('#4', width = 70)
    material_tree.column('#5', width = 70)
    material_tree.column('#6', minwidth = 0)
    material_tree.pack()
    MatsDisplay()
    
def AddMats2():
    global mat_add, quantity
    quantity = IntVar()
    if not inventory_tree.selection():
       print("ERROR")
    else:
        curItem = inventory_tree.focus()
        contents =(inventory_tree.item(curItem))
        selecteditem = contents['values']
        mat_add = Toplevel()
        mat_add.title("Add Materials")
        mat_add.geometry("300x300")
        mat_add.resizable(False, False)
        mat_add.attributes("-topmost", True)
        
        int_val = mat_add.register(IntValidation)
        add_frame = Frame(mat_add)
        add_frame.pack(side = TOP, padx = 10, pady = 12)
        btn_frame = Frame(mat_add)
        btn_frame.pack(side = TOP, padx = 10, pady = 12)
        title = Label(add_frame, text = "Add Material", font = ('Consolas Bold', 12), bg = '#ffffff', width = 30)
        title.grid(row = 0, columnspan = 2, pady = 5)
        lbl_prodID = Label(add_frame, text = "Product ID:", bd = 5)
        lbl_prodID.grid(row = 1, sticky = W)
        lbl_prodname = Label(add_frame, text = "Product Name:", bd = 5)
        lbl_prodname.grid(row = 2, sticky = W)
        lbl_price = Label(add_frame, text = "Price:", bd = 5)
        lbl_price.grid(row = 3, sticky = W)
        lbl_quantity = Label(add_frame, text = "Quantity:", bd = 5)
        lbl_quantity.grid(row = 4, sticky = W)
        lbl_quantype = Label(add_frame, text = "Quantity type:", bd = 5)
        lbl_quantype.grid(row = 5, sticky = W)

        ent_prodID = Label(add_frame, text = selecteditem[0])
        ent_prodID.grid(row = 1, column = 1, pady = 5, sticky = W)
        ent_prodname = Label(add_frame, text = selecteditem[1])
        ent_prodname.grid(row = 2, column = 1, pady = 5, sticky = W)
        ent_price = Label(add_frame, text = selecteditem[7])
        ent_price.grid(row = 3, column = 1, pady = 5, sticky = W)
        quantity.set("")
        ent_quantity = Entry(add_frame, textvariable = quantity, width = 10, validate = "key", validatecommand = (int_val, '%S'))
        ent_quantity.grid(row = 4, column = 1, pady = 5, sticky = W)
        ent_quant_type = Label(add_frame, text = selecteditem[6])
        ent_quant_type.grid(row = 5, column = 1, sticky = W)

        btn_cancel = Button(btn_frame, text = "Cancel", relief = FLAT, overrelief = SUNKEN, bg = '#79DC78', width = 15, command = mat_add.destroy)
        btn_cancel.grid(row = 0, column = 0, padx = 5)
        btn_edit = Button(btn_frame, text = "Save", relief = FLAT, overrelief = SUNKEN, bg = '#79DC78', width = 15, command = AddMats3)
        btn_edit.grid(row = 0, column = 1, padx = 5)

def AddMats3():
    dbFunc()
    curItem = inventory_tree.focus()
    contents =(inventory_tree.item(curItem))
    selecteditem = contents['values']
    curr.execute("""SELECT prodID FROM materials WHERE projID = ? and prodID = ?""", (str(proj_id.get()), selecteditem[0],))
    fetch = curr.fetchall()
    list_materials = [x[0] for x in fetch]
    in_stock = int(selecteditem[5]) - quantity.get()
    if quantity.get() < 0 or quantity.get() == "":
        error = tkMessageBox.showerror('Error', 'Invalid, Fill all entries')
    elif selecteditem[0] in list_materials:
        curr.execute("""UPDATE materials SET quantity = ? WHERE prodID = ?""", (in_stock, selecteditem[0], ))
        conn.commit()
    else:
        curr.execute("""UPDATE inventory SET instock = ? WHERE prodID = ?""", (in_stock, selecteditem[0], ))
        conn.commit()
        if in_stock < 1:
            curr.execute("""UPDATE inventory SET status = 'Out-of-stock' WHERE ProdID = ?""", (selecteditem[0], ))
            conn.commit()
        curr.execute("""INSERT INTO materials VALUES(?, ?, ?, ?, ?, ?)""", (str(proj_id.get()), str(selecteditem[0]), str(selecteditem[1]), int(selecteditem[5]), int(quantity.get()), str(selecteditem[6])))
        conn.commit()
        curr.close()
        conn.close()
        mat_add.destroy()
        InvRefresh()
        material_tree.delete(*material_tree.get_children())
        MatsDisplay()

def AddMatsClose():
    add_material.destroy()
    monitor_tree.delete(*monitor_tree.get_children())
    MonitorDisplay()
    tab_parent.add(tab1, text = "Project Monitor", image = pic_monitor, compound = LEFT, state = 'normal')
    tab_parent.add(tab2, text = "Inventory", image = pic_inventory, compound = LEFT, state = 'normal')
    tab_parent.add(tab3, text = "Customer Archive", image = pic_customer, compound = LEFT, state = 'normal')
    tab_parent.add(tab4, text = "Manage Accounts", image = pic_account, compound = LEFT, state = 'normal')
    tab_parent.select(tab_id = tab1)
    inventory_btn_add.configure(state = 'normal')
    inventory_btn_edit.configure(state = 'normal')
    inventory_btn_delete.configure(state = 'normal')
    inventory_btn_select.configure(state = 'disable')
    inventory_btn_done.configure(state = 'disable')
#-------------------------------------------------------------
def MonitorUpdate():
    if not monitor_tree.selection():
       print("ERROR")
    else:
        project = []
        progress = []
        global edit_proj
        edit_proj = Toplevel()
        edit_proj.title("Update Project")
        edit_proj.geometry("300x300")
        edit_proj.resizable(False, False)
        edit_proj.lift()
        edit_proj.attributes("-topmost", True)

        title_frame = Frame(edit_proj, relief = SOLID)
        title_frame.pack(side = TOP, padx = 10, pady = 10)
        edit_frame = Frame(edit_proj)
        edit_frame.pack(side = TOP, padx = 10, pady = 12)
        lbl_text = Label(title_frame, text = "Update Project", font = ("Consolas", 12), bg = '#ffffff', width = 30)
        lbl_text.pack(fill = X)

        curItem = monitor_tree.focus()
        contents =(monitor_tree.item(curItem))
        selecteditem = contents['values']
        dbFunc()
        curr.execute("""SELECT * FROM project WHERE projID = ?""", (selecteditem[0],))
        fetch1 = curr.fetchall()
        for x in fetch1[0]:
            project.append(x)
        curr.execute("""SELECT * FROM progress WHERE projID = ?""", (selecteditem[0],))
        fetch2 = curr.fetchall()
        for x in fetch2[0]:
            progress.append(x)
        curr.close()
        conn.close()

        if project[5] == 'Fullpayment' or progress[1] == 1:
            statepay = DISABLED
        else:
            statepay = NORMAL
        if project[6] == 0 or progress[2] == 1:
            statewood = DISABLED
        else:
            statewood = NORMAL
        if project[7] == 0 or progress[3] == 1:
            stateweld = DISABLED
        else:
            stateweld = NORMAL
        if project[8] == 0 or progress[4] == 1:
            statesew = DISABLED
        else:
            statesew = NORMAL
        if progress[5] == 1:
            statedelivery = DISABLED
        else:
            statedelivery = NORMAL
        progress_pay.set(progress[1])
        progress_woodworking.set(progress[2])
        progress_welding.set(progress[3])
        progress_sewing.set(progress[4])
        progress_delivery.set(progress[5])
        lbl_projID = Label(edit_frame, text = "Project ID:", bd = 5)
        lbl_projID.grid(row = 0, sticky = W)
        lbl_pay = Label(edit_frame, text = "Payment:", bd = 5)
        lbl_pay.grid(row = 1, sticky = W)
        lbl_ass = Label(edit_frame, text = "Assembly:", bd = 5)
        lbl_ass.grid(row = 2, sticky = W)
        lbl_delivery = Label(edit_frame, text = "Delivery/Pickup:", bd = 5)
        lbl_delivery.grid(row = 5, sticky = W)

        lbl_prodID = Label(edit_frame, text = selecteditem[0], bd = 5)
        lbl_prodID.grid(row = 0, column = 1, sticky = W)
        Checkbutton(edit_frame, text = project[5], variable = progress_pay, state = statepay).grid(row = 1, column = 1, columnspan = 3, sticky = W)
        Checkbutton(edit_frame, text = "Woodworking", variable = progress_woodworking, state = statewood).grid(row = 2, column = 1, columnspan = 3, sticky = W)
        Checkbutton(edit_frame, text = "Welding", variable = progress_welding, state = stateweld).grid(row = 3, column = 1, columnspan = 3, sticky = W)
        Checkbutton(edit_frame, text ="Sewing", variable = progress_sewing, state = statesew).grid(row = 4, column = 1, columnspan = 3, sticky = W)
        Checkbutton(edit_frame, text = project[9], variable = progress_delivery, state = statedelivery).grid(row = 5, column = 1, columnspan = 3, sticky = W)

        btn_cancel = Button(edit_frame, text = "Cancel", relief = FLAT, overrelief = SUNKEN, bg = '#69B0A8', width = 15, command = edit_proj.destroy)
        btn_cancel.grid(row = 6, column = 0, padx = 5, pady = 10)
        btn_update = Button(edit_frame, text = "Save Changes", relief = FLAT, overrelief = SUNKEN, bg = '#69B0A8', width = 15, command = MonitorUpdateFunc2)
        btn_update.grid(row = 6, column = 1, padx = 5)

def MonitorUpdateFunc2():
    dbFunc()
    curItem = monitor_tree.focus()
    contents =(monitor_tree.item(curItem))
    selecteditem = contents['values']
    curr.execute("""UPDATE progress SET payStat = ?, woodWorking = ?, welding = ?, sewing = ?, delivery = ? WHERE projID = ?""", (int(progress_pay.get()), int(progress_woodworking.get()), int(progress_welding.get()), int(progress_sewing.get()), int(progress_delivery.get()), selecteditem[0]))
    conn.commit()
    if progress_delivery.get() == 1:
        curr.execute("""UPDATE project SET status = ? WHERE projID = ?""", (str("Complete"), selecteditem[0],))
        conn.commit()        
    curr.close()
    conn.close()
    edit_proj.destroy()
#-------------------------------------------------------------------
def MonitorDelete():
    if not monitor_tree.selection():
       print("ERROR")
    else:
        curItem = monitor_tree.focus()
        contents =(monitor_tree.item(curItem))
        selecteditem = contents['values']
        if selecteditem[1] == "Complete":
            result = tkMessageBox.askquestion('Project Complete', 'Remove from Project Monitor?', icon="warning")
            if result == 'yes':
                dbFunc()
                curr.execute("""UPDATE project SET status = ? WHERE ProjID = ?""", (str("Archive"), selecteditem[0],))
                conn.commit()
                curItem = monitor_tree.focus()
                contents =(monitor_tree.item(curItem))
                selecteditem = contents['values']
                monitor_tree.delete(curItem)
                curr.close()
                conn.close()
        else:
            error = tkMessageBox.showerror('Error', 'Project not Complete.')
#--------------------------------------------------------------
def Exit():
    result = tkMessageBox.askquestion('Exit', "Exit Ben's Management System?", icon="warning")
    if result == 'yes':
        main.destroy()
        import aLogin





######################################################################Inventory#################################################################
################################################################################################################################################
def InvDisplay():
    dbFunc()
    curr.execute("""SELECT * FROM inventory ORDER BY prodID""")
    fetch = curr.fetchall()
    for data in fetch:
        inventory_tree.insert('', 'end', values=(data))
    curr.close()
    conn.close()
#-----------------------------------------------------------
def InvSearch():
    if inventory_search.get() != "":
        inventory_tree.delete(*inventory_tree.get_children())
        dbFunc()
        curr.execute("""SELECT * FROM inventory WHERE prodName LIKE ? or matType LIKE ? or color LIKE ? or dist LIKE ? or  quanType LIKE ? or status LIKE ?""", (str(inventory_search.get()), str(inventory_search.get()), str(inventory_search.get()), str(inventory_search.get()), str(inventory_search.get()), str(inventory_search.get()),))
        fetch = curr.fetchall()
        for data in fetch:
            inventory_tree.insert('', 'end', values=(data))
        curr.close()
        conn.close()
#--------------------------------------------------------------------
def InvRefresh():
    inventory_tree.delete(*inventory_tree.get_children())
    InvDisplay()
    inventory_search.set("")
#---------------------------------------------------------------------
def InvAdd():
    global add_prod
    add_prod = Toplevel()
    add_prod.title("New Product")
    add_prod.geometry("350x400")
    add_prod.configure(bg = '#C5FDB5')
    add_prod.resizable(False, False)
    add_prod.lift()
    add_prod.attributes("-topmost", True)
    add_prod.grab_set()

    dbFunc()
    curr.execute("""SELECT COUNT(*) FROM inventory""")
    fetch = curr.fetchone()
    n = int(1)
    for x in fetch:
            n+=x
    n2 = str(n)
    prod_id.set("#INV"+ n2.zfill(6))
    curr.close()
    conn.close()
    title_frame = Frame(add_prod, bg = '#C5FDB5', relief = SOLID, width = 600)
    title_frame.pack(side = TOP, pady = 15, fill = Y)
    lbl_text = Label(title_frame, text = "Add New Product", font = ('Consolas', 15), bg = '#ffffff', width = 35)
    lbl_text.pack(ipady = 8, fill = X)
    add_frame = Frame(add_prod, bg = '#C5FDB5')
    add_frame.pack(side = TOP)
    btn_frame = Frame(add_prod, bg = '#C5FDB5')
    btn_frame.pack(side = TOP)
    
    int_val = add_frame.register(IntValidation)
    lbl_prodID = Label(add_frame, text = "Product ID:", bg = '#C5FDB5', font = ('Consolas', 10), bd = 5)
    lbl_prodID.grid(row = 0, column = 0, sticky = W)
    lbl_prodname = Label(add_frame, text = "Product Name:", bg = '#C5FDB5', font = ('Consolas', 10), bd = 5)
    lbl_prodname.grid(row = 1, column = 0, sticky = W)
    lbl_mat = Label(add_frame, text = "Material Type:", bg = '#C5FDB5', font = ('Consolas', 10), bd = 5)
    lbl_mat.grid(row = 2, column = 0, sticky = W)
    lbl_color = Label(add_frame, text = "Color:", bg = '#C5FDB5', font = ('Consolas', 10), bd = 5)
    lbl_color.grid(row = 3, column = 0, sticky = W)
    lbl_distinct = Label(add_frame, text = "Other Distinctions:", bg = '#C5FDB5', font = ('Consolas', 10), bd = 5)
    lbl_distinct.grid(row = 4, column = 0, sticky = W)
    lbl_instock = Label(add_frame, text = "In-Stock:", bg = '#C5FDB5', font = ('Consolas', 10), bd = 5)
    lbl_instock.grid(row = 5, column = 0, sticky = W)
    lbl_price = Label(add_frame, text = "Price(₱):", bg = '#C5FDB5', font = ('Consolas', 10), bd = 5)
    lbl_price.grid(row = 6, column = 0, sticky = W)
    lbl_status = Label(add_frame, text = "Status:", bg = '#C5FDB5', font = ('Consolas', 10), bd = 5)
    lbl_status.grid(row = 7, column = 0, sticky = W)
    
    ent_prodID = Entry(add_frame, textvariable = prod_id, width = 25, state = 'disable')
    ent_prodID.grid(row = 0, column = 1, columnspan = 2, pady = 5, sticky = W)
    ent_prodname = Entry(add_frame, textvariable = prod_name, width = 25)
    ent_prodname.grid(row = 1, column = 1, columnspan = 2, pady = 5, sticky = W)
    ent_mat_type = ttk.Combobox(add_frame, width = 22, textvariable = mat_type, state = 'readonly')
    ent_mat_type['values'] = ("Wood", "Fabric", "Metal", "Other")
    ent_mat_type.grid(row = 2, column = 1, columnspan = 2, sticky = W)
    ent_color = Entry(add_frame, textvariable = color, width = 25)
    ent_color.grid(row = 3, column = 1, columnspan = 2, pady = 5, sticky = W)
    ent_distinct = Entry(add_frame, textvariable = distinction, width = 25)
    ent_distinct.grid(row = 4, column = 1, columnspan = 2, pady = 5, sticky = W)

    in_stock.set("")
    ent_instock = Entry(add_frame, textvariable = in_stock, width = 8, validate = "key", validatecommand = (int_val, '%S'))
    ent_instock.grid(row = 5, column = 1, pady = 5, sticky = W)
    ent_quant_type = ttk.Combobox(add_frame, width = 12, textvariable = quant_type, state = 'readonly')
    ent_quant_type['values'] = ("Pieces", "Sheets(Yard)", "Sheets(Meter)", "Packs", "Rolls")
    ent_quant_type.grid(row = 5, column = 2, sticky = W)
    price.set("")
    ent_price = Entry(add_frame, textvariable = price, width = 25, validate = "key", validatecommand = (int_val, '%S'))
    ent_price.grid(row = 6, column = 1, columnspan = 2, pady = 5, sticky = W)
    ent_status = ttk.Combobox(add_frame, width = 22, textvariable = status, state = 'readonly')
    ent_status['values'] = ("Available", "Out-of-stock", "En route", "Discontinued")
    ent_status.grid(row = 7, column = 1, columnspan = 2, sticky = W)

    btn_cancel = Button(btn_frame, text = "Cancel", relief = FLAT, overrelief = SUNKEN, bg = '#F2FCF2', font = ('Consolas', 10), width = 15, command = add_prod.destroy)
    btn_cancel.grid(row = 0, column = 0, padx = 5, pady = 15)
    btn_add = Button(btn_frame, text = "Save", relief = FLAT, overrelief = SUNKEN, bg = '#79DC78', font = ('Consolas', 10), width = 15, command = InvAddValidate)
    btn_add.grid(row = 0, column = 1, padx = 5)

def InvAddValidate():
    if prod_id.get() == "" or prod_name.get() == "" or mat_type.get() == "" or color.get() == "" or distinction.get() == "" or in_stock.get() == "" or quant_type.get() == "" or price.get() == "" or status.get() == "":
        add_prod.grab_release()
        error = tkMessageBox.showerror('Error', 'Invalid, Fill all entries')
    elif in_stock.get() < 1 and status.get() == 'Available':
        add_prod.grab_release()
        error = tkMessageBox.showerror('Error', 'Invalid, 0 Stock should either be Out-of-stock, En route or Discontinued')  
    else:
        InvAddFunc2()
    add_prod.grab_set()
        
def InvAddFunc2():
    dbFunc()
    curr.execute("""INSERT INTO inventory VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)""", (str(prod_id.get()), str(prod_name.get()), str(mat_type.get()), str(color.get()), str(distinction.get()), int(in_stock.get()), str(quant_type.get()), int(price.get()), str(status.get())))
    conn.commit()
    add_prod.destroy()
    prod_id.set("")
    prod_name.set("")
    mat_type.set("")
    color.set("")
    distinction.set("")
    in_stock.set("")
    quant_type.set("")
    price.set("")
    status.set("")
    curr.close()
    conn.close()
    InvRefresh()    
#------------------------------------------------------------------
def InvEdit():
    if not inventory_tree.selection():
       print("ERROR")
    else:
        global edit_prod
        edit_prod = Toplevel()
        edit_prod.title("Update Item")
        edit_prod.geometry("350x350")
        edit_prod.configure(bg = '#C5FDB5')
        edit_prod.resizable(False, False)
        edit_prod.lift()
        edit_prod.attributes("-topmost", True)
        edit_prod.grab_set()

        add_frame = Frame(edit_prod, bg = '#C5FDB5')
        add_frame.pack(side = TOP, padx = 10, pady = 12)
        btn_frame = Frame(edit_prod, bg = '#C5FDB5')
        btn_frame.pack(side = TOP, pady = 10)
        curItem = inventory_tree.focus()
        contents =(inventory_tree.item(curItem))
        selecteditem = contents['values']
        in_stock.set("")
        price.set("")
        status.set(selecteditem[8])
        prod_name.set(selecteditem[1])
        
        int_val = add_frame.register(IntValidation)
        lbl_prodID = Label(add_frame, text = "Product ID:", bg = '#C5FDB5', font = ('Consolas', 10), bd = 5)
        lbl_prodID.grid(row = 0, sticky = W)
        lbl_prodname = Label(add_frame, text = "Product Name:", bg = '#C5FDB5', font = ('Consolas', 10), bd = 5)
        lbl_prodname.grid(row = 1, sticky = W)
        lbl_mat = Label(add_frame, text = "Material Type:", bg = '#C5FDB5', font = ('Consolas', 10), bd = 5)
        lbl_mat.grid(row = 2, sticky = W)
        lbl_color = Label(add_frame, text = "Color:", bg = '#C5FDB5', font = ('Consolas', 10), bd = 5)
        lbl_color.grid(row = 3, sticky = W)
        lbl_distinct = Label(add_frame, text = "Other Distinctions:", bg = '#C5FDB5', font = ('Consolas', 10), bd = 5)
        lbl_distinct.grid(row = 4, sticky = W)
        lbl_instock = Label(add_frame, text = "In-Stock:", bg = '#C5FDB5', font = ('Consolas', 10), bd = 5)
        lbl_instock.grid(row = 5, sticky = W)
        lbl_price = Label(add_frame, text = "Price:", bg = '#C5FDB5', font = ('Consolas', 10), bd = 5)
        lbl_price.grid(row = 6, sticky = W)
        lbl_status = Label(add_frame, text = "Status:", bg = '#C5FDB5', font = ('Consolas', 10), bd = 5)
        lbl_status.grid(row = 7, sticky = W)

        ent_prodID = Label(add_frame, text = selecteditem[0], bg = '#C5FDB5', font = ('Consolas', 10))
        ent_prodID.grid(row = 0, column = 1, columnspan = 2, pady = 5, sticky = W)
        ent_prodname = Label(add_frame, text = selecteditem[1], bg = '#C5FDB5', font = ('Consolas', 10))
        ent_prodname.grid(row = 1, column = 1, columnspan = 2, pady = 5, sticky = W)
        ent_mat_type = Label(add_frame, text = selecteditem[2], bg = '#C5FDB5', font = ('Consolas', 10))
        ent_mat_type.grid(row = 2, column = 1, columnspan = 2, sticky = W)
        ent_color = Label(add_frame, text = selecteditem[3], bg = '#C5FDB5', font = ('Consolas', 10))
        ent_color.grid(row = 3, column = 1, columnspan = 2, pady = 5, sticky = W)
        ent_distinct = Label(add_frame, text = selecteditem[4], bg = '#C5FDB5', font = ('Consolas', 10))
        ent_distinct.grid(row = 4, column = 1, columnspan = 2, pady = 5, sticky = W)

        ent_instock = Entry(add_frame, textvariable = in_stock, width = 10, validate = "key", validatecommand = (int_val, '%S'))
        ent_instock.grid(row = 5, column = 1, pady = 5, sticky = W)
        ent_quant_type = Label(add_frame, text = selecteditem[6], bg = '#C5FDB5', font = ('Consolas', 10))
        ent_quant_type.grid(row = 5, column = 2, sticky = W)
        ent_price = Entry(add_frame, textvariable = price, width = 20, validate = "key", validatecommand = (int_val, '%S'))
        ent_price.grid(row = 6, column = 1, columnspan = 2, pady = 5, sticky = W)
        ent_status = ttk.Combobox(add_frame, width = 18, textvariable = status, state = 'readonly')
        ent_status['values'] = ("Available", "Out-of-stock", "En route", "Discontinued")
        ent_status.grid(row = 7, column = 1, columnspan = 2, sticky = W)

        btn_cancel = Button(btn_frame, text = "Cancel", relief = FLAT, overrelief = SUNKEN, bg = '#F2FCF2', width = 15, command = edit_prod.destroy)
        btn_cancel.grid(row = 0, column = 0, padx = 5)
        btn_edit = Button(btn_frame, text = "Save Changes", relief = FLAT, overrelief = SUNKEN, bg = '#79DC78', width = 15, command = InvEditValidate)
        btn_edit.grid(row = 0, column = 1, padx = 5)

def InvEditValidate():
    if in_stock.get() == "" or price.get() == "" or status.get() == "":
        edit_prod.grab_release()
        error = tkMessageBox.showerror('Error', 'Invalid, Fill all entries')
    elif in_stock.get() < 1 and status.get() == 'Available':
        edit_prod.grab_release()
        error = tkMessageBox.showerror('Error', 'Invalid, 0 Stock should either be Out-of-stock, En route or Discontinued')  
    else:
        InvEditFunc2()

def InvEditFunc2():
    dbFunc()
    curItem = inventory_tree.focus()
    contents =(inventory_tree.item(curItem))
    selecteditem = contents['values']
    curr.execute("""UPDATE inventory SET instock = ?, price = ?, status = ?  WHERE ProdName = ?""", (int(in_stock.get()), int(price.get()), str(status.get()), str(prod_name.get())))
    conn.commit()
    curr.close()
    conn.close()
    InvRefresh()
    edit_prod.grab_release()
    edit_prod.destroy()
#-------------------------------------------------------------------
def InvDelete():
    if not inventory_tree.selection():
       print("ERROR")
    else:
        result = tkMessageBox.askquestion('Delete', 'Delete product from inventory?', icon="warning")
        if result == 'yes':
            curItem = inventory_tree.focus()
            contents =(inventory_tree.item(curItem))
            selecteditem = contents['values']
            inventory_tree.delete(curItem)            
            dbFunc()
            curr.execute("""DELETE FROM inventory WHERE prodName = ?""", (selecteditem[1],))
            conn.commit()
            curr.close()
            conn.close()





##############################3##############################Customer Archive###################################################################
################################################################################################################################################
def CustDisplay():
    dbFunc()
    curr.execute("""SELECT * FROM customer GROUP BY customerID""")
    fetch = curr.fetchall()
    for data in fetch:
        cust_tree.insert('', 'end', values=(data))
    curr.close()
    conn.close()

def ViewDisplay():
    dbFunc()
    curItem = cust_tree.focus()
    contents =(cust_tree.item(curItem))
    selecteditem = contents['values']
    curr.execute("""SELECT projID, startDate, endDate, desc, payStat, delivery FROM project WHERE custID LIKE ?""", (selecteditem[1], ))
    fetch = curr.fetchall()
    for data in fetch:
        view_tree.insert('', 'end', values=(data))
    curr.close()
    conn.close()

def CustSearch():
    if cust_search.get() != "":
        cust_tree.delete(*cust_tree.get_children())
        dbFunc()
        curr.execute("""SELECT * FROM customer WHERE projID LIKE ? or customerID LIKE ? or fName LIKE ? or lName LIKE ?""", (str(cust_search.get()), str(cust_search.get()), str(cust_search.get()), str(cust_search.get()), ))
        fetch = curr.fetchall()
        for data in fetch:
            cust_tree.insert('', 'end', values=(data))
        curr.close()
        conn.close()

def CustRefresh():
    cust_tree.delete(*cust_tree.get_children())
    CustDisplay()
    cust_search.set("")

def CustView():
    if not cust_tree.selection():
       print("ERROR")
    else:
        global view_cust, view_tree
        view_cust = Toplevel()
        view_cust.title("Archive")
        view_cust.geometry("350x350")
        view_cust.configure(bg = '#deecf6')
        view_cust.resizable(False, False)
        view_cust.lift()
        view_cust.attributes("-topmost", True)
        view_cust.grab_set()
        cust_frame = LabelFrame(view_cust, text = "Customer Information", bg = '#deecf6', font = ('Consolas', 10))
        cust_frame.pack(side = TOP, fill = X, pady = 10, padx = 10)
        tree_frame = Frame(view_cust, bg = '#deecf6')
        tree_frame.pack(side = TOP, fill = X, pady = 10, padx = 10)
        curItem = cust_tree.focus()
        contents =(cust_tree.item(curItem))
        selecteditem = contents['values']
        customer = str(selecteditem[1] + "\t" + selecteditem[4] +  ", "+ selecteditem[3])
        lbl_customer = Label(cust_frame, text = customer, bg = '#deecf6', font = ('Consolas', 10))
        lbl_customer.grid(row = 0)
        lbl_address = Label(cust_frame, text = selecteditem[5], bg = '#deecf6', font = ('Consolas', 10))
        lbl_address.grid(row = 1)
        lbl_contact = Label(cust_frame, text = selecteditem[6], bg = '#deecf6', font = ('Consolas', 10))
        lbl_contact.grid(row = 2)

        view_scrollbarx = Scrollbar(tree_frame, orient = HORIZONTAL)
        view_scrollbary = Scrollbar(tree_frame, orient = VERTICAL)
        view_tree = ttk.Treeview(tree_frame, columns=('ProjectID', 'StartDate', 'EndDate', 'Description', 'PayStat', 'Delivery'), selectmode="extended", height=100, yscrollcommand = view_scrollbary.set, xscrollcommand = view_scrollbarx.set)
        view_scrollbary.config(command = view_tree.yview)
        view_scrollbary.pack(side = RIGHT, fill = Y)
        view_scrollbarx.config(command = view_tree.xview)
        view_scrollbarx.pack(side = BOTTOM, fill = X)
        view_tree.heading('ProjectID', text = "Project ID",anchor = W)
        view_tree.heading('StartDate', text = "Start Date",anchor = W)
        view_tree.heading('EndDate', text = "Completion Date",anchor = W)
        view_tree.heading('Description', text = "Description",anchor = W)
        view_tree.heading('PayStat', text = "Payment",anchor = W)
        view_tree.heading('Delivery', text = "Delivery",anchor = W)
        view_tree.column('#0', stretch = NO, minwidth = 0, width = 0)
        view_tree.column('#1', width = 80)
        view_tree.column('#2', width = 70)
        view_tree.column('#3', width = 100)
        view_tree.column('#4', width = 150)
        view_tree.column('#5', width = 80)
        view_tree.column('#6', width = 70)
        view_tree.pack(anchor = W)
        ViewDisplay()

#################################################################ProjectMonitor#################################################################
pic_gantt = PhotoImage(file = r"D:\Users\Diane\Desktop\Upholstery-Management-System-main\gantt.png")
pic_open = PhotoImage(file = r"D:\Users\Diane\Desktop\Upholstery-Management-System-main\open.png")
pic_refresh = PhotoImage(file = r"D:\Users\Diane\Desktop\Upholstery-Management-System-main\refresh.png")
pic_add = PhotoImage(file = r"D:\Users\Diane\Desktop\Upholstery-Management-System-main\add.png")
pic_edit = PhotoImage(file = r"D:\Users\Diane\Desktop\Upholstery-Management-System-main\edit.png")
pic_delete = PhotoImage(file = r"D:\Users\Diane\Desktop\Upholstery-Management-System-main\delete.png")
pic_exit = PhotoImage(file = r"D:\Users\Diane\Desktop\Upholstery-Management-System-main\exit.png")
count = 0
monitor_top_frame = Frame(tab1, bd = 1, bg = '#B6E0DC')
monitor_top_frame.pack(side = TOP, pady = 10)
monitor_tree_frame = Frame(tab1, bg = '#B6E0DC')
monitor_tree_frame.pack(side = LEFT, fill = X)

monitor_btn_open = Button(monitor_top_frame, text = "Gantt Chart", bg = '#ffffff', relief = FLAT, overrelief = SUNKEN, image = pic_gantt, compound = TOP, width=100, font = ('Consolas', 11), command = MonitorGantt)
monitor_btn_open.grid(row = 0, column = 0, padx = 10)
monitor_btn_open = Button(monitor_top_frame, text = "Open", bg = '#ffffff', relief = FLAT, overrelief = SUNKEN, image = pic_open, compound = TOP, width=100, font = ('Consolas', 11), command = lambda: MonitorTable(count))
monitor_btn_open.grid(row = 0, column = 1, padx = 10)
monitor_btn_refresh = Button(monitor_top_frame, text = "Refresh", bg = '#ffffff', relief = FLAT, overrelief = SUNKEN, image = pic_refresh, compound = TOP, width=100, font = ('Consolas', 11), command = lambda: MonitorRefresh(count))
monitor_btn_refresh.grid(row = 0, column = 2, padx = 10)
monitor_btn_add = Button(monitor_top_frame, text="Add", bg = '#ffffff', relief = FLAT, overrelief = SUNKEN, image = pic_add, compound = TOP, width=100, font = ('Consolas', 11), command = MonitorAdd)
monitor_btn_add.grid(row = 0, column = 3, padx = 10)
monitor_btn_edit = Button(monitor_top_frame, text = "Update", bg = '#ffffff', relief = FLAT, overrelief = SUNKEN, image = pic_edit, compound = TOP, width=100, font = ('Consolas', 11), command = MonitorUpdate)
monitor_btn_edit.grid(row = 0, column = 4, padx = 10)
monitor_btn_delete = Button(monitor_top_frame, text = "Remove", bg = '#ffffff', relief = FLAT, overrelief = SUNKEN, image = pic_delete, compound = TOP, width = 100, font = ('Consolas', 11), command = MonitorDelete)
monitor_btn_delete.grid(row = 0, column = 5, padx = 10)
monitor_btn_delete = Button(monitor_top_frame, text = "Log-out", bg = '#69B0A8', fg = '#ffffff', relief = FLAT, overrelief = SUNKEN, image = pic_exit, compound = TOP, width = 100, font = ('Consolas', 11), command = Exit)
monitor_btn_delete.grid(row = 0, column = 6, padx = 10)

monitor_scrollbarx = Scrollbar(monitor_tree_frame, orient = HORIZONTAL)
monitor_scrollbary = Scrollbar(monitor_tree_frame, orient = VERTICAL)
monitor_tree = ttk.Treeview(monitor_tree_frame, columns=('ProjectID', 'Status'), selectmode="extended", height=100, yscrollcommand = monitor_scrollbary.set, xscrollcommand = monitor_scrollbarx.set)
monitor_scrollbary.config(command = monitor_tree.yview)
monitor_scrollbary.pack(side = RIGHT, fill = Y)
monitor_scrollbarx.config(command = monitor_tree.xview)
monitor_scrollbarx.pack(side = BOTTOM, fill = X)
monitor_tree.heading('ProjectID', text = "Project ID",anchor = W)
monitor_tree.heading('Status', text = "Status",anchor = W)
monitor_tree.column('#0', stretch = NO, minwidth = 0, width = 0)
monitor_tree.column('#1', width = 100)
monitor_tree.column('#2', width = 70)
monitor_tree.pack(anchor = W)
MonitorDisplay()

##############################Inventory###############################
inventory_top_frame = Frame(tab2, width = 600, bg = '#79DC78', relief = GROOVE, bd = 1)
inventory_top_frame.pack(side = TOP, fill = X)
inventory_left_frame = Frame(tab2, width = 600, bg = '#79DC78', relief = GROOVE, bd = 1)
inventory_left_frame.pack(side = LEFT, fill = Y)
inventory_tree_frame = Frame(tab2, width = 600, bg = '#79DC78')
inventory_tree_frame.pack(side = RIGHT)

inventory_search_entry = Entry(inventory_top_frame, textvariable = inventory_search, width = 30)
inventory_search_entry.pack(side = RIGHT, padx = 10, pady = 10, fill = X)
inventory_btn_search = Button(inventory_top_frame, text = "Search", bg = '#C5FDB5', relief = FLAT, overrelief = SUNKEN, width = 15, font = ('Consolas', 10), command = InvSearch)
inventory_btn_search.pack(side = RIGHT, padx = 10, pady = 10, fill = X)
inventory_btn_refresh = Button(inventory_left_frame, text = "Refresh", bg = '#C5FDB5', relief = FLAT, overrelief = SUNKEN, width = 15, font = ('Consolas', 10), command = InvRefresh)
inventory_btn_refresh.pack(side = TOP, padx = 10, pady = 10, fill = X)
inventory_btn_add = Button(inventory_left_frame, text = "Add", bg = '#C5FDB5', relief = FLAT, overrelief = SUNKEN, width = 15, font = ('Consolas', 10), command = InvAdd)
inventory_btn_add.pack(side = TOP, padx = 10, pady = 10, fill = X)
inventory_btn_edit = Button(inventory_left_frame, text = "Update", bg = '#C5FDB5', relief = FLAT, overrelief = SUNKEN, width = 15, font = ('Consolas', 10), command = InvEdit)
inventory_btn_edit.pack(side = TOP, padx = 10, pady = 10, fill = X)
inventory_btn_delete = Button(inventory_left_frame, text = "Delete", bg = '#C5FDB5', relief = FLAT, overrelief = SUNKEN, width = 15, font = ('Consolas', 10), command = InvDelete)
inventory_btn_delete.pack(side = TOP, padx = 10, pady = 10, fill = X)
inventory_btn_select = Button(inventory_left_frame, text = "Select", bg = '#deecf6', relief = FLAT, overrelief = SUNKEN, width = 15, font = ('Consolas', 10), command = AddMats2, state = 'disable')
inventory_btn_select.pack(side = TOP, padx = 10, pady = 10, fill = X)
inventory_btn_done = Button(inventory_left_frame, text = "Done", bg = '#deecf6', relief = FLAT, overrelief = SUNKEN, width = 15, font = ('Consolas', 10), command = AddMatsClose, state = 'disable')
inventory_btn_done.pack(side = TOP, padx = 10, pady = 10, fill = X)

inventory_scrollbarx = Scrollbar(inventory_tree_frame, orient = HORIZONTAL)
inventory_scrollbary = Scrollbar(inventory_tree_frame, orient = VERTICAL)
inventory_tree = ttk.Treeview(inventory_tree_frame, columns = ('ProductID', 'ProductName', 'MaterialType','Color', 'OtherDistinctions', 'In-stock', 'QuantityType', 'Price', 'Status'), selectmode = "extended", height = 100, yscrollcommand = inventory_scrollbary.set, xscrollcommand = inventory_scrollbarx.set)
inventory_scrollbary.config(command = inventory_tree.yview)
inventory_scrollbary.pack(side = RIGHT, fill = Y)
inventory_scrollbarx.config(command = inventory_tree.xview)
inventory_scrollbarx.pack(side = BOTTOM, fill = X)
inventory_tree.heading('ProductID', text = "Product ID", anchor = W)
inventory_tree.heading('ProductName', text = "Product Name", anchor = W)
inventory_tree.heading('MaterialType', text = "Material Type", anchor = W)
inventory_tree.heading('Color', text = "Color",anchor = W)
inventory_tree.heading('OtherDistinctions', text = "Other Distinctions", anchor = W)
inventory_tree.heading('In-stock', text = "In-stock", anchor = W)
inventory_tree.heading('QuantityType', text = "Quantity Type", anchor = W)
inventory_tree.heading('Price', text = "Price", anchor = W)
inventory_tree.heading('Status', text = "Status", anchor = W)
inventory_tree.column('#0', stretch = NO, minwidth = 0, width = 0)
inventory_tree.column('#1', width = 70)
inventory_tree.column('#2', width = 120)
inventory_tree.column('#3', width = 120)
inventory_tree.column('#4', width = 70)
inventory_tree.column('#5', width = 150)
inventory_tree.column('#6', width = 70)
inventory_tree.column('#7', width = 120)
inventory_tree.column('#8', width = 70)
inventory_tree.column('#9', width = 70)
inventory_tree.pack()
InvDisplay()

###########################Customer Archive###########################
cust_search_frame = Frame(tab3, width=600, bg = '#78B3DD', relief = GROOVE, bd=1)
cust_search_frame.pack(side = TOP, fill = X)
cust_menu_frame = Frame(tab3, bg = '#78B3DD', relief = GROOVE, bd=1)
cust_menu_frame.pack(side = LEFT, fill = Y)
cust_tree_frame = Frame(tab3, width=600, bg = '#78B3DD')
cust_tree_frame.pack(side = TOP)

cust_search_entry = Entry(cust_search_frame, textvariable = cust_search, width=20)
cust_search_entry.pack(side=RIGHT, padx=10, pady=10, fill=X)
cust_btn_search = Button(cust_search_frame, text="Search", bg = '#deecf6', relief = FLAT, overrelief = SUNKEN, width = 15, font = ('Consolas', 10), command = CustSearch)
cust_btn_search.pack(side=RIGHT, padx=10, pady=10, fill=X)

cust_btn_reset = Button(cust_menu_frame, text = "Refresh", bg = '#deecf6', relief = FLAT, overrelief = SUNKEN, width = 15, font = ('Consolas', 10), command = CustRefresh)
cust_btn_reset.pack(side = TOP, padx = 10, pady = 10, fill = X)
cust_btn_view = Button(cust_menu_frame, text = "View", bg = '#deecf6', relief = FLAT, overrelief = SUNKEN, width = 15, font = ('Consolas', 10), command = CustView)
cust_btn_view.pack(side = TOP, padx = 10, pady = 10, fill = X)
cust_btn_select = Button(cust_menu_frame, text = "Select", bg = '#C5FDB5', relief = FLAT, overrelief = SUNKEN, width = 15, font = ('Consolas', 10), command = ExistingCustomerSelect, state = 'disable')
cust_btn_select.pack(side = TOP, padx = 10, pady = 10, fill = X)
cust_btn_back = Button(cust_menu_frame, text = "Back", bg = '#C5FDB5', relief = FLAT, overrelief = SUNKEN, width = 15, font = ('Consolas', 10), command = ExistingCustomerBack, state = 'disable')
cust_btn_back.pack(side = TOP, padx = 10, pady = 10, fill = X)

cust_scrollbarx = Scrollbar(cust_tree_frame, orient = HORIZONTAL)
cust_scrollbary = Scrollbar(cust_tree_frame, orient = VERTICAL)
cust_tree = ttk.Treeview(cust_tree_frame, columns = ('ProjectID', 'CustomerID', 'TransactionDate', 'FirstName', 'LastName', 'Address', 'Contact'), selectmode = "extended", height = 100, yscrollcommand = cust_scrollbary.set, xscrollcommand = cust_scrollbarx.set)
cust_scrollbary.config(command = cust_tree.yview)
cust_scrollbary.pack(side = RIGHT, fill = Y)
cust_scrollbarx.config(command = cust_tree.xview)
cust_scrollbarx.pack(side = BOTTOM, fill = X)
cust_tree.heading('ProjectID', text = "Project ID", anchor = W)
cust_tree.heading('CustomerID', text = "Customer ID", anchor = W)
cust_tree.heading('TransactionDate', text = "Transaction Date", anchor = W)
cust_tree.heading('FirstName', text = "First Name", anchor = W)
cust_tree.heading('LastName', text = "Last Name", anchor = W)
cust_tree.heading('Address', text = "Address", anchor = W)
cust_tree.heading('Contact', text = "Contact Number", anchor = W)
cust_tree.column('#0', stretch = NO, minwidth = 0, width = 0)
cust_tree.column('#1', stretch = NO, minwidth = 0, width = 0)
cust_tree.column('#2', width = 120)
cust_tree.column('#3', width = 120)
cust_tree.column('#4', width = 120)
cust_tree.column('#5', width = 120)
cust_tree.column('#6', width = 260)
cust_tree.column('#7', width = 120)
cust_tree.pack()
CustDisplay()
