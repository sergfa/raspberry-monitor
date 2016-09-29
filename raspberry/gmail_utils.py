import smtplib

def sendEmail(fromAddr, toAddrs, key, text, skipSend):
    try:  
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(fromAddr, key)
        if(skipSend):
		    print("Sending email from " + fromAddr + " to " + toAddrs + " Text: " + text);
        else:
            server.sendmail(fromAddr, toAddrs, text)		
        server.close()
        return True
    except:  
        return False
		
