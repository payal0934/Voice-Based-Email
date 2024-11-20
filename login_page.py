import imaplib, email
import smtplib
from gtts import gTTS
from playsound import playsound
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders 
from text_speech import *

import os
import re



password = ""
addres = ""
item = ""
subject = ""
body = ""
signal = 0
s = smtplib.SMTP('smtp.gmail.com',587)
s.starttls()
imap_url = 'imap.gmail.com'
conn = imaplib.IMAP4_SSL(imap_url)
attachment_dir = 'C:/Users/Desktop/'



def convert_special_char(text):
    temp = text
    special_chars = ['attherate', 'dot', 'underscore', 'dollar', 'hash', 'star', 'plus', 'minus', 'space', 'dash']
    for character in special_chars:
        while(True):
            pos = temp.find(character)
            if pos == -1:
                break

            else:
                if character == 'attherate':
                    temp = temp.replace('attherate', '@')
                elif character == 'dot':
                    temp = temp.replace('dot', '.')
                elif character == 'underscore':
                    temp = temp.replace('underscore', '_')
                elif character == 'dollar':
                    temp = temp.replace('dollar', '$')
                elif character == 'hash':
                    temp = temp.replace('hash', '#')
                elif character == 'star':
                    temp = temp.replace('star', '*')
                elif character == 'plus':
                    temp = temp.replace('plus', '+')
                elif character == 'minus':
                    temp = temp.replace('minus', '-')
                elif character == 'space':
                    temp = temp.replace('space', '')
                elif character == 'dash':
                    temp = temp.replace('dash', '-')

    return temp
                




def compose_area():
    global addres, password, s, item, subject, body

    text_to_speech("you have reached the page where you can compose and send email.")
    flag = True
    flag1 = True
    fromaddr = addres
    toaddr = list()

    while(flag1):
        while(flag):
            text_to_speech("enter receiver's email address")
            to = ""
            to = speech_to_text(15)
            print(to)
            # to = input()

            if to != 'n':
                text_to_speech("you meant" + to + "say yes to confirm or no to enter again")
                say = speech_to_text(5)
                # say = input()
                if(say == 'yes' or say == 'ye' or say == 's'):
                    toaddr.append(to)
                    flag = False
            else:
                text_to_speech("could not understand what you meant")

        text_to_speech("Do you want to enter more recipient? say yes or no")
        say1 = speech_to_text(3)
        # say1 = input()
        if(say1 == 'no' or 'no' in say1):
            flag1 = False

        flag = True

    newtoaddr = list()
    for item in toaddr:
        item = item.strip()
        item = item.replace(' ', '')
        item = convert_special_char(item)
        newtoaddr.append(item)
        print(item)

    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = ",".join(newtoaddr)
    flag = True

    while(flag):
        text_to_speech("enter subject")
        
        subject = speech_to_text(10)
        # subject = input()
        if subject == 'n':
            text_to_speech("could not understand what you meant")
        else:
            flag = False
    print(subject)
    msg['Subject'] = subject
    flag = True
    while flag:
        text_to_speech("enter body of the mail")
        body = speech_to_text(20)
        # body = input()
        if body == 'n':
            text_to_speech("could not understand what you meant")
        else:
            flag = False
    print(body)
    msg.attach(MIMEText(body, 'plain'))
    text_to_speech("any attachment? say yes or no")
    x = speech_to_text(3)
    # x = input()
    x = x.lower()
    if x == 'yes':
        text_to_speech("Do you want to record an audio and send as an attachment?")
        say = speech_to_text(2)
        # say = input()
        say = say.lower()

        if say == 'yes' or 'yes' in say:
            text_to_speech("Enter filename.")
            filename = speech_to_text(5)
            filename = input()
            filename = filename.lower()
            filename = filename + '.mp3'
            filename = filename.replace(' ', '')
            print(filename)
            text_to_speech("Enter your audio message.")
            audio_msg = speech_to_text(10)
            flagconf = True
            while flagconf:
                try:
                    tts = gTTS(text=audio_msg, lang='en', slow=False)
                    tts.save(filename)
                    flagconf = False
                except:
                    print('Trying again')
            attachment = open(filename, "rb")
            p = MIMEBase('application', 'octet-stream')
            p.set_payload((attachment).read())
            encoders.encode_base64(p)
            p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
            msg.attach(p)

        elif say == 'no':
            text_to_speech("Enter filename with extension")

            filename = speech_to_text(5)
            filename = input()
            filename = filename.strip()
            filename = filename.replace(' ', '')
            filename = filename.lower()
            filename = convert_special_char(filename)
            
            attachment = open(filename, "rb")
            p = MIMEBase('application', 'octet-stream')
            p.set_payload((attachment).read())
            encoders.encode_base64(p)
            p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
            msg.attach(p)
    try:
        s.sendmail(fromaddr, newtoaddr, msg.as_string())
        text_to_speech("Your email has been sent successfully. You will now be redirected to the menu page.")
        
    except:
        text_to_speech("Sorry, your email failed to send. please try again. You will now be redirected to the the compose page again.")
        
    s.quit()
    print("success")
    
    # compose  = Compose()
    # compose.recipient = item
    # compose.subject = subject
    # compose.body = body

    


def get_body(msg):
    if msg.is_multipart():
        return get_body(msg.get_payload(0))
    else:
        return msg.get_payload(None, True)
    

def get_attachment(msg):
    global i
    for part in msg.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        filename = part.get_filename()
        if bool(filename):
            filepath = os.path.join(attachment_dir, filename)
            with open(filepath, "wb") as f:
                f.write(part.get_payload(decode=True))
                text_to_speech("Attachment has been downloaded")
               
                path = 'C:/Users/hp/Desktop/'
                files = os.listdir(path)
                paths = [os.path.join(path, basename) for basename in files]
                file_name = max(paths, key=os.path.getctime)
            with open(file_name, "rb") as f:
                if file_name.find('.jpg') != -1:
                    text_to_speech("attachment is an image")
               
                if file_name.find('.png') != -1:
                    text_to_speech("attachment is an image")
               
                if file_name.find('.mp3') != -1:
                    text_to_speech("Playing the downloaded audio file.")
                    
                    playsound(file_name)



def reply_mail(msg_id, message):
    global s
    TO_ADDRESS = message['From']
    FROM_ADDRESS = addres
    msg = email.mime.multipart.MIMEMultipart()
    msg['to'] = TO_ADDRESS
    msg['from'] = FROM_ADDRESS
    msg['subject'] = message['Subject']
    msg.add_header('In-Reply-To', msg_id)
    flag = True
    while(flag):
        text_to_speech("Enter body.")
        # body = input()
        body = speech_to_text(20)
        print(body)
        try:
            msg.attach(MIMEText(body, 'plain'))
            s.sendmail(msg['from'], msg['to'], msg.as_string())
            text_to_speech("Your reply has been sent successfully.")
            
            flag = False
        except:
            text_to_speech("Your reply could not be sent. Do you want to try again? Say yes or no.")
            # act = input()
            act = speech_to_text(3)
            act = act.lower()
            if act != 'yes':
                flag = False


def frwd_mail(item, message):
    global s
    flag1 = True
    flag = True
    global i
    newtoaddr = list()
    while flag:
        while flag1:
            while True:
                text_to_speech("Enter receiver's email address")
                # to = input()
                to = speech_to_text(15)
                text_to_speech("You meant " + to + " say yes to confirm or no to enter again")
                # yn = input()
                yn = speech_to_text(3)
                yn = yn.lower()
                if yn == 'yes':
                    to = to.strip()
                    to = to.replace(' ', '')
                    to = to.lower()
                    to = convert_special_char(to)
                    print(to)
                    newtoaddr.append(to)
                    break
            text_to_speech("Do you want to add more recepients?")
            # ans1 = input()
            ans1 = speech_to_text(3)
            ans1 = ans1.lower()
            print(ans1)
            if ans1 == "no" :
                flag1 = False

        message['From'] = addres
        message['To'] = ",".join(newtoaddr)
        try:
            s.sendmail(addres, newtoaddr, message.as_string())
            text_to_speech("Your mail has been forwarded successfully.")
            
            flag = False
        except:
            text_to_speech("Your mail could not be forwarded. Do you want to try again? Say yes or no.")
            # act = input()
            act = speech_to_text(3)
            act = act.lower()
            if act != 'yes':
                flag = False


def read_mails(mail_list,folder):
    global s
    mail_list.reverse()
    mail_count = 0
    to_read_list = list()
    for item in mail_list:
        result, email_data = conn.fetch(item, '(RFC822)')
        raw_email = email_data[0][1].decode()
        message = email.message_from_string(raw_email)
        To = message['To']
        From = message['From']
        Subject = message['Subject']
        Msg_id = message['Message-ID']
        text_to_speech("Email number " + str(mail_count + 1) + "    .The mail is from " + From + " to " + To + "  . The subject of the mail is " + Subject)
        
        print('message id= ', Msg_id)
        print('From :', From)
        print('To :', To)
        print('Subject :', Subject)
        print("\n")
        to_read_list.append(Msg_id)
        mail_count = mail_count + 1

    flag = True
    while flag :
        n = 0
        flag1 = True
        while flag1:
            text_to_speech("Enter the email number of mail you want to read.")
            # n = input()
            n = speech_to_text(2)
            if (n == 'one'):
                n = '1'
            if n == 'tu' or n == 'two' or n == 'too' or n == 'to':
                n = '2'
            
            print(n)
            text_to_speech("You meant " + str(n) + ". Say yes or no.")
            # say = input()
            say = speech_to_text(2)
            # say = say.lower()
            if say == 'yes' or say == 'ye' or say == 's':
                flag1 = False
        n = int(n)
        msgid = to_read_list[n - 1]
        print("message id is =", msgid)
        typ, data = conn.search(None, '(HEADER Message-ID "%s")' % msgid)
        data = data[0]
        result, email_data = conn.fetch(data, '(RFC822)')
        raw_email = email_data[0][1].decode()
        message = email.message_from_string(raw_email)
        To = message['To']
        From = message['From']
        Subject = message['Subject']
        Msg_id = message['Message-ID']
        print('From :', From)
        print('To :', To)
        print('Subject :', Subject)
        text_to_speech("The mail is from " + From + " to " + To + "  . The subject of the mail is " + Subject)
        
        Body = get_body(message)
        Body = Body.decode()
        Body = re.sub('<.*?>', '', Body)
        Body = os.linesep.join([s for s in Body.splitlines() if s])
        if Body != '':
            text_to_speech(Body)
            
        else:
            text_to_speech("Body is empty.")

        get_attachment(message)

        if folder == 'inbox':
            text_to_speech("Do you want to reply to this mail? Say yes or no. ")
            # ans = input()
            ans = speech_to_text(3)
            ans = ans.lower()
            print(ans)
            if ans == "yes" or ans == 'ye' or ans == 's':
                reply_mail(Msg_id, message)

        if folder == 'inbox' or folder == 'sent':
            text_to_speech("Do you want to forward this mail to anyone? Say yes or no. ")
            ans = speech_to_text(3)
            # ans = input()
            ans = ans.lower()
            print(ans)
            if ans == "yes" or ans == 'ye' or ans == 's':
                frwd_mail(Msg_id, message)


        if folder == 'inbox' or folder == 'sent':
            text_to_speech("Do you want to delete this mail? Say yes or no. ")
            # ans = input()
            ans = speech_to_text(3)
            ans = ans.lower()
            print(ans)
            if ans == "yes" or ans == 'ye' or ans == 's':
                try:
                    conn.store(data, '+X-GM-LABELS', '\\Trash')
                    conn.expunge()
                    text_to_speech("The mail has been deleted successfully.")
                   
                    print("mail deleted")
                except:
                    text_to_speech("Sorry, could not delete this mail. Please try again later.")
                    

        if folder == 'trash':
            text_to_speech("Do you want to delete this mail? Say yes or no. ")
            # ans = input()
            ans = speech_to_text(3)
            ans = ans.lower()
            print(ans)
            if ans == "yes" or ans == 'ye' or ans == 's':
                try:
                    conn.store(data, '+FLAGS', '\\Deleted')
                    conn.expunge()
                    text_to_speech("The mail has been deleted permanently.")
                    
                    print("mail deleted")
                except:
                    text_to_speech("Sorry, could not delete this mail. Please try again later.")
                    

        text_to_speech("Email ends here.")

        text_to_speech("Do you want to read more mails?")
        # ans = input()
        ans = speech_to_text(2)
        ans = ans.lower()
        if ans == "no":
            flag = False


def search_specific_mail(folder,key,value,foldername):
    global i, conn
    conn.select(folder)
    result, data = conn.search(None,key,'"{}"'.format(value))
    mail_list=data[0].split()
    if len(mail_list) != 0:
        text_to_speech("There are " + str(len(mail_list)) + " emails with this email ID.")
    
    if len(mail_list) == 0:
        text_to_speech("There are no emails with this email ID.")

    else:
        read_mails(mail_list,foldername)



def inbox_view():
    global addres, password, conn
    
    imap_url = 'imap.gmail.com'
    conn = imaplib.IMAP4_SSL(imap_url)
    conn.login(addres, password)
    conn.select('"INBOX"')
    result, data = conn.search(None, '(UNSEEN)')
    unread_list = data[0].split()
    no = len(unread_list)
    result1, data1 = conn.search(None, "ALL")
    mail_list = data1[0].split()
    text = "You have reached your inbox. There are " + str(len(mail_list)) + " total mails in your inbox. You have " + str(no) + " unread emails" + ". To read unread emails say unread. To search a specific email say search. To go back to the menu page say back. To logout say logout."
    text_to_speech(text)
    
    flag = True
    while(flag):
        act = speech_to_text(5)
        # act = input()
        act = act.lower()
        print(act)
        if act == 'unread' or act == 'read' or act == 'ead':
            flag = False
            if no!=0:
                read_mails(unread_list,'inbox')
            else:
                text_to_speech("You have no unread emails.")
                
        elif act == 'search':
            flag = False
            emailid = ""
            while True:
                text_to_speech("Enter email ID of the person who's email you want to search.")
                # emailid = input()
                emailid = speech_to_text(15)
                print(emailid)
                text_to_speech("You meant " + emailid + " say yes to confirm or no to enter again")
                # yn = input()
                yn = speech_to_text(5)
                yn = yn.lower()
                if yn == 'yes' or yn == 'ye' or yn == 's':
                    break
            emailid = emailid.strip()
            emailid = emailid.replace(' ', '')
            emailid = emailid.lower()
            emailid = convert_special_char(emailid)
            search_specific_mail('INBOX', 'FROM', emailid,'inbox')

        elif act == 'back':
            text_to_speech("You will now be redirected to the menu page.")
            conn.logout()
            print("successs")
            activity_area()

        elif act == 'log out':
            addres = ""
            password = ""
            text_to_speech("Please Once Click On the screen then you will be redirected to login page")
            

        else:
            text_to_speech("Invalid action. Please try again.")
            

        text_to_speech("If you wish to do anything else in the inbox or logout of your mail say yes or else say no.")
        # ans = input()
        ans = speech_to_text(3)
        ans = ans.lower()
        if ans == 'yes' or ans == 'ye' or ans == 's':
            flag = True
            text_to_speech("Enter your desired action. Say unread, search, back or logout. ")
            
    text_to_speech("You will now be redirected to the menu page.")
    
    conn.logout()
    print("success")
    

def sent_view():
    global addres, password, conn
    
    imap_url = 'imap.gmail.com'
    conn = imaplib.IMAP4_SSL(imap_url)
    conn.login(addres, password)
    conn.select('"[Gmail]/Sent Mail"')
    result1, data1 = conn.search(None, "ALL")
    mail_list = data1[0].split()
    text = "You have reached your sent mails folder. You have " + str(len(mail_list)) + " mails in your sent mails folder. To search a specific email say search. To go back to the menu page say back. To logout say logout."
    text_to_speech(text)

    flag = True
    while (flag):
        act = speech_to_text(5)
        act = act.lower()
        print(act)
        if act == 'search':
            flag = False
            emailid = ""
            while True:
                text_to_speech("Enter email ID of receiver.")
              
                emailid = speech_to_text(15)
                text_to_speech("You meant " + emailid + " say yes to confirm or no to enter again")
                
                yn = speech_to_text(5)
                yn = yn.lower()
                if yn == 'yes' or yn == 'ye' or yn == 's':
                    break
            emailid = emailid.strip()
            emailid = emailid.replace(' ', '')
            emailid = emailid.lower()
            emailid = convert_special_char(emailid)
            search_specific_mail('"[Gmail]/Sent Mail"', 'TO', emailid,'sent')

        elif act == 'back':
            text_to_speech("You will now be redirected to the menu page.")

            conn.logout()
            print("success")
            activity_area()

        elif act == 'log out':
            addres = ""
            password = ""
            text_to_speech("Please Once Click On the screen then you will be redirected to login page")
            print("success")

        else:
            text_to_speech("Invalid action. Please try again.")
           

        text_to_speech("If you wish to do anything else in the sent mails folder or logout of your mail say yes or else say no.")
        
        ans = speech_to_text(3)
        ans = ans.lower()
        if ans == 'yes' or ans == 'ye' or ans == 's':
            flag = True
            text_to_speech("Enter your desired action. Say search, back or logout. ")
            i = i + str(1)
    text_to_speech("You will now be redirected to the menu page.")

    conn.logout()
    print("success")
    
    

def trash_view():
    global addres, password, conn
    
    imap_url = 'imap.gmail.com'
    conn = imaplib.IMAP4_SSL(imap_url)
    conn.login(addres, password)
    conn.select('"[Gmail]/Trash"')
    result1, data1 = conn.search(None, "ALL")
    mail_list = data1[0].split()
    text = "You have reached your trash folder. You have " + str(len(mail_list)) + " mails in your trash folder. To search a specific email say search. To go back to the menu page say back. To logout say logout."
    text_to_speech(text)
   
    flag = True
    while (flag):
        act = speech_to_text(5)
        act = act.lower()
        print(act)
        if act == 'search':
            flag = False
            emailid = ""
            while True:
                text_to_speech("Enter email ID of sender.")
                
                emailid = speech_to_text(15)
                text_to_speech("You meant " + emailid + " say yes to confirm or no to enter again")
             
                yn = speech_to_text(5)
                yn = yn.lower()
                if yn == 'yes' or  yn == 'ye' or yn == 's':
                    break
            emailid = emailid.strip()
            emailid = emailid.replace(' ', '')
            emailid = emailid.lower()
            emailid = convert_special_char(emailid)
            search_specific_mail('"[Gmail]/Trash"', 'FROM', emailid, 'trash')

        elif act == 'back':
            text_to_speech("You will now be redirected to the menu page.")
      
            conn.logout()
            print('success')
            activity_area()

        elif act == 'log out':
            addres = ""
            password = ""
            text_to_speech("You have been logged out of your account and now will be redirected back to the login page.")
            print('logout')

        else:
            text_to_speech("Invalid action. Please try again.")
   
        text_to_speech("If you wish to do anything else in the trash folder or logout of your mail say yes or else say no.")

        ans = speech_to_text(3)
        ans = ans.lower()
        print(ans)
        if ans == 'yes' or ans == 'ye' or ans == 's':
            flag = True
            text_to_speech("Enter your desired action. Say search, back or logout. ")
            
    text_to_speech("You will now be redirected to the menu page.")
    
    conn.logout()
    print("success")
    
        


def activity_area():
    global addres, password, signal

    flag = True
    if(signal == 0):
        text_to_speech("you have logged into your account. What would you like to do?")

    while(flag):
        text_to_speech("to compose email say compose. To open inbox folder say inbox . To open sent folder say sent. to open trash folder say trash. To logout say logout. Do you want me to repeat?")
        say = speech_to_text(3)
        # say = input()
        if say == 'no' or say == 'o':
            flag = False

    text_to_speech("Enter your desired action")
    
    act = speech_to_text(5)
    print(act)
    act = act.lower()
    signal = 1


    if act == "compose" or "compo" in act:
        compose_area()
        

    elif act == "inbox" or "in" in act or "box" in act:
        inbox_view()

    elif act == "sent" or act == "send"  :
        sent_view()
    elif act == "trash" or act == "crash" or act == "tash":
        trash_view()
    elif act == "logout":
        addres = ""
        password = ""
        text_to_speech("Please Once Click On the screen then you will be redirected to login page")
        
    else:
        text_to_speech("Invalid action. Please try again.")
        activity_area()


def login_area():
    global addres, password

    text_to_speech("welcome to our voice based email application. Login with your email account in order to continue.")
    # text_to_speech("welcome to voice based application")
    flag = True
    while(flag):
        text_to_speech("Enter your email")
        
        addres = speech_to_text(10)
        
        if addres != 'n':
            text_to_speech("You meant" + addres + "say yes to confirm or no to enter again")
            print(addres)
            say = speech_to_text(3)
            if(say == 'yes' or 'ye' in say or 's' in say):
                flag = False

        else:
            text_to_speech("could not understand what you meant")
            

    addres = addres.strip()
    addres = addres.replace(' ', '')
    addres = convert_special_char(addres)
  

    print(addres)

    flag = True
    while(flag):
        text_to_speech("Enter your password")
        password = speech_to_text(15)
        
        if password != 'n':
            text_to_speech("you meant" + password + "say yes to confirm or no to enter again")
            say = speech_to_text(7)
            print(password)
            if say == 'yes' or 'ye' in say or 's' in say:
                flag = False

        else:
            text_to_speech("could not understand what you meant")

    password = password.strip()
    password = password.replace(' ', '')
    password = convert_special_char(password)


    print(password)
    
    
    
    imap_url = 'imap.gmail.com'
   
    try:
        conn = imaplib.IMAP4_SSL(imap_url)
        conn.login(addres, password)

        s.login(addres, password)
        text_to_speech("congratulations. You have logged in successfully. You will now be redirected to the menu page")
        text_to_speech("now once click on the screen")
        


    except:
        text_to_speech("Invalid login Details. Please try again")


