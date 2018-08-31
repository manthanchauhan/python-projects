import csv
from string import Template
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

datafile_address = 'D:\Git\python-projects\email-sender\data.csv'
messagefile_address = 'D:\Git\python-projects\email-sender\message.txt'
my_email = 'myemail@gmail.com'
my_password = 'mypassword'
email_subject = 'subject of email'

def read_data():
    filename = datafile_address
    contacts = []
    datafile = open(filename, 'r')
    datareader = csv.reader(datafile)
    fields = next(datareader)
    email_pos = -1
    name_pos = -1
    l = len(fields)
    for i in range(0, l):
        if fields[i] == 'name':
            name_pos = i
        elif fields[i] == 'email':
            email_pos = i
        if email_pos != -1 and name_pos != -1:
            break
    for row in datareader:
        name = row[name_pos]
        email = row[email_pos]
        contacts.append([name, email])
    return contacts
def read_msg():
    filename = messagefile_address
    msgfile = open(filename, 'r')
    msg = msgfile.read()
    return Template(msg)
def create_channel():
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login(my_email, my_password)
    return s    
contacts = read_data()
template = read_msg()
channel = create_channel()
sent = 0
for contact in contacts:
    msg = MIMEMultipart()
    body = template.substitute(reciever_name=contact[0])
    msg['From'] = my_email
    msg['To'] = contact[1]
    msg['Subject'] = email_subject
    msg.attach(MIMEText(body, 'html'))
    channel.send_message(msg)
    sent += 1
    del msg
channel.quit()
print('Your %d email(s) were sent' %(sent))


    
            