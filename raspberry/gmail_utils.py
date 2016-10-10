import smtplib, sys, logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

logger = logging.getLogger('gmail_utils')

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
            logger.debug(text);
        else:
            server.sendmail(fromAddr, toAddrs, text)		
        server.close()
        return True
    except Exception as err:  
        logger.critical ("Failed to send email: {0}".format(err))
        return False
		
