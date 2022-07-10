import tkinter as tk
import tkinter.font as tkFont
import time
import os
from ftplib import FTP
from datetime import datetime
from tkinter import messagebox
import shutil

root = tk.Tk()
#ftp = FTP(ftp_server)
try:
   ftpReader = open("FTPConnect.txt")
   for line in ftpReader:
              ftp_server, ftp_user, ftp_password = line.split(';')
   ftp_server = str(ftp_server)
   ftp_user = str(ftp_user)
   ftp_password = str(ftp_password)
   ftpReader.close()
except:
   print("No Ftp Login Infomation file")
   
try:
   ftp = FTP(ftp_server)
   ftp.login(user = ftp_user, passwd = ftp_password)
except:
   print("Can't connect to FTP server")
   
root.title("KFC Restaurant")
width=1200
height=700
screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()
alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
root.geometry(alignstr)
root.resizable(width=False, height=False)
        
root.configure(background='#ff6d6f')

#FUNCTION---------------------------------------------------------------------------------------------
item=[]
itemprice=[]

try:
    menuList = open("Menu.txt",'r',encoding="utf-8")
except IOError:
    print("Can not find file")
else:
    for line in menuList:
        foodItem, priceMenu = line.split()
        item.append(foodItem)
        itemprice.append(priceMenu)
    menuList.close()

def downloadFile(destination):
    path, filename = destination.split('/')
    ftp.cwd("/..")
    ftp.cwd(path)
    os.chdir(path)
    localfile = open(filename, 'wb')
    ftp.retrbinary('RETR ' + filename, localfile.write, 1024)
    localfile.close()
    ftp.cwd("/..")
    os.chdir("..")
   

def uploadFile(destination):
    #ทำการแปลง UTF-8 เพื่อให้สามารถรับภาษาไทยได้
    ftp.encoding = 'utf-8'
    try:
        #ทำการเปิดไฟล์ใน Path ที่กำหนดแล้ว Upload ไฟล์นั้นใน Server FTP
        path, filename = destination.split('/')
        ftp.cwd("/..")
        ftp.cwd(path)
        ftp.storbinary('STOR '+ filename, open(destination , 'rb'))
        ftp.cwd("/..")
    except:
         print("Can't find the File Directory or It's not exist")
    
#ฟังก์ชันสำหรับรับค่าการกดปุ่มเมนู
def btnClick(number, price):
    global text_Input
    global operator
    p_menu.append(price)

    if number == "setno.1":
        p1.append(number)
    if number == "frenchfries":
        p2.append(number)
    if number == "tunacornsalad":
        p3.append(number)
    if number == "eggtart":
        p4.append(number)
    if number == "setno.2":
        p5.append(number)
    if number == "bonelesschicken":
        p6.append(number)
    if number == "mashedpotatoes":
        p7.append(number)
    if number == "vanillaicecream":
        p8.append(number)
    if number == "setno.3":
        p9.append(number)
    if number == "shrimpdonuts":
        p10.append(number)
    if number == "coleslaw":
        p11.append(number)
    if number == "cocoamalt":
        p12.append(number)
        
    #ทำการรีเซ็ตการแสดงผลเพื่ออัพเดต ข้อมูลสินค้าทุกครั้ง
    txtReceipt.delete("1.0", tk.END)
    txtReceipt.insert(tk.END, "\n==============MENU LIST=============== \n\n")
    txtReceipt.insert(tk.END, "       set no.1           " + str(len(p1)) + "\n")
    txtReceipt.insert(tk.END, "       set no.2           " + str(len(p5)) + "\n")
    txtReceipt.insert(tk.END, "       set no.3           " + str(len(p9)) + "\n")
    txtReceipt.insert(tk.END, "       french fries       " + str(len(p2)) + "\n")
    txtReceipt.insert(tk.END, "       boneless chicken   " + str(len(p6)) + "\n")
    txtReceipt.insert(tk.END, "       shrimp donuts      " + str(len(p10)) + "\n")
    txtReceipt.insert(tk.END, "       tuna corn salad    " + str(len(p3)) + "\n")
    txtReceipt.insert(tk.END, "       mashed potatoes    " + str(len(p7)) + "\n")
    txtReceipt.insert(tk.END, "       coleslaw           " + str(len(p11)) + "\n")
    txtReceipt.insert(tk.END, "       egg tart           " + str(len(p4)) + "\n")
    txtReceipt.insert(tk.END, "       vanilla ice cream  " + str(len(p8)) + "\n")
    txtReceipt.insert(tk.END, "       cocoa malt         " + str(len(p12)) + "\n")


totalprice = 0
vatprice = 0
change = 0
tcost = 0

setZero=[]  #count
p_menu=[]   #price
p1=[]       #set no.1
p2=[]       #french fries
p3=[]       #tuna corn salad
p4=[]       #egg tart 
p5=[]       #set no.2
p6=[]       #boneless chicken
p7=[]       #mashed potatoes
p8=[]       #vanilla ice cream
p9=[]       #set no.3
p10=[]      #shrimp donuts
p11=[]      #coleslaw
p12=[]      #cocoa malt

#ฟังก์ชันสำหรับรวบรวมผลข้อมูล
def CalculateTotal():
    txtReceipt.delete("1.0", tk.END)
    global totalprice, vatprice, change, tcost
    totalprice = 0
    vatprice = 0
    change = 0
    tcost = 0
    money = input6.get()
    #คำนวนค่าอาหารรวม และ ค่าภาษี
    for i in p_menu:
        totalprice = totalprice + int(i)
        vatprice = totalprice * float(itemprice[12]) / 100

    #รับค่าสำหรับคำนวน เงินที่ลูกค่าจ่ายมา เพื่อหาค่าเงินทอน
    input3.set(str(totalprice) + " bath ")
    cost = str('%.2f' % vatprice + " bath ")
    tcost = str(float(totalprice) + float("%.2f" % vatprice)) + " bath "
    input5.set(tcost)
    input4.set(cost)
    #กรณีลืมใส่ค่าในช่อง
    try:
        totalVat = float(totalprice) + float("%.2f" % vatprice)
        if int(money) >= totalVat:
            change = int(money) - totalVat
            input7.set(str("%.2f" % change) + " bath ")
    except ValueError:
        input6.set("Enter numbers only")
        input7.set("No change")
    else:
        if int(money) < totalVat:
            input6.set("not enough amount")
    #แสดงว่าเราสั่งอะไรไปบ้าง
    txtReceipt.insert(tk.END, "\n==============MENU LIST=============== \n\n")
    txtReceipt.insert(tk.END, "       set no.1           " + str(len(p1)) + "\n")
    txtReceipt.insert(tk.END, "       set no.2           " + str(len(p5)) + "\n")
    txtReceipt.insert(tk.END, "       set no.3           " + str(len(p9)) + "\n")
    txtReceipt.insert(tk.END, "       french fries       " + str(len(p2)) + "\n")
    txtReceipt.insert(tk.END, "       boneless chicken   " + str(len(p6)) + "\n")
    txtReceipt.insert(tk.END, "       shrimp donuts      " + str(len(p10)) + "\n")
    txtReceipt.insert(tk.END, "       tuna corn salad    " + str(len(p3)) + "\n")
    txtReceipt.insert(tk.END, "       mashed potatoes    " + str(len(p7)) + "\n")
    txtReceipt.insert(tk.END, "       coleslaw           " + str(len(p11)) + "\n")
    txtReceipt.insert(tk.END, "       egg tart           " + str(len(p4)) + "\n")
    txtReceipt.insert(tk.END, "       vanilla ice cream  " + str(len(p8)) + "\n")
    txtReceipt.insert(tk.END, "       cocoa malt         " + str(len(p12)) + "\n")


global totalList

def uploadFTP():
    global totalprice
    ftp.encoding = 'utf-8'
    priceTotal = str(float(totalprice) + float(vatprice)) # ราคารวม
    fileNumber = 1
    uploadLicense = "FromShop/" + str(input1.get()) + " (" + str(fileNumber) +")" + ".txt"
    #ทำการตรวจสอบจำนวนไฟล์ว่า ใน FTP ตอนนี้ ทะเบียนที่เรากำลังจะกรอกลงไป อยู่ลำดับที่เท่าไหร่
    numberOfFile = 1
    fileName = str(input1.get()) + " (" + str(numberOfFile) + ").txt"
    ftp.cwd("FromParking")
    if not fileName in ftp.nlst():
            fileName =  str(input1.get()) + " (" + str(numberOfFile) + ").txt"
            print(fileName)
    else:
        
        while(True):
            if fileName in ftp.nlst():
                numberOfFile += 1
                fileName =  str(input1.get()) + " (" + str(numberOfFile) + ").txt"
                print(fileName)
            else :
                print(fileName)
                numberOfFile -= 1
                fileName =  str(input1.get()) + " (" + str(numberOfFile) + ").txt"
                print("Done")
                break
    
    ftp.cwd("/..")
    #ทำการกรอกข้อมูลที่ต้องใช้ คือราคาของลูกค้าที่สั่งไป ลงในโฟลเดอร์เพื่อเตรียมอัพโหลด
    uploadLicense = "FromShop/" + fileName
    entryUpload = open(uploadLicense, mode = "w", encoding = "utf-8")
    entryUpload.write(str(input1.get()) + " " + priceTotal)
    entryUpload.close()
    fileNumber = 1
    #อัพโหลดไฟล์สำหรับนำไปใช้กับฝั่งของเครื่องจอดรถ
    uploadFile(uploadLicense)
    print("Finish Create, Please Enjoy")
    
    
#ฟังก์ชันสำหรับรีเซ็ตค่าทั้งหมด
def Reset():
    global totalprice,vatprice,change,tcost,p1,p2,p3,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12,txtReceipt

    input1.set("")
    input3.set("")
    input4.set("")
    input5.set("")
    input6.set("")
    input7.set("")

    setZero.clear()
    p_menu.clear()
    totalprice = 0
    vatprice = 0
    change = 0
    tcost = 0

    txtReceipt.delete("1.0", tk.END)

    p1.clear()   #set no.1
    p2.clear()   #french fries
    p3.clear()   #tuna corn salad
    p4.clear()   #egg tart 
    p5.clear()   #set no.2
    p6.clear()   #boneless chicken
    p7.clear()   #mashed potatoes
    p8.clear()   #vanilla ice cream
    p9.clear()   #set no.3
    p10.clear()  #shrimp donuts
    p11.clear()  #coleslaw
    p12.clear()  #cocoa malt

def qExit():
    root.destroy()
#ฟังก์ชันสำหรับ Validate Directory ว่าโฟลเดอร์นั้นว่างหรือมีอยู่หรือไม่ 
def ResetData():
    try:
      shutil.rmtree("FromShop")
    except:
      os.mkdir("FromShop")
    else:
      os.mkdir("FromShop")
    

photo1 = tk.PhotoImage(file = r"Menu1.png")
GButton_762=tk.Button(root,image = photo1,command = lambda:btnClick(item[0], (itemprice[0]))).place(x=540,y=10,width=160,height=130)
GLabel_762=tk.Label(root)
ft = tkFont.Font(family='Times',size=10)
GLabel_762["font"] = ft
GLabel_762["fg"] = "#333333"
GLabel_762["bg"] = "#ff6d6f"
GLabel_762["justify"] = "center"
GLabel_762["text"] = "Set no.1"
GLabel_762.place(x=540,y=145,width=160,height=25)


photo2 = tk.PhotoImage(file = r"Menu5.png")
GButton_835=tk.Button(root,image = photo2,command = lambda:btnClick(item[1], (itemprice[1]))).place(x=540,y=180,width=160,height=130)
GLabel_835=tk.Label(root)
ft = tkFont.Font(family='Times',size=10)
GLabel_835["font"] = ft
GLabel_835["fg"] = "#333333"
GLabel_835["bg"] = "#ff6d6f"
GLabel_835["justify"] = "center"
GLabel_835["text"] = "french fries"
GLabel_835.place(x=540,y=315,width=160,height=25)


photo3 = tk.PhotoImage(file = r"Menu6.png")
GButton_404=tk.Button(root,image = photo3,command = lambda:btnClick(item[2], (itemprice[2]))).place(x=540,y=350,width=160,height=130)
GLabel_404=tk.Label(root)
ft = tkFont.Font(family='Times',size=10)
GLabel_404["font"] = ft
GLabel_404["fg"] = "#333333"
GLabel_404["bg"] = "#ff6d6f"
GLabel_404["justify"] = "center"
GLabel_404["text"] = "tuna corn salad"
GLabel_404.place(x=540,y=485,width=160,height=25)


photo4 = tk.PhotoImage(file = r"Menu9.png")
GButton_134=tk.Button(root,image = photo4,command = lambda:btnClick(item[3], (itemprice[3]))).place(x=540,y=520,width=160,height=130)
GLabel_134=tk.Label(root)
ft = tkFont.Font(family='Times',size=10)
GLabel_134["font"] = ft
GLabel_134["fg"] = "#333333"
GLabel_134["bg"] = "#ff6d6f"
GLabel_134["justify"] = "center"
GLabel_134["text"] = "egg tart"
GLabel_134.place(x=540,y=655,width=160,height=25)


photo5 = tk.PhotoImage(file = r"Menu2.png")
GButton_587=tk.Button(root,image = photo5,command = lambda:btnClick(item[4], (itemprice[4]))).place(x=770,y=10,width=160,height=130)
GLabel_587=tk.Label(root)
ft = tkFont.Font(family='Times',size=10)
GLabel_587["font"] = ft
GLabel_587["fg"] = "#333333"
GLabel_587["bg"] = "#ff6d6f"
GLabel_587["justify"] = "center"
GLabel_587["text"] = "Set no.2"
GLabel_587.place(x=770,y=145,width=160,height=25)


photo6 = tk.PhotoImage(file = r"Menu4.png")
GButton_755=tk.Button(root,image = photo6,command = lambda:btnClick(item[5], (itemprice[5]))).place(x=770,y=180,width=160,height=130)
GLabel_835=tk.Label(root)
ft = tkFont.Font(family='Times',size=10)
GLabel_835["font"] = ft
GLabel_835["fg"] = "#333333"
GLabel_835["bg"] = "#ff6d6f"
GLabel_835["justify"] = "center"
GLabel_835["text"] = "boneless chicken"
GLabel_835.place(x=770,y=315,width=160,height=25)


photo7 = tk.PhotoImage(file = r"Menu7.png")
GButton_995=tk.Button(root,image = photo7,command = lambda:btnClick(item[6], (itemprice[6]))).place(x=770,y=350,width=160,height=130)
GLabel_995=tk.Label(root)
ft = tkFont.Font(family='Times',size=10)
GLabel_995["font"] = ft
GLabel_995["fg"] = "#333333"
GLabel_995["bg"] = "#ff6d6f"
GLabel_995["justify"] = "center"
GLabel_995["text"] = "mashed potatoes"
GLabel_995.place(x=770,y=485,width=160,height=25)


photo8 = tk.PhotoImage(file = r"Menu12.png")
GButton_266=tk.Button(root,image = photo8,command = lambda:btnClick(item[7], (itemprice[7]))).place(x=770,y=520,width=160,height=130)
GLabel_266=tk.Label(root)
ft = tkFont.Font(family='Times',size=10)
GLabel_266["font"] = ft
GLabel_266["fg"] = "#333333"
GLabel_266["bg"] = "#ff6d6f"
GLabel_266["justify"] = "center"
GLabel_266["text"] = "vanilla ice cream"
GLabel_266.place(x=770,y=655,width=160,height=25)        


photo9 = tk.PhotoImage(file = r"Menu3.png")
GButton_187=tk.Button(root,image = photo9,command = lambda:btnClick(item[8], (itemprice[8]))).place(x=1000,y=10,width=160,height=130)
GLabel_187=tk.Label(root)
ft = tkFont.Font(family='Times',size=10)
GLabel_187["font"] = ft
GLabel_187["fg"] = "#333333"
GLabel_187["bg"] = "#ff6d6f"
GLabel_187["justify"] = "center"
GLabel_187["text"] = "Set no.3"
GLabel_187.place(x=1000,y=145,width=160,height=25)


photo10 = tk.PhotoImage(file = r"Menu10.png")
GButton_571=tk.Button(root,image = photo10,command = lambda:btnClick(item[9], (itemprice[9]))).place(x=1000,y=180,width=160,height=130)
GLabel_835=tk.Label(root)
ft = tkFont.Font(family='Times',size=10)
GLabel_835["font"] = ft
GLabel_835["fg"] = "#333333"
GLabel_835["bg"] = "#ff6d6f"
GLabel_835["justify"] = "center"
GLabel_835["text"] = "shrimp donuts"
GLabel_835.place(x=1000,y=315,width=160,height=25)


photo11 = tk.PhotoImage(file = r"Menu8.png")
GButton_311=tk.Button(root,image = photo11,command = lambda:btnClick(item[10], (itemprice[10]))).place(x=1000,y=350,width=160,height=130)
GLabel_311=tk.Label(root)
ft = tkFont.Font(family='Times',size=10)
GLabel_311["font"] = ft
GLabel_311["fg"] = "#333333"
GLabel_311["bg"] = "#ff6d6f"
GLabel_311["justify"] = "center"
GLabel_311["text"] = "coleslaw"
GLabel_311.place(x=1000,y=485,width=160,height=25)


photo12 = tk.PhotoImage(file = r"Menu11.png")
GButton_650=tk.Button(root,image = photo12,command = lambda:btnClick(item[11], (itemprice[11]))).place(x=1000,y=520,width=160,height=130)
GLabel_650=tk.Label(root)
ft = tkFont.Font(family='Times',size=10)
GLabel_650["font"] = ft
GLabel_650["fg"] = "#333333"
GLabel_650["bg"] = "#ff6d6f"
GLabel_650["justify"] = "center"
GLabel_650["text"] = "cocoa malt"
GLabel_650.place(x=1000,y=655,width=160,height=25)
        

GLabel_name=tk.Label(root)
ft = tkFont.Font(family='Times',size=25)
GLabel_name["font"] = ft
GLabel_name["fg"] = "#000000"
GLabel_name["bg"] = "#bf4143"
GLabel_name["justify"] = "center"
GLabel_name["text"] = " ——————— KFC Menu ——————— "
GLabel_name.place(x=30,y=30,width=425,height=40)
        
GLabel_time = tk.Label(root)
ft = tkFont.Font(family='Times',size=15)
GLabel_time["font"] = ft
GLabel_time["fg"] = "#000000"
GLabel_time["bg"] = "#bf4143"
GLabel_time["justify"] = "center"
GLabel_time.place(x=30,y=70,width=425,height=30)

def clock():
    curtime = datetime.now()
    ftime = curtime.strftime('%a %d %b %Y %H:%M:%S %p')
    GLabel_time.config(text=ftime)
    GLabel_time.after(1000, clock)
clock()

GLabel_439=tk.Label(root)
ft = tkFont.Font(family='Times',size=10)
GLabel_439["font"] = ft
GLabel_439["fg"] = "#333333"
GLabel_439["justify"] = "center"
GLabel_439["text"] = "car registration : "
GLabel_439.place(x=30,y=110,width=100,height=30)
        
input1 = tk.StringVar()
GLineEdit_816=tk.Entry(root)
GLineEdit_816["borderwidth"] = "1px"
ft = tkFont.Font(family='Times',size=10)
GLineEdit_816["font"] = ft
GLineEdit_816["fg"] = "#333333"
GLineEdit_816["justify"] = "center"
GLineEdit_816["text"] = "Entry"
GLineEdit_816["textvariable"] = input1
GLineEdit_816.place(x=140,y=110,width=315,height=30)
        


GLabel_95=tk.Label(root)
ft = tkFont.Font(family='Times',size=10)
GLabel_95["font"] = ft
GLabel_95["fg"] = "#333333"
GLabel_95["justify"] = "center"
GLabel_95["text"] = "food list : "
GLabel_95.place(x=30,y=150,width=100,height=30)

txtReceipt = tk.Text(root)
txtReceipt.place(x=140,y=150,width=315,height=275)


GLabel_367=tk.Label(root)
ft = tkFont.Font(family='Times',size=10)
GLabel_367["font"] = ft
GLabel_367["fg"] = "#333333"
GLabel_367["justify"] = "center"
GLabel_367["text"] = "price : "
GLabel_367.place(x=30,y=440,width=100,height=30)
        
input3 = tk.StringVar()
GLineEdit_36=tk.Entry(root)
GLineEdit_36["borderwidth"] = "1px"
ft = tkFont.Font(family='Times',size=10)
GLineEdit_36["font"] = ft
GLineEdit_36["fg"] = "#333333"
GLineEdit_36["justify"] = "center"
GLineEdit_36["text"] = "Entry"
GLineEdit_36["textvariable"] = input3
GLineEdit_36.place(x=140,y=440,width=115,height=30)
        
        
        
GLabel_23=tk.Label(root)
ft = tkFont.Font(family='Times',size=10)
GLabel_23["font"] = ft
GLabel_23["fg"] = "#333333"
GLabel_23["justify"] = "center"
GLabel_23["text"] = "tax : "
GLabel_23.place(x=265,y=440,width=70,height=30)
        
input4 = tk.StringVar()
GLineEdit_7=tk.Entry(root)
GLineEdit_7["borderwidth"] = "1px"
ft = tkFont.Font(family='Times',size=10)
GLineEdit_7["font"] = ft
GLineEdit_7["fg"] = "#333333"
GLineEdit_7["justify"] = "center"
GLineEdit_7["text"] = "Entry"
GLineEdit_7["textvariable"] = input4
GLineEdit_7.place(x=340,y=440,width=115,height=30)



GLabel_439=tk.Label(root)
ft = tkFont.Font(family='Times',size=10)
GLabel_439["font"] = ft
GLabel_439["fg"] = "#333333"
GLabel_439["justify"] = "center"
GLabel_439["text"] = "total : "
GLabel_439.place(x=30,y=480,width=100,height=30)
        
input5 = tk.StringVar()
GLineEdit_599=tk.Entry(root)
GLineEdit_599["borderwidth"] = "1px"
ft = tkFont.Font(family='Times',size=10)
GLineEdit_599["font"] = ft
GLineEdit_599["fg"] = "#333333"
GLineEdit_599["justify"] = "center"
GLineEdit_599["text"] = "Entry"
GLineEdit_599["textvariable"] = input5
GLineEdit_599.place(x=140,y=480,width=315,height=30)
        


GLabel_503=tk.Label(root)
ft = tkFont.Font(family='Times',size=10)
GLabel_503["font"] = ft
GLabel_503["fg"] = "#333333"
GLabel_503["justify"] = "center"
GLabel_503["text"] = "cash : "
GLabel_503.place(x=30,y=520,width=100,height=30)
        
input6 = tk.StringVar()
GLineEdit_151=tk.Entry(root)
GLineEdit_151["borderwidth"] = "1px"
ft = tkFont.Font(family='Times',size=10)
GLineEdit_151["font"] = ft
GLineEdit_151["fg"] = "#333333"
GLineEdit_151["justify"] = "center"
GLineEdit_151["text"] = "Entry"
GLineEdit_151["textvariable"] = input6
GLineEdit_151.place(x=140,y=520,width=315,height=30)
        


GLabel_705=tk.Label(root)
ft = tkFont.Font(family='Times',size=10)
GLabel_705["font"] = ft
GLabel_705["fg"] = "#333333"
GLabel_705["justify"] = "center"
GLabel_705["text"] = "change : "
GLabel_705.place(x=30,y=560,width=100,height=30)
        
input7 = tk.StringVar()
GLineEdit_431=tk.Entry(root)
GLineEdit_431["borderwidth"] = "1px"   
ft = tkFont.Font(family='Times',size=10)
GLineEdit_431["font"] = ft
GLineEdit_431["fg"] = "#333333"
GLineEdit_431["justify"] = "center"
GLineEdit_431["text"] = "Entry"
GLineEdit_431["textvariable"] = input7
GLineEdit_431.place(x=140,y=560,width=315,height=30)
        
#Button------------------------------------------------------------------------------------------------
GButton_1=tk.Button(root,command = lambda :Reset())
GButton_1["bg"] = "#efefef"
ft = tkFont.Font(family='Times',size=12)
GButton_1["font"] = ft
GButton_1["fg"] = "#000000"
GButton_1["bg"] = "#bf4143"
GButton_1["justify"] = "center"
GButton_1["text"] = "Reset"
GButton_1.place(x=30,y=605,width=125,height=40)


GButton_2=tk.Button(root,command= lambda:CalculateTotal())
GButton_2["bg"] = "#efefef"
ft = tkFont.Font(family='Times',size=12)
GButton_2["font"] = ft
GButton_2["fg"] = "#000000"
GButton_2["bg"] = "#bf4143"
GButton_2["justify"] = "center"
GButton_2["text"] = "Total"
GButton_2.place(x=180,y=605,width=125,height=40)


GButton_3=tk.Button(root,command = lambda:uploadFTP())
GButton_3["bg"] = "#efefef"
ft = tkFont.Font(family='Times',size=12)
GButton_3["font"] = ft
GButton_3["fg"] = "#000000"
GButton_3["bg"] = "#bf4143"
GButton_3["justify"] = "center"
GButton_3["text"] = "Submit"
GButton_3.place(x=330,y=605,width=125,height=40)


GButton_4=tk.Button(root,command = lambda:qExit())
GButton_4["bg"] = "#efefef"
ft = tkFont.Font(family='Times',size=12)
GButton_4["font"] = ft
GButton_4["fg"] = "#000000"
GButton_4["bg"] = "#bf4143"
GButton_4["justify"] = "center"
GButton_4["text"] = "Exit"
GButton_4.place(x=30,y=655,width=125,height=40)

GButton_5=tk.Button(root,command = lambda:ResetData())
GButton_5["bg"] = "#efefef"
ft = tkFont.Font(family='Times',size=12)
GButton_5["font"] = ft
GButton_5["fg"] = "#000000"
GButton_5["bg"] = "#bf4143"
GButton_5["justify"] = "center"
GButton_5["text"] = "ResetData"
GButton_5.place(x=180,y=655,width=125,height=40)


     
root.mainloop()
