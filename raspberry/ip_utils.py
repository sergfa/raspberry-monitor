import subprocess, sys, socket, os, logging

logFileName =  os.path.join(os.path.abspath(os.path.dirname(__file__)), '../logs', 'ip.log')
loggingLevel =  "DEBUG"
logging.basicConfig(filename=logFileName,level=loggingLevel, format='%(asctime)s %(message)s')

def checkIp(ip):
    socket.inet_aton(ip)         

def getPublicIP():
    output = subprocess.check_output("curl -s https://api.ipify.org/?format=text; echo", shell=True).decode("ascii");
    logging.debug("Get output from https://api.ipify.org : " + output)    
    try:
        checkIp(output)
    except:
        logging.debug("Failed to parse output from  https://api.ipify.org : " + output)
        output = subprocess.check_output("curl -s http://ipecho.net/plain; echo", shell=True).decode("ascii");
        logging.debug("Get output from http://ipecho.net : " + output)
        checkIp(output)
    return output;


