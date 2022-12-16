import sqlite3
conn = sqlite3.connect("bens.db")
curr = conn.cursor()

#Project
curr.execute("""CREATE TABLE project(projID varchar(255), custID varchar(255), startDate varchar(255), endDate varchar(255), desc varchar(255), payStat varchar(12), woodWorking int(9) not null, welding int(9) not null, sewing int(9) not null, delivery varchar(10), status varchar(10))""")
#data = ("#PROJ000001", "#CUS000001", "2020-09-27", "2020-10-10", "upuan na mukha ni eugeo", "Fullpayment", 1, 1, 1, "Delivery", "In Progress")
#curr.execute("""INSERT INTO project VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", data)

#data = ("#PROJ000002", "#CUS000002", "2020-09-28", "2020-10-01", "sample", "Downpayment", 1, 0, 1, "Pick-up", "In Progress")
#curr.execute("""INSERT INTO project VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", data)

#Progress
curr.execute("""CREATE TABLE progress(projID varchar(255), payStat int(9) not null, woodWorking int(9) not null, welding int(9) not null, sewing int(9) not null, delivery int(9) not null)""")
#data = ("#PROJ000001", 1, 0, 1, 0, 0)
#curr.execute("""INSERT INTO progress VALUES(?, ?, ?, ?, ?, ?)""", data)

#data = ("#PROJ000002", 1, 0, 0, 1, 0)
#curr.execute("""INSERT INTO progress VALUES(?, ?, ?, ?, ?, ?)""", data)

#Inventory
curr.execute("""CREATE TABLE inventory(prodID varchar(255), prodName varchar(255), matType varchar(255), color varchar(255), dist varchar(255), instock int(255) not null, quanType varchar(255), price int(255) not null, status varchar(255))""")
#data = ("#INV000001", "sample", "Metal", "Blue", "sample", 888,"Pieces", 888, "Available")
#curr.execute("""INSERT INTO inventory VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)""", data)

#data = ("#INV000002", "Dinowaifuu", "Metal", "Pink", "trash", 15,"Pieces", 1, "Available")
#curr.execute("""INSERT INTO inventory VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)""", data)

#Customer
curr.execute("""CREATE TABLE customer(projID varchar(255), customerID varchar(255), transactDate varchar(255), fName varchar(255), lName varchar(255), address varchar(255), contact archar(255))""")
#data = ("#PROJ000001", "#CUS000001", "2020-09-27", "Kazuto", "Kirigaya", "Forest House K4 22nd Floor Aincrad", "091234586953")
#curr.execute("""INSERT INTO customer VALUES(?, ?, ?, ?, ?, ?, ?)""", data)

#data = ("#PROJ000002", "#CUS000002", "2020-09-28", "Satoru", "Fujinuma", "waley kase a city withouth me", "091234586953")
#curr.execute("""INSERT INTO customer VALUES(?, ?, ?, ?, ?, ?, ?)""", data)

#Materials
curr.execute("""CREATE TABLE materials(projID varchar(255), prodID varchar(255), prodName varchar(255), price int(9) not null, quantity int(9) not null, quantType varchar(255))""")
#data = ("#PROJ000001", "#INV000001", "sample", 888, 9, "Pieces")
#curr.execute("""INSERT INTO materials VALUES(?, ?, ?, ?, ?, ?)""", data)

#data = ("#PROJ000001", "#INV000002", "Dinowaiuu", 1, 21, "Pieces")
#curr.execute("""INSERT INTO materials VALUES(?, ?, ?, ?, ?, ?)""", data)

#data = ("#PROJ000002", "#INV000002", "Dinowaiuu", 1, 10, "Pieces")
#curr.execute("""INSERT INTO materials VALUES(?, ?, ?, ?, ?, ?)""", data)

#Account
curr.execute("""CREATE TABLE account(employee varchar(255), username varchar(255), password varchar(255), authority varchar(255))""")
data = ("Uchiha Sasuke", "admin", "1234", "Administrator")
curr.execute("""INSERT INTO account VALUES(?, ?, ?, ?)""", data)
#data = ("Kageyama Shigeo", "tensai", "baka", "Project Coordinator")
#curr.execute("""INSERT INTO account VALUES(?, ?, ?, ?)""", data)
#data = ("weebshit", "astig", "ko", "Inventory Clerk")
#curr.execute("""INSERT INTO account VALUES(?, ?, ?, ?)""", data)

conn.commit()
conn.close()

#required conn.commit() conn.close()
