import smtplib, sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def sendEmail(fromAddr, toAddrs, key, body, subject, skipSend):
    msg = MIMEMultipart()
    msg['From'] = fromAddr
    msg['To'] = toAddrs
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    text = msg.as_string()
   
    try:  
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(fromAddr, key)
        if(skipSend):
            print(text);
        else:
            server.sendmail(fromAddr, toAddrs, text)		
        server.close()
        return True
    except:  
        print ("Unexpected error:", sys.exc_info()[0])
        return False
		
