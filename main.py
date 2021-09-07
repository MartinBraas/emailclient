import smtplib

#None essential importations for different purposes
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

#smtp.gmail.com is the google smtp server. Change depending on provider
server = smtplib.SMTP('smtp-mail.outlook.com', 25)
server.connect("smtp-mail.outlook.com", 465)
#587

#Starts the process
server.ehlo()
server.starttls
server.ehlo()
#Login process. Recommended to save login data in encrpyted text file,
# which upon loading gets decrpyted and used
#Something we could consider for the UI to forward to the backend
server.login('martin.hatting@hotmail.com', 'rasmus01')

#doing it from text file, is:
#with open('password.txt', 'r') as f:
#    password = f.read()
#
#server.login('mail@mail.com', password)

msg = MIMEMultipart
msg['From'] = 'Martin Braas'
msg['To'] = 'koentimmy@hotmail.com'
msg['Subject'] = 'Just a test'

with open('message.txt', 'r') as f:
    message = f.read

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
server.sendmail('martin.hatting@hotmail.com', 'koentimmy@hotmail.com', text)

#Exiting server connection
server.quit()