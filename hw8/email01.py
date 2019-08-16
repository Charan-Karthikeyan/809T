import os
from datetime import datetime
import smtplib
from smtplib import SMTP
from smtplib import SMTPException
import email 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

#Time stamp to record image
def mail(coord_x,coord_y):
	pic_time = datetime.now().strftime('%Y%m%d%H%M%S')
	command = 'raspistill -w 1280 -h 720 -vf -hf -o ' + pic_time +'.jpg'
	os.system(command)

	#Email login information
	## Enter your user name and 
	smtpUser = "pchan3113@gmail.com"
	smtpPass = 'A1zxcvbnm'

	#Destination email information
	toAdd = ['ENPM809TS19@gmail.com','pvcharankarthikeyan@gmail.com']
	fromAdd = smtpUser
	subject = "Image recorded at" +pic_time
	msg = MIMEMultipart()
	msg['Subject'] = subject
	msg["From"] = fromAdd
	#msg["To"] = toAdd
	msg["To"] = ",".join(toAdd)
	msg.preamble = "Image recorded at" + pic_time

	#Email Text
	coor_x = str(coord_x)
	coor_y = str(coord_y)
	body = MIMEText("Image recorded at"+pic_time+" "+str(coor_x)+" "+str(coor_y))
	msg.attach(body)

	#Attach image
	fp = open(pic_time+'.jpg','rb')
	img = MIMEImage(fp.read())
	fp.close()
	msg.attach(img)

	s = smtplib.SMTP("smtp.gmail.com",587)

	s.ehlo()
	s.starttls()
	s.ehlo()

	s.login(smtpUser,smtpPass)
	s.sendmail(fromAdd,toAdd,msg.as_string())
	s.quit()

	print("The Email has been Delivered")