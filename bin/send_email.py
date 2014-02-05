import os,smtplib  
from email.mime.text import MIMEText

def send_email(recipients_array, subject, message, config):
	# Optional send of confirmation email
	# See here: http://www.nixtutor.com/linux/send-mail-through-gmail-with-python/
	if all (key in config for key in (
		"EMAIL_USERNAME",
		"EMAIL_PASSWORD",
		"EMAIL_SERVER",
		"EMAIL_FROM",
	)):
		server = smtplib.SMTP(config['EMAIL_SERVER']) 
		# server.set_debuglevel(1) 
		msg = MIMEText(message)
		sender = config['EMAIL_SERVER']
		msg['Subject'] = "subject line"
		msg['From'] = config['EMAIL_FROM']
		msg['To'] = ", ".join(recipients_array)
		server.starttls()
		server.login(config['EMAIL_USERNAME'],config['EMAIL_PASSWORD'])
		server.sendmail(sender, recipients_array, msg.as_string())
		server.quit()
		print ("Sent email notification to %s" % (', '.join(recipients_array)))
	else:
		print "Missing email config settings"
