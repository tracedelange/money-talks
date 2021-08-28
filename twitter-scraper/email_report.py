import smtplib
from email.message import EmailMessage
from config import email_config

def email_report(body, to, subject):

    gmail_user = email_config.gmail_user
    gmail_password = email_config.gmail_password


    msg = EmailMessage()
    msg.set_content(body)

    msg['Subject'] = subject
    msg['From'] = gmail_user
    msg['To'] = to

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        # server.sendmail(sent_from, to, body)
        server.send_message(msg)
        server.close()
        print('Email sent!')
    except:
        print('Something went wrong...')

    return


if __name__ == "__main__":


    sending_to = input('Sending to: ')
    subject = input('Message subject: ')
    body = input('Message body: ')

    email_report(body,sending_to, subject)


    