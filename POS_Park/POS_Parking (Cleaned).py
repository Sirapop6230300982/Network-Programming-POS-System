from tkinter import *
import os
import random
import time
from datetime import datetime,date,timedelta

from ftplib import FTP
from smtplib import *
from tkinter import messagebox

from getpass import getpass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import tkinter
import shutil
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

#ทำการเชื่อมต่อ FTP Server
try:
   ftp = FTP(ftp_server)
   ftp.login(user = ftp_user, passwd = ftp_password)
except:
   print("Can't connect to FTP server")

def downloadFile(destination):
    path, filename = destination.split('/')
    ftp.cwd("/..")
    try:
       ftp.cwd(path)
       os.chdir(path)
       localfile = open(filename, 'wb')
       ftp.retrbinary('RETR ' + filename, localfile.write, 1024)
       localfile.close()
       ftp.cwd("/..")
       os.chdir("..")
    except:
       print("Can't find the File Directory or It's not exist")
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

def EnterOperation():
    confirmEnter = tkinter.messagebox.askquestion("AddData","คุณต้องการเพิ่มข้อมูลในโปรแกรมหรือไม่ ?")
    if confirmEnter == "yes":
       carLicense = txtReference.get()
       carLicense = str(carLicense)
       if carLicense != '':
          fileNumber = 1
          #ทำการระบุค่าว่าเป็นเวล่าเท่าใด ในรูปแบบของ Day/Month/Year xx:xx:xx
          currentTime = datetime.today()
          currentTimeFormat = currentTime.strftime("%d/%m/%Y %H:%M:%S")
          uploadLicense = "FromParking/" + str(carLicense) + " (" + str(fileNumber) +")" + ".txt"
          #ในส่วน While จะเป็นส่วนที่ทำการนับจำนวนไฟล์ว่า ใน Directory เป้าหมายมีไฟล์ชื่อ xxx กี่ไฟล์เพื่อทำการระบุลำดับของไฟล์
          while(os.path.isfile(uploadLicense) == True):
              fileNumber += 1
              uploadLicense = "FromParking/" + str(carLicense) + " (" + str(fileNumber) +")" + ".txt"
          #ใช้เป็นโหมด W เพื่อทำการเริ่มต้นไฟล์ใหม่ทุกครั้ง
          entryUpload = open(uploadLicense, mode = "w+", encoding = "utf-8")
          entryUpload.write(str(currentTimeFormat) + " " + str(carLicense))
          entryUpload.close()
          fileNumber = 1
          uploadFile(uploadLicense)
          #เมื่อทำคำสั่งเสร็จจะทำการ print ข้อความเพื่อบ่งบอกถึงความสำเร็จของปฏิบัติการทั้งฝั่ง Terminal และ TK Inter
          print("Finish Create, Please Enjoy")
          message = currentTime.strftime("%H:%M:%S") +"   "+ carLicense
          txtTotal = Label(fTotal, text=message,font = ('Agency FB',20,'bold'), bd = 4, width = 45, height = 2, bg = "white")
          txtTotal.grid(row = 1, column = 0)
       else:
            tkinter.messagebox.showinfo("แจ้งเตือน !!!","ข้อมูลว่างเปล่ากรุณาเติมข้อมูล !!!")
            txtTotal = Label(fTotal,font = ('Agency FB',20,'bold'), bd = 4, width = 45, height = 2, bg = "white")
            txtTotal.grid(row = 1, column = 0)  
    

def ExitOperation():
    confirmExit = tkinter.messagebox.askquestion("ExitData","คุณต้องการระบุรถออกในโปรแกรมหรือไม่ ?")
    if confirmExit == "yes":
       carLicense = txtReference.get()
       carLicense = str(carLicense)
       if carLicense != '':
          fileNumber = 1
          #ทำการระบุค่าว่าเป็นเวล่าเท่าใด ในรูปแบบของ Day/Month/Year xx:xx:xx
          currentTime = datetime.today()
          currentTimeFormat = currentTime.strftime("%d/%m/%Y %H:%M:%S")
          currentTimeFormatOnlyTime = currentTime.strftime("%H:%M:%S")
          #กำหนดตัวแปรสำหรับเป็นค่าเริ่มต้น ลำดับไฟล์ โดยเริ่มทั้งไฟล์ของ ฝั่งเครื่องคิวรับบัตรจอดรถ และ ฝั่งเครื่องคิดเงินในร้านค้า โดยเริ่มต้นที่ลำดับไฟล์ ที่ 1
          downloadLicense = "FromParking/" + str(carLicense) + " (" + str(fileNumber) +")" + ".txt"
          downloadShop = "FromShop/" + str(carLicense) + " (" + str(fileNumber) +")" + ".txt"
          justForConditionCheck = "FromParking/" + str(carLicense) + " (" + str(fileNumber+1) +")" + ".txt"
          #เงื่อนไขแรก ตรวจสอบว่าเคยมีไฟล์ลำดับที่ 1 หรือไม่ถ้าไม่เคย ก็ใช้ลำดับที่ 1 เป็นตัวในการทำกระบวนการต่อไป
          if(os.path.isfile(downloadLicense) == False ):
              fileNumber = 1
              downloadLicense = "FromParking/" + str(carLicense) + " (" + str(fileNumber) +")" + ".txt"
              downloadShop = "FromShop/" + str(carLicense) + " (" + str(fileNumber) +")" + ".txt"
          #หากตรวจพบว่ามีไฟล์ลำดับที่ 1 อยู่แล้ว ก็จะทำการเรียงลำดับของไฟล์ต่อไป เพื่อไปสู่ไฟล์ลำดับล่าสุด
          else:
              while(os.path.isfile(downloadLicense) == True and os.path.isfile(justForConditionCheck)):
                  fileNumber += 1
                  downloadLicense = "FromParking/" + str(carLicense) + " (" + str(fileNumber) +")" + ".txt"
                  downloadShop = "FromShop/" + str(carLicense) + " (" + str(fileNumber) +")" + ".txt"
                  justForConditionCheck = "FromParking/" + str(carLicense) + " (" + str(fileNumber+1) +")" + ".txt"
          #เริ่มต้นอ่านไฟล์ที่มีอยู่ โดยจะอ่านไฟล์ตาม Directory ที่ระบุเอาไว้
          try:
             inputDownloadLicense = open(downloadLicense, "r", encoding="utf-8")
          except:
             print("Invalid input")
          else:
             #อ่านไฟล์จากทางฝั่ง Ftp Server เครื่องเข้าคิวจอดรถ
             for line in inputDownloadLicense:
                 entryDate, entryTime, entryLiscense = line.split()
             downloadFile(downloadShop)
             pricePay = 0
             #อ่านไฟล์จากทางฝั่ง Ftp Server ร้านค้า ถ้าในไฟล์ไม่มี ค่าใดๆ ซึ่งนั้นแปลว่า FTP Server ไม่มีไฟล์นั้น แปลว่า ไม่มีการใช้จ่ายใดๆ ในห้าง
             try:
                 inputDownloadShop = open(downloadShop, "r", encoding="utf-8")
                 for line in inputDownloadShop:
                     licensePlate, pricePay = line.split()
             except:
                 print("No file Directory")

             #ทำการนับลำดับของไฟล์เพื่อทำการเขียนไฟล์สรุปการใช้จ่ายของทะเบียนรถคันนั้น และ ครั้งที่นั้น
             fileNumberReport = 1
             reportPreapare = "SendReport/" + str(fileNumberReport) + ".txt"
             while(os.path.isfile(reportPreapare) == True):
                 fileNumberReport += 1
                 reportPreapare = "SendReport/" + str(fileNumberReport) + ".txt"
             updateLiscense = open(reportPreapare, mode = "w+", encoding = "utf-8")
             #การตั้งชื่อไฟล์จะตั้งเป็นตัวเลขเช่น 1.txt เพื่อให้ง่ายต่อการนำไปใช้ในกระบวนการสรุปค่าใช้จ่ายของวันนั้น
             writeupdate = entryDate + " " + entryTime + " " + entryLiscense + " " + str(pricePay) + " " + currentTimeFormat + " "
             updateLiscense.write(writeupdate)
             #ทำการเปรียบเทียบเวลาของ ขาเข้า และ ขาออก
             hourA, minuteA, secondA = entryTime.split(':')
             hourB, minuteB, secondB = currentTimeFormatOnlyTime.split(':')
             compareHour = 0
             if(int(hourA) > int(hourB)):
                 compareHour = (int(hourA) + int(hourB)) - int(hourA)
             else:
                 compareHour = int(hourB) - int(hourA)
             if(int(minuteA) > int(minuteB)):
                 compareHour =- 1
             payPark = 10 + (10*compareHour)    
             updateLiscense.write(str(payPark))
             #อัพโหลดไฟล์ลง Directory และ FTP Server เพื่อรอการสรุปผลรวม    
             updateLiscense.close()
             inputDownloadLicense.close()
             inputDownloadShop.close()
             fileNumber = 1
             fileNumberReport = 1
             uploadFile(reportPreapare)
             #ทำการแสดงผลความสำเร็จของกระบวนการ และ แสดงค่าจอดรถ
             print("Finish Update, Ready to Report")
             message = str(entryTime) + "   " + carLicense + "   " + str(currentTimeFormatOnlyTime) + " ค่าจอดรถ : " + str(payPark)
             txtTotal = Label(fTotal, text=message,font = ('Agency FB',20,'bold'), bd = 4, width = 45, height = 2, bg = "white")
             txtTotal.grid(row = 1, column = 0)
       else:
         tkinter.messagebox.showinfo("แจ้งเตือน !!!","ข้อมูลว่างเปล่ากรุณาเติมข้อมูล !!!")
         txtTotal = Label(fTotal,font = ('Agency FB',20,'bold'), bd = 4, width = 45, height = 3, bg = "white")
         txtTotal.grid(row = 1, column = 0)
    

    
def qExit():
    root.destroy()

#ฟังก์ชันสำหรับ Validate Directory ว่าโฟลเดอร์นั้นว่างหรือมีอยู่หรือไม่ ทั้งทางฝั่ง Code และ FTP
def ResetData():
   confirmqResetData = tkinter.messagebox.askquestion("ResetData","คุณต้องการรีเซ็ตโปรแกรมหรือไม่ ?")
   if confirmqResetData == "yes":
      try:
         shutil.rmtree("FromParking")
      except:
         os.mkdir("FromParking")
      else:
         try:
            os.mkdir("FromParking")
         except:
            print("You are opening the TextFile Close it first")
      try:
         shutil.rmtree("FromShop")
      except:
         os.mkdir("FromShop")
      else:
         try:
            os.mkdir("FromShop")
         except:
            print("You are opening the TextFile Close it first")
      try:
         shutil.rmtree("SendReport")
      except:
         os.mkdir("SendReport")
      else:
         try:
            os.mkdir("SendReport")
         except:
            print("You are opening the TextFile Close it first")
      try:
         ftp.cwd("FromParking")
         for something in ftp.nlst():
            try:
                ftp.delete(something)
            except Exception:
                ftp.rmd(something)
         ftp.cwd("/..")
      except:
           ftp.mkd("FromParking")
      try:
         ftp.cwd("FromShop")
         for something in ftp.nlst():
            try:
                ftp.delete(something)
            except Exception:
                ftp.rmd(something)
         ftp.cwd("/..")
      except:
           ftp.mkd("FromShop")
      try:
         ftp.cwd("SendReport")
         for something in ftp.nlst():
            try:
                ftp.delete(something)
            except Exception:
                ftp.rmd(something)
         ftp.cwd("/..")
      except:
           ftp.mkd("SendReport")

      try:
         yesterday = date.today() - timedelta(days=1)
         sendOutFile = str(yesterday) + ".txt"
         os.remove(sendOutFile)
      except:
         print("There is no Existing Txt File")
   

def ReportOperation():
    #เนื่องจากการส่งผลสรุปนั้นจำเป็นต้องส่งหลัง เที่ยงคืน ของวัน ดังนั้นเมื่อถึงเวลานั้น เราจึงต้องใช้เป็นการระบุเวลา วันก่อนวันที่จะส่งข้อมูล เพื่อให้เป็นข้อมูลของวันที่เราจะส่งจริงๆ
    #เช่น ส่งข้่อมูลของ วันที่ 1 แต่เวลาปัจจุบันได้เกินเที่ยงคืนมาแล้วจึงทำให้ ปัจจุบันอยู่วันที่ 2 ดังนั้นจึงต้องทำการ ลดเลขที่ของวัน ลงเพื่อให้ตรงของวันที่ 1
    yesterday = date.today() - timedelta(days=1)
    sendOutFile = str(yesterday) + ".txt"
    reportDirectory = 'SendReport'
    #ทำการนับจำนวนไฟล์ที่มีอยู่ใน Directory จัดเตรียมไว้เตรียมทำสรุป
    reportDirectoryCount = (len([name for name in os.listdir(reportDirectory) 
                              if os.path.isfile(os.path.join(reportDirectory, name))])) + 1
    #จะ Run ไฟล์ไปตามลำดับที่ได้ทำการนับจำนวนไฟล์ไว้เพื่อบันทึกทั้งหมดลงในไฟล์เดียว
    try:
       for i in range(1,reportDirectoryCount) :
           fileFromParking = "SendReport/" + str(i) + ".txt"
           inputfile = open(fileFromParking, "r", encoding="utf-8") 
           for line in inputfile:
                   entryDate,entryTime, carLicense, shoppingBook, exitTime, exitDate, payPark = line.split()
           out = open(sendOutFile, mode = "a", encoding = "utf-8")
           writeFile = str(entryDate) + " " + str(entryTime) + " " + str(carLicense) + " " + str(shoppingBook) + " " + str(exitTime) + " " + str(exitDate) + " " + str(payPark) +  "\n"
           out.write(writeFile)
       inputfile.close()
       out.close()
    except:
       print("No File To Report")
    #เตรียมการสำหรับส่งอีเมล
    try:
       smtp_domain = 'smtp.gmail.com'        #'smtp.gmail.com'
       smtp_port = 587                       #587
       input = open("SMTP_Account.txt")
       sender_email, sender_password, receiver_email = input.read().split(";")
       print("Sending Email")
    
       server = SMTP(smtp_domain, smtp_port)
       server.starttls()
       server.login(sender_email, sender_password)
       msg = MIMEMultipart()
       msg['From'] = sender_email
       msg['To'] = receiver_email
       msg['Subject'] = 'Daily Report'
       email_message = 'Please read this'
       body = email_message
       msg.attach(MIMEText(body, 'plain'))
       #ระบุชื่อไฟล์ว่าต้องเป็นวันก่อนหน้าวันที่ส่ง
       filename = str(yesterday) + ".txt"
       attachment = open(filename, "rb")
       part = MIMEBase('application', 'octet-stream')
       part.set_payload((attachment).read())
       encoders.encode_base64(part)
       part.add_header('Content-Disposition', "attachment; filename=%s" %filename)

       msg.attach(part)

       text = msg.as_string()

       server.sendmail(sender_email, receiver_email, text)
    except:
       print("Can't send Email")
    server.quit()
    input.close()




root = Tk()
width=1200
height=700
screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()
alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
root.geometry(alignstr)
root.title("PARKING")
root.configure(background ='seashell4')

Tops = Frame(root, width = 1000, height = 50, bg = 'seashell4', relief = SUNKEN)
Tops.pack(side = TOP)

f1 = Frame(root, width = 800, height = 700, relief = SUNKEN, bg = 'seashell4').pack()

fMainR = Frame(root, width = 150, height = 100, bd = 10, relief = RIDGE, bg = "black")
fMainR.place(x = 320, y = 410)
fTotal = Frame(fMainR, width = 150, height = 100, bd = 12, relief = "raise")
fTotal.pack(side = TOP)

lb1Info = Label(Tops, font = ('Agency FB',55,'bold'), text = "Parking !!!", fg = 'white', bg = 'black', anchor = 'w')
lb1Info.grid(row = 0, column = 0)

localtime = time.asctime(time.localtime(time.time()))
lb1Info = Label(Tops, font = ('Agency FB',20,'bold'), text = localtime, fg = 'black', anchor = 'w')
lb1Info.grid(row = 2, column = 0)

global isEmailSent 
isEmailSent = False
def clock():
    global isEmailSent 
    curtime = datetime.now()
    ftime = curtime.strftime('%a %d %b %Y %H:%M:%S %p')
    lb1Info.config(text=ftime)
    lb1Info.after(1000, clock)
    #ตั้งค่าว่า ชั่วโมงที่เท่าไหร่ จึงจะส่ง Email
    if(int(curtime.strftime('%H')) >= 2 and int(curtime.strftime('%H')) <= 5) and isEmailSent == False:
       isEmailSent = True
       try:
          ReportOperation()
       except:
          print("No File to Report")
    if(int(curtime.strftime('%H')) > 5 and int(curtime.strftime('%H')) <= 23) and isEmailSent == True:
       isEmailSent = False
    #ตั้งค่าว่า ชั่วโมงที่เท่าไหร่ จึงจะเปลี่ยนเครื่อง   
    if(int(curtime.strftime('%H')) >= 3  and int(curtime.strftime('%H')) <= 23):
       message = "1"
       txtTotal = Label(fTotal, text=str(message),font = ('Agency FB',20,'bold'), bd = 4, width = 5, height = 1, bg = "yellow")
       txtTotal.grid(row = 0, column = 0)
    elif(int(curtime.strftime('%H')) >= 0  and int(curtime.strftime('%H')) <= 2):
       message = "2"
       txtTotal = Label(fTotal, text=str(message),font = ('Agency FB',20,'bold'), bd = 4, width = 5, height = 1, bg = "yellow")
       txtTotal.grid(row = 0, column = 0)
             
       
clock()    

lblReference = Label(f1, font = ('Agency FB',30,'bold'),
                     text = "CAR Registration", bg ='white')
lblReference.place(x = 480, y = 200)

txtReference = Entry(f1, font = ('Agency FB',25,'bold'),
                     insertwidth = 4, bd = 4, relief = RIDGE, bg = "white", justify = 'left')
txtReference.place(x = 455, y = 270)

lblTotal = Label(fTotal, font = ('Agency FB',15,'bold'),
                 text = "TOTAL", bd = 2, anchor = 'w')
lblTotal.grid(row = 0, column = 0, sticky = W)

txtTotal = Text(fTotal, font = ('Agency FB',20,'bold'),
                bd = 4, width = 45, height = 3, bg = "white")
txtTotal.grid(row = 1, column = 0)




btnEnter = Button(f1, padx = 6, pady = 4, bd = 6, fg = 'black',
                  font = ('Agency FB',16,'bold'), width = 5,text = "Entry", bg = 'bisque4',
                  command = lambda:EnterOperation()).place(x = 520, y = 340)

btnOut = Button(f1, padx = 6, pady = 4, bd = 6, fg = 'black',
                font = ('Agency FB',16,'bold'), width = 5,text = "Quit", bg = 'bisque4',
                command = lambda:ExitOperation()).place(x = 610, y = 340)

btnExit = Button(f1, padx = 6, pady = 4, bd = 10,fg = 'black',
                 font = ('Agency FB',20,'bold'),width = 7,text = "EXIT", bg = 'bisque4',
                 command = lambda:qExit()).place(x = 420, y = 600)

btnReset = Button(f1, padx = 6, pady = 4, bd = 10, fg = 'black',
                  font = ('Agency FB',20,'bold'), width = 8,text = "RESET DATA", bg = 'bisque4', command = lambda:ResetData()).place(x = 555, y = 600)

btnSend = Button(f1, padx = 6, pady = 4, bd = 10, fg = 'black',
                 font = ('Agency FB',20,'bold'), width = 7,text = "SUM", bg = 'bisque4',
                 command = lambda:ReportOperation()).place(x = 690, y = 600)


root.mainloop()
