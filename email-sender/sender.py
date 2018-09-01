import pandas
from string import Template
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

datafile_address = 'D:\Git\python-projects\email-sender\Book1.csv'
messagefile_address = 'D:\Git\python-projects\email-sender\message.txt'
my_email = 'manthanchauhan913@gmail.com'
my_password = 'password'
email_subject = 'subject of email'

def read_data():
    filename = datafile_address
    data = pandas.read_csv(filename)
    contacts = list(zip(data['name'], data['email']))
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


    
            