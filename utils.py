import csv
import datetime
import constants
import smtplib
from email.message import EmailMessage


def log_disaster(website, critical=False):
    """
    This function will log the disaster into a csv file.
    """
    now = datetime.datetime.now()
    status = "DOWN!"
    if critical:
        status = "CRITICAL!"
    with open(constants.csv_log_file_address, mode='a') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow([str(now), website, status])


def alarm_admin(website):
    """
    This function will alarm admin with an email contaims the log of down-time
    """

    with open(constants.csv_log_file_address) as fp:
        msg = EmailMessage()
        msg.set_content(fp.read())

    msg['Subject'] = "CRITICAL EMAIL !"
    msg['From'] = 'a.farhadi@pishro.computer'
    msg['To'] = constants.admin_email

    try:
        smtpObj = smtplib.SMTP(constants.EMAIL_HOST, constants.EMAIL_PORT)
        smtpObj.ehlo()
        smtpObj.starttls()
        smtpObj.ehlo()
        smtpObj.login(constants.EMAIL_HOST_USER, constants.EMAIL_HOST_PASSWORD)
        smtpObj.send_message(msg)
        print("Successfully sent email")
    except Exception as e:
        print("Error: unable to send email\n", e)
