import smtplib

def sendEmail(fromAddr, toAddrs, key, text):
    try:  
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(fromAddr, key)
        server.sendmail(fromAddr, toAddrs, text)
        server.close()
        return True
    except:  
        return False
		
