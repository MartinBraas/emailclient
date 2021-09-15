
smtp_serv = "a"
port_w_tls = 0
port = 0

email_adress = "a"
email_password = "a"

def choose_smtp(number):
    global smtp_serv, port_w_tls, port
    if number == 0:
        smtp_serv = "smtp-mail.outlook.com"
        port_w_tls = 587
        port = 25
    elif number == 1:
        smtp_serv = "smtp.gmail.com"
        port_w_tls = 587
        port = 25
    return smtp_serv, port_w_tls, port

def load_login(email_adr, email_pwd):
    global email_adress, email_password
    email_adress = email_adr
    email_password = email_pwd
    return email_adress, email_password
