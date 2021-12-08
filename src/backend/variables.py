
# Variable initialization
smtp_serv = "localhost"
port_w_tls = None
port = 2525
email_adress = "a"
email_password = "a"

imap_serv = "a"
imap_port = 0

server = None # active server instance

# State machine function, for choosing SMTP server
def choose_smtp(number, advanced_smtp, advanced_port):
    global smtp_serv, port_w_tls, port

    ## DISABLE SMTP FOR NOW BECAUSE https://github.com/rnwood/smtp4dev
    # return smtp_serv, port_w_tls, port

    if number == 0:
        smtp_serv = "smtp-mail.outlook.com"
        port_w_tls = 587
        port = 25
    elif number == 1:
        smtp_serv = "smtp.gmail.com"
        port_w_tls = 587
        port = 25
    elif number == 2:
        smtp_serv = advanced_smtp
        port_w_tls = advanced_port
        port = 25
    # print("SMTP server: ", smtp_serv, " // SMTP Port: ", port_w_tls)
    return smtp_serv, port_w_tls, port

def choose_imap(number, advanced_imap, advanced_im_port):
    global imap_serv, imap_port
    if number == 0:
        imap_serv = "imap-mail.outlook.com"
        imap_port = 993
    elif number == 1:
        imap_serv = "imap.gmail.com"
        imap_port = 993
    elif number == 2:
        imap_serv = advanced_imap
        imap_port = advanced_im_port
    return imap_serv, imap_port

# Function for passing login credentials from login UI page
def load_login(email_adr, email_pwd):
    global email_adress, email_password
    email_adress = email_adr
    email_password = email_pwd
    return email_adress, email_password
