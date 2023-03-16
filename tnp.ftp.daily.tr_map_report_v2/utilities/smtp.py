import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.utils import formatdate
from email import encoders
import datetime
from ftplib import FTP


def send_mail(send_from, send_to, subject, text, files, isTls=True):
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = ', '.join(send_to[0:3])
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    msg.attach(MIMEText(text))

    part = MIMEBase('application', "octet-stream")
    part.set_payload(open(files, "rb").read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename=' + files)
    msg.attach(part)
    smtp = smtplib.SMTP('192.168.2.18', 25)
    if isTls:
        smtp.starttls()
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.quit()


send_from = 'TNP@tele2.kz'
send_to = ['yerlan.akhmetov@tele2.kz']
text = '''Hello!

Report Transmission Quantity sites in attachment.

Best regards TNP'''

date_now = str(datetime.datetime.now())
date_ftp_soem = date_now[:4] + date_now[5:7] + date_now[8:10]

files = 'quantity_site' + date_ftp_soem + '.xlsx'

ftp = FTP('172.18.23.111')  # IP ftp
ftp.login('ftpuser', 'ericsson')
ftp.cwd('Q-ty_site')  # path to dir

loc_file = open(files, 'wb')
ftp.retrbinary('RETR ' + files, loc_file.write, 1024)
loc_file.close()
print('downloading finished')

ftp.quit()

server = '192.168.2.18'
port = '25'
subject = files

send_mail(send_from, send_to, subject, text, files)
