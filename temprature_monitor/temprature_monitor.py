from raspberry.gmail_utils import sendEmail
import ConfigParser

config = ConfigParser.ConfigParser()
config.read('env/config.cfg')
gmailFromAddr = config.get('gmail', 'fromAddrs')
gmailPassword= config.get('gmail', 'password')
gmailToAddr = config.get('gmail', 'toAddrs')
appMode = config.get('env', 'mode')


def sendTemprature(temprature):
    return sendEmail(gmailFromAddr, gmailToAddr, gmailPassword , "Hello, Please note , the temprature of your Raspberry is " + \
    str( temprature), appMode == "dev")
   

sent = sendTemprature(85);
msg =  "Email was sent" if sent else "Failed to sent email"	
print(msg)
	
	