import subprocess, sys, socket, os, logging

logger = logging.getLogger('ip_utils')

def checkIp(ip):
    socket.inet_aton(ip)         

def getPublicIP():
    output = subprocess.check_output("curl -s https://api.ipify.org/?format=text; echo", shell=True).decode("ascii");
    logger.debug("Get output from https://api.ipify.org : " + output)    
    try:
        checkIp(output)
    except:
        logger.debug("Failed to parse output from  https://api.ipify.org : " + output)
        output = subprocess.check_output("curl -s http://ipecho.net/plain; echo", shell=True).decode("ascii");
        logger.debug("Get output from http://ipecho.net : " + output)
        checkIp(output)
    return output;


