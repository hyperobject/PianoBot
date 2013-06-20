import random
import string
import os
from subprocess import call
from getpass import getpass
import urllib
import imaplib
import smtplib
def generate_id(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for x in range(size))
def imap_get_latest(username, password, imap):
	imap_server = imaplib.IMAP4_SSL(imap)
	imap_server.login(username, password)
	imap_server.select('inbox')
	result, data = imap_server.uid('search', None, "ALL")
	latest_email_uid = data[0].split()[-1]
	result, data = imap_server.uid('fetch', latest_email_uid, '(RFC822)')
	raw_email = data[0][1]
	imap_server.logout()
	return email.message_from_string(raw_email)
def sendemail(username, password, server, body, subject, toaddr):
	msg = MIMEMultipart()
	msg['From'] = username
	msg['To'] = toaddr
	msg['Subject'] = subject
	part = MIMEText(body, 'plain')
	msg.attach(part)
	emailserver = smtplib.SMTP(server)
	emailserver.starttls()
	emailserver.login(username,password)
	emailserver.sendmail(username, toaddr, msg.as_string())
	emailserver.quit()
username = raw_input('Email username? ')
password = getpass('Email password? (hidden) ')
port = raw_input('MIDI port? ')
code = generate_id()
usedCode = None
while True: #main loop
	latest_email = imap_get_latest(username, password, 'imap.gmail.com')
	if latest_email['Subject'] == code and not latest_email['Subject'] == usedCode:
		body = latest_email.get_payload()[0].get_payload()
		urllib.urlretrieve(body, 'play.mid')
		call(['pmidi -p', port + ' play.mid'])
		os.remove('play.mid')
		usedCode = code
		code = generate_id()
		sendemail(username, password, 'smtp.gmail.com:587', 'Thanks. Command was ' + body + '. The new code is ' + code, "Command ran successfully", latest_email['From'])
		print code
	time.sleep(60)
