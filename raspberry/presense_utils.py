import  subprocess, sys, os, socket

def readPresenseData():
    data = {}
    output = subprocess.check_output("sudo arp-scan -l", shell=True).decode("ascii");
    lines = output.split('\n')
    for line in lines:
        line = line.rstrip()
        device = line.split(None, 2);
        print(device)		
        if(len(device) == 3 and checkIp(device[0])):
            data[device[1]] = device[0]		
    return data;

def loadInitialPresenses():
    data = {}
    presenseFilename = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../env', 'presense.txt')
    with open(presenseFilename, "r") as lines:
        for line in lines:
            line = line.rstrip()
            person = line.split(None, 1);
            data[person[0]] = [person[1], -1]		
    return data

def checkIp(ip):
    try:
         socket.inet_aton(ip)
         return True
    except:
       	return False