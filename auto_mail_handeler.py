#modules
from time import sleep
import smtplib, ssl
import imaplib
import email
import os
from datetime import datetime
from dotenv import load_dotenv
import base64

failed_counter = 0
message = ""
port = 465  # For SSL
smtp_server = "smtp.gmail.com"
#credentials
username ="tb.token.dealer@gmail.com"
#password
load_dotenv('.env')
app_password = password = base64.b64decode(os.environ.get("password")).decode("utf-8")
#mail reciver
mail_reciever = "edin.grech@gmail.com"
gmail_host= 'imap.gmail.com'
#set connection
mail = imaplib.IMAP4_SSL(gmail_host)
#login
mail.login(username, app_password)


def setTimeVerification():
    global current_date
    global current_date_time
    current_date = str(datetime.today().strftime("%d-%b-%Y"))
    current_date_time = email.utils.formatdate(localtime=True)

def mailLookUp():
    global failed_counter
    global message
    #look for new 
    mail.select("INBOX")
    _, selected_mails = mail.search(None, 'FROM "'+mail_reciever+'" SINCE "'+current_date+'" UNSEEN')

    if len(selected_mails[0].split()) == 0:
        print("No new mail",failed_counter,end="\r")
        failed_counter += 1
        sleep(5)
        mailLookUp()
    elif failed_counter >= 100:
        print("ERROR No new mail",failed_counter,"\n=====Time expired=====")
        message = False
    else:
        print("==== Mail found ====")
        failed_counter = 0

        for num in selected_mails[0].split():
            _, data = mail.fetch(num , '(RFC822)')
            _, bytes_data = data[0]

            #convert the byte data to message
            email_message = email.message_from_bytes(bytes_data)
            messageLo = email_message["Subject"]
            print(message)
            #get mail time only
            email_recived_time = email_message['Date'][17:25]
            if email_recived_time <= current_date_time:
                message = messageLo
            else:
                print("==== ERROR Mail is old====")
                message = False
    

def send_email_notification(message=None):
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(username, app_password)
        server.sendmail(username, mail_reciever, message)