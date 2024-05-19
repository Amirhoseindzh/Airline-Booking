import mysql.connector
from csv import DictWriter
from csv import DictReader
import os
        
print('> ENTER THE DATABASE INFORMATIONS  :\n')
host=input('HOST NAME :')
username=input('USERNAME :')
password=input('PASSWORD :')
database=input('DATABASE :') 

conn =mysql.connector.connect(host=host,username=username,password=password , database=database)
my_cursor = conn.cursor(dictionary=True)


print("\n********************WELCOME TO FLIGHT BOOKING SYSTEM***********************")

counter = 0
while counter<1:
    acc = input("\nDO YOU HAVE A ACCOUNT (Y/N)?-")
    e = []
    if acc=='y' or acc=='yes' or acc=='Y' or acc=='YES':
        
        my_cursor.execute("SHOW TABLES LIKE 'customers'")
        result_2 = my_cursor.fetchone()
        if 'customers' not in str(result_2):
                print("\n YOU HAVE NOT AN ACCOUNT :(  --> PLEASE FIRST CREAT ONE <-- ")
                print('\n ----------------------------------------------------------')
                 
    
        else:    
            count=0
            while count<1:
                email = input("\nENTER YOUR EMAIL ID:-")
                e.append(email)
                pas = (input("\nENTER YOUR PASSWORD:-"))
                otp = (input("\nENTER A OTP CODE ON YOUR EMAIL AND PHONE NO:-"))

                my_cursor.execute("SELECT email,password,otp FROM customers")
                result_1 = my_cursor.fetchall()
                for i in range(len(result_1)):
                    
                    if (result_1[i]['email']==email) and (result_1[i]['password']==pas) and (result_1[i]['otp']==otp) :
                        
                        print("\n-------LOGIN SUCCESSFUL-------")
                        count=1
                        break
                    else:
                        pass
                else:
                    print("\n  -- LOGIN FAILURE. TRY AGAIN ! --")

                
                    

            counter=1


    elif acc=='n' or acc=='no' or acc=='N' or acc=='NO':
        nam = input("\nENTER YOUR FULL NAME:-")
        pn = int(input("\nENTER YOUR PHONE NO:-"))
        city = input("\nENTER YOUR CITY NAME:-")
        state = input("\nENTER YOUR STATE:-")
        em = input("\nENTER YOUR EMAIL ID:-")
        e.append(em)
        passw = input("\nENTER YOUR PASSWORD:-")
        print(f"\nOTP SEND TO {pn} AND {em}")
        ot = int(input("\nENTER THE OTP NO:-"))

        
        stmt = "SHOW TABLES LIKE 'customers'"
        my_cursor.execute(stmt)
        result = my_cursor.fetchone()

        if 'customers' not in str(result):
            my_cursor.execute("CREATE TABLE customers (id INT AUTO_INCREMENT PRIMARY KEY, nam VARCHAR(255), phoneNo VARCHAR(255) , city VARCHAR(255) ,state VARCHAR(255) , email VARCHAR(255),password VARCHAR(255), otp VARCHAR(255)) ")
        
        sql = "INSERT INTO customers (nam, phoneNo ,city , state , email, password , OTP ) VALUES (%s, %s,%s,%s,%s,%s,%s)"
        val = [(nam,pn,city,state,em,passw,ot)]
        my_cursor.executemany(sql, val)
        conn.commit()
            
        print("\n-------YOUR ACCOUNT IS CREATED SUCCESSFULLY-------")
        counter = 1

    else:
        print('\n>> WRONG INPUT ! TRY AGAIN .. ')


print("\nhow do you want to search your flight by")
print("1.flight number")
print("2.mannualy")

ans = int(input("\nAnswer (1/2):-"))


if ans==1:
    num = (input("\nENTER FLIGHT NUMBER:-"))
    query = "SELECT * FROM FLIGHTS WHERE FLIGHT_NO = '{}' ".format(num)
    my_cursor.execute(query)
    print("\nYOUR FLIGHT DATA IS-------")
    for a in my_cursor:
        print(a)

deplo = []
arrlo = []
fli = []

def flight_data():   
    departure = input("\nENTER YOUR DEPARTURE LOCAION:-")
    arrival = input("\nENTER YOUR ARRIVAL LOCATION:-")
    query2 = "SELECT AIRLINES_NAME FROM FLIGHTS WHERE DEPARTURE = '{}' AND DESTINATION = '{}'".format(departure, arrival)
    deplo.append(departure)
    arrlo.append(arrival)
    my_cursor.execute(query2)
    print("\nYOUR REQUIRED FLIGHTS ARE------")
    for b in my_cursor:
        print(b) 
    fly = input("\nENTER A FLIGHT NAME YOU WANT:-")
    fli.append(fly)
    print("\nHEAR THE DETAILS OF YOUR FLIGHT--")
    query3 = "SELECT * FROM FLIGHTS WHERE AIRLINES_NAME = '{}' AND DEPARTURE = '{}' AND DESTINATION = '{}' ".format(fly, departure, arrival)
    my_cursor.execute(query3)
    for c in my_cursor:
        return print(c)
        

if ans==2:
    flight_data()
    

con = input("\nWOULD YOU LIKE TO CONTINUE (Y/N):-")
while True:
    if con=='n' or con=='N' or con=='no' or con=='NO':
        flight_data()
    else:
        break

passenger = int(input("\nENTER A NUMBER OF PASSANGERS:-"))

nam=[]
ag=[]
gen=[]

def pass_data():
    name = input("\nENTER A NAME OF A PASSENGER:-")
    age = int(input(f"\nENTER THE AGE OF {name}:-"))
    gender = input("\nMALE/FEMALE:-")
    nam.append(name)
    ag.append(age)
    gen.append(gender)
    with open('userdata.csv', 'a', newline='') as csvfile:
        csvwriter = DictWriter(csvfile, fieldnames=['name', 'age', 'gender'])
        csvwriter.writeheader()
        csvwriter.writerow({'name':name, 'age':age, 'gender':gender})
    return print("\n-------DATA ENTERED SUCCESSFULLY-------")        

for d in range(passenger):
        pass_data()

def read_csv():
    with open('userdata.csv',mode='r') as csvreader:
        reader = DictReader(csvreader)
        for row in reader:
            if row['name']=='name':
                pass
            else:
                print(f"name :{row['name']} , age : {row['age']} , gender : {row['gender']}")
    os.remove(r'userdata.csv')
    return print("------------------------------------")
read_csv()
print("\nCHECK YOUR DETAILS----")

ch = input("\nDO YOU WANT TO CONTINUE (Y/N):-")

while True:
    if ch=='n' or ch=='N' or ch=='no' or ch=='NO':
        for e in range(passenger):
            pass_data()
        read_csv()
    else:
        break

print("\nCHOOSE THE CLASS YOU WANT:-")
print("1.ECONOMY CLASS")
print("2.BUSINESS CLASS (+20% CHARGES)")
print("3.FIRST CLASS (+40% CHARGES)")

flo = []
tdep = []
tarr= []

def fl_nm():
    query4 = "SELECT FLIGHT_NO FROM FLIGHTS WHERE airlines_name = '{}' and DEPARTURE = '{}' and DESTINATION = '{}' ".format (fli[0], deplo[0], arrlo[0])
    my_cursor.execute(query4)
    for f in my_cursor:
        flo.append(f)

    query5 = "SELECT TIME_OF_DEPARTURE FROM FLIGHTS WHERE airlines_name = '{}' and DEPARTURE = '{}' and DESTINATION = '{}' ".format (fli[0], deplo[0], arrlo[0])
    my_cursor.execute(query5)
    for g in my_cursor:
        tdep.append(g)

    query6 = "SELECT TIME_OF_ARRIVAL FROM FLIGHTS WHERE airlines_name = '{}' and DEPARTURE = '{}' and DESTINATION = '{}' ".format (fli[0], deplo[0], arrlo[0])
    my_cursor.execute(query6)
    for h in my_cursor:
        tarr.append(h)

an = []
de = []
ds = []
td = []
ta = []

def fl_no():
    query7 = "SELECT AIRLINES_NAME FROM FLIGHTS WHERE FLIGHT_NO = '{}'".format(num)
    my_cursor.execute(query7)
    for i in my_cursor:
        an.append(i)

    query8 = "SELECT DEPARTURE FROM FLIGHTS WHERE FLIGHT_NO = '{}'".format(num)
    my_cursor.execute(query8)
    for j in my_cursor:
        de.append(j)

    query9 = "SELECT DESTINATION FROM FLIGHTS WHERE FLIGHT_NO = '{}'".format(num)
    my_cursor.execute(query9)
    for k in my_cursor:
        ds.append(k) 

    query10 = "SELECT TIME_OF_DEPARTURE FROM FLIGHTS WHERE FLIGHT_NO = '{}'".format(num)
    my_cursor.execute(query10)
    for l in my_cursor:
        td.append(l)

    query11 = "SELECT TIME_OF_ARRIVAL FROM FLIGHTS WHERE FLIGHT_NO = '{}'".format(num)
    my_cursor.execute(query11)
    for m in my_cursor:
        ta.append(m)

cl = int(input("\nENTER CLASS NO (1/2/3):-"))

payment = []

if ans==1 and cl==1:
    fl_no()
    query12 = "SELECT CHARGES*{} FROM FLIGHTS WHERE FLIGHT_NO = '{}'".format(passenger, num)
    print(f"\nnames = {nam}               age = {ag}           gender = {gen}")
    print(f"flight name = {an}         departure = {de}       destination = {ds}")
    print(f"flight number = {num}      diparture time = {td}        arrival time = {ta}     ")
    print("class = economy class")
    for n in my_cursor:
        payment.append(n)
        print(f"\nYOU HAVE TO PAY {n} TOMANS")

elif ans==1 and cl==2:
    fl_no()
    query13 = "SELECT (CHARGES +CHARGES*0.2)*{} FROM FLIGHTS WHERE flight_no = '{}' ".format (passenger, num)
    my_cursor.execute(query13)
    print(f"\nnames = {nam}               age = {ag}           gender = {gen}")
    print(f"flight name = {an}         departure = {de}       destination = {ds}")
    print(f"flight number = {num}      diparture time = {td}        arrival time = {ta}     ")
    print("class = business class")
    for o in my_cursor:
        payment.append(o)
        print(f"\nYOU HAVE TO PAY {o} TOMANS") 

elif ans==1 and cl==3:
    fl_no()
    query14 = "SELECT (CHARGES +CHARGES*0.4)*{} FROM FLIGHTS WHERE FLIGHT_NO = '{}'".format (passenger, num)
    my_cursor.execute(query14)
    print(f"\nnames = {nam}               age = {ag}           gender = {gen}")
    print(f"flight name = {an}         departure = {de}       destination = {ds}")
    print(f"flight number = {num}      diparture time = {td}        arrival time = {ta}     ")
    print("class = first class")
    for p in my_cursor:
        payment.append(p)
        print(f"\nYOU HAVE TO PAY {p} TOMANS")


elif ans==2 and cl==1:
    fl_nm()
    query15 = "SELECT CHARGES*{} FROM FLIGHTS WHERE airlines_name = '{}' and DEPARTURE = '{}' and DESTINATION = '{}' ".format (passenger, fli[0], deplo[0], arrlo[0])
    my_cursor.execute(query15)
    print(f"\nnames = {nam}               age = {ag}           gender = {gen}")
    print(f"flight name = {fli}         departure = {deplo}       destination = {arrlo}")
    print(f"flight number = {flo}      diparture time = {tdep}        arrival time = {tarr}     ")
    print("class = economy class")
    for q in my_cursor:
        payment.append(q)
        print(f"\nYOU HAVE TO PAY {q} TOMANS") 

elif  ans==2 and cl==2:
    fl_nm()
    query16 = "SELECT (CHARGES +CHARGES*0.2)*{} FROM FLIGHTS WHERE airlines_name = '{}' and DEPARTURE = '{}' and DESTINATION = '{}' ".format (passenger, fli[0], deplo[0], arrlo[0])
    my_cursor.execute(query16)
    print(f"\nnames = {nam}               age = {ag}           gender = {gen}")
    print(f"flight name = {fli}         departure = {deplo}       destinatio = {arrlo}")
    print(f"flight number = {flo}      diparture time = {tdep}        arrival time = {tarr}     ")
    print("class = business class")
    for r in my_cursor:
        payment.append(r)
        print(f"\nYOU HAVE TO PAY {r} TOMANS")  

elif ans==2 and cl==3:
    fl_nm()
    query17 = "SELECT (CHARGES +CHARGES*0.4)*{} FROM FLIGHTS WHERE airlines_name = '{}' and DEPARTURE = '{}' and DESTINATION = '{}' ".format (passenger, fli[0], deplo[0], arrlo[0])
    my_cursor.execute(query17)
    print(f"\nnames = {nam}               age = {ag}           gender = {gen}")
    print(f"flight name = {fli}         departure = {deplo}       destination = {arrlo}")
    print(f"flight number = {flo}      diparture time = {tdep}        arrival time = {tarr}     ")
    print("class = first class")
    for s in my_cursor:
        payment.append(s)
        print(f"\nYOU HAVE TO PAY {s} TOMANS")

pay = input("\nTO PAY PRESS (P):-")

if pay=='p' or pay=='P':
    print("\nHOW YOU WANT TO PAY ?")
    print("1.GOOGLE PAY")
    print("2.AMAZON PAY")
    print("3.PAYPAL")
    print("4.APPLE PAY")
    print("5.CREDIT CARD")
    print("6.DEBIT CARD")
    
    

pay2 = int(input("\nENTER YOUR PAYMENT METHOD (1/2/3/4........):-"))

if pay2==1:
    print("\n-------------------GOOGLE PAY---------------------------")
    print(F"PAY {payment[0]} TOMANS")
    pay3 = input("\nTO CONTINUE PAYMENT PRESS (P):-")
    ott = int(input("\nENTER A OTP SENT TO YOUR PHONE NO AND EMAIL:-"))
    print("\nTRANSACTION SUCCESSFUL------------")
    print("\n**********THANK YOU***********")

if pay2==2:
    print("\n-------------------AMAZON PAY---------------------------")
    print(F"PAY {payment[0]} TOMANS")
    pay3 = input("\nTO CONTINUE PAYMENT PRESS (P):-")
    ott = int(input("\nENTER A OTP SENT TO YOUR PHONE NO AND EMAIL:-"))
    print("\nTRANSACTION SUCCESSFUL------------")
    print("\n**********THANK YOU***********")
    
if pay2==3:
    print("\n-------------------PAYPAL---------------------------")
    print(F"PAY {payment[0]} TOMANS")
    pay3 = input("\nTO CONTINUE PAYMENT PRESS (P):-")
    ott = int(input("\nENTER A OTP SENT TO YOUR PHONE NO AND EMAIL:-"))
    print("\nTRANSACTION SUCCESSFUL------------")
    print("**********THANK YOU***********")

if pay2==4:
    print("\n-------------------APPLE PAY---------------------------")
    print(F"PAY {payment[0]} TOMANS")
    pay3 = input("\nTO CONTINUE PAYMENT PRESS (P):-")
    ott = int(input("\nENTER A OTP SENT TO YOUR PHONE NO AND EMAIL:-"))
    print("\nTRANSACTION SUCCESSFUL------------")
    print("**********THANK YOU***********")

if pay2==5 or pay2==6:
    print("\n-------------------CARD payment---------------------------")
    print(F"PAY {payment[0]} TOMANS")
    c_no = int(input("\nENTER YOUR CARD NO:-"))
    cvv = int(input("\nENTER YOUR CVV:-"))
    ott2 = int(input("\nENTER A OTP SEND TO YOUR NUMBER:-"))
    print("\nTRANSACTION SUCCESSFUL------------")
    print("**********THANK YOU***********")

print("\n--------THANKS FOR USING FLIGHT BOOKING SYSTEM--------------")
print(f"\nYOUR TICKETS ARE SEND TO YOUR EMAIL {e[0]} ")
print("\nSEE YOU LATER :)")

conn.close()

# CODED BY AMIRHOSEIN DEZHABDOLLAHI