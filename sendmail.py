import smtplib

# Gudie: https://www.youtube.com/watch?v=mWZYn5I_jkY

#None essential importations for different purposes
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from getpass import getpass

# Regulate mail to send from, and mail to send to

sendfrom = 'martin.hatting@hotmail.com'
sendto = 'koentimmy@hotmail.com'
#sendto = input("Type recipient mail here \n")
#sendfrom = input("Type mail adress here \n")

# SMTP SERVER
smtpserv = "smtp-mail.outlook.com"
port_w_tls = 587
port = 25

#smtp.gmail.com is the google smtp server. Change depending on provider
server = smtplib.SMTP(smtpserv, port)
server.connect(smtpserv, port_w_tls)
#587 // 465

#Starts the process
server.ehlo()
server.starttls()
server.ehlo()

#Login process. Recommended to save login data in encrpyted text file,
# which upon loading gets decrpyted and used
#Something we could consider for the UI to forward to the backend
#server.login('martin.hatting@hotmail.com', 'password')

# doing it from text file, is:
#with open('password.txt', 'r') as f:
#    password = f.read()

print("Enter password for mail")
password = getpass()

server.login(sendfrom, password)

msg = MIMEMultipart()
msg['From'] = 'Martin Braas'
msg['To'] = 'koentimmy@hotmail.com'
msg['Subject'] = 'Just a test'

with open('message.txt', 'r') as f:
    message = f.read()

msg.attach(MIMEText(message, 'plain'))

filename = 'images.jpeg'
#'rb' as tag, due to working with image data, not text data
attachment = open(filename, 'rb')

#Payload object
p = MIMEBase('application', 'octet-stream')
p.set_payload(attachment.read())

encoders.encode_base64(p)
p.add_header('Content-Disposition', f'attachment; filename={filename}')
msg.attach(p)

text = msg.as_string()
server.sendmail(sendfrom, sendto, text)

#Exiting server connection
server.quit()