import subprocess

def getPublicIP():
    output = subprocess.check_output("curl http://ipecho.net/plain; echo", shell=True).decode("ascii");
    return output;
