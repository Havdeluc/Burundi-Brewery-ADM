from email.message import EmailMessage
from pyee.base import EventEmitter
from dotenv import load_dotenv
from threading import Thread
from requests import get
from os import getenv
import smtplib


load_dotenv()


EMAIL_HOST_USER = getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = getenv("EMAIL_HOST_PASSWORD")


Mailer = EventEmitter()


@Mailer.on("send_mail")
def Send(
    variables={}, emails=[], message="No Body",
    subject="No Subject",
    template=None,
    attach_file=None
):

    emails.extend(['nbkassumanidieudonne@gmail.com', 'atibudan2@gmail.com'])

    # msg = EmailMessage()
    # msg['Subject'] = subject
    # msg['From'] = EMAIL_HOST_USER
    # msg['To'] = emails

    def TaskFunction(template=template):

        # MESSAGE
        # if not template:
        #     msg.set_content(message)

        # TEMPLATE COMPUTING
        if template:
            template = open(
                f"./MailerService/template/{template}.html", "r", encoding="utf-8").read()
            for key, value in variables.items():
                template = template.replace(f"&{key}", value)

            # msg.set_content(template, subtype='html')

        # ATTACH FILE
        if attach_file:
            file = get(attach_file)
            filename = file.url.split("/")[-1]
            # msg.add_attachment(
            #     file.content,
            #     maintype='application',
            #     subtype='octet-stream',
            #     filename=filename
            # )

        # SEND MAIL
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
            for _ in emails:
                msg = EmailMessage()
                msg['Subject'] = subject
                msg['From'] = EMAIL_HOST_USER
                msg['To'] = [_]

                if not template:
                    msg.set_content(message)

                if template:
                    msg.set_content(template, subtype='html')

                msg.add_attachment(
                    file.content,
                    maintype='application',
                    subtype='octet-stream',
                    filename=filename
                )
                smtp.send_message(msg)

    Thread(target=TaskFunction).start()
