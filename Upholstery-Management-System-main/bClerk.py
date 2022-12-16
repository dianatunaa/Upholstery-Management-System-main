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

pic_monitor = PhotoImage(file = r'D:\Users\Diane\Desktop\Upholstery-Management-System-main\monitor.png')
pic_inventory = PhotoImage(file = r'D:\Users\Diane\Desktop\Upholstery-Management-System-main\inv.png')

tab_parent.add(tab1, text = "Project Monitor", image = pic_monitor, compound = LEFT)
tab_parent.add(tab2, text = "Inventory", image = pic_inventory, compound = LEFT)
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





#################################################################ProjectMonitor#################################################################
pic_gantt = PhotoImage(file = r"D:\Users\Diane\Desktop\Upholstery-Management-System-main\gantt.png")
pic_open = PhotoImage(file = r"D:\Users\Diane\Desktop\Upholstery-Management-System-main\open.png")
pic_refresh = PhotoImage(file = r"D:\Users\Diane\Desktop\Upholstery-Management-System-main\refresh.png")
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
monitor_btn_delete = Button(monitor_top_frame, text = "Log-out", bg = '#69B0A8', fg = '#ffffff', relief = FLAT, overrelief = SUNKEN, image = pic_exit, compound = TOP, width = 100, font = ('Consolas', 11), command = Exit)
monitor_btn_delete.grid(row = 0, column = 3, padx = 10)

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
