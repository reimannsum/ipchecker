from requests import get
import smtplib, ssl, sys

port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "" + sys.args[1]  # Enter your address
receiver_email = "" + sys.args[2]  # Enter receiver address
password = '' + sys.args[0]
password = password.strip()
device_name = '' + sys.args[3] # The name of the system reporting


def print_error():
	import datetime
	t = datetime.date.today()
	error_log = open('/home/pi/logs/ip.log', 'a')
	error_string = 'No internet access at ' + t
	error_log.write(error_string)
	error_log.close()


def pull_ip(tries_failed):
	if tries_failed > 5:
		print_error()
		return ''
	try:
		ip = get('https://api.ipify.org').text
	except Exception as e:
		pull_ip(tries_failed + 1)
	else:
		return ip


def send_new_ip(new_ip):
	message = f"Subject: IP address change\n\n{0}\n{1}".format(device_name, ip)
	context = ssl.create_default_context()
	with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
		server.login(sender_email, password)
		server.sendmail(sender_email, receiver_email, message)

try:
	file = open('/home/pi/logs/myIP','r')
except Exception as e:
	currentIP = ''
else:
	currentIP = file.readline().strip()
	file.close()

ip = pull_ip(0)
if ip is not '':
	if not ip == currentIP:
		send_new_ip(ip)
		file = open('/home/pi/logs/myIP','w')
		file.write(ip)
		file.close()
