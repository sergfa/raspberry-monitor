import  subprocess, sys, os, socket, time


def loadInitialPresences():
    data = {}
    presenceFilename = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../env', 'presence.txt')
    with open(presenceFilename, "r") as lines:
        for line in lines:
            line = line.rstrip()
            person = line.split(None, 1);
            data[person[0]] = {"device" : person[1], "status": "unknown", "last_seen": 0}		
    return data

def checkIp(ip):
    try:
         socket.inet_aton(ip)
         return True
    except:
       	return False




def monitor_device_state(presence_data, timeout):
    def update_device_state(presense, new_state):
        if(presense['status'] != new_state):
            presense['status'] = new_state

    while True:
        time.sleep(30)
        now = time.time()
        for mac_address in presence_data:
            if now - presence_data[mac_address]['last_seen'] > timeout:
                update_device_state(presence_data[mac_address], 'offline')
            else:
                update_device_state(presence_data[mac_address], 'online')

     
def arp_scan(presence_data):
    def readPresenceData():
        data = {}
        output = subprocess.check_output("sudo arp-scan -l", shell=True).decode("ascii");
        lines = output.split('\n')
        for line in lines:
            line = line.rstrip()
            device = line.split(None, 2);
            if(len(device) == 3 and checkIp(device[0])):
                data[device[1]] = device[0]		
        return data;
	
    while True:
        time.sleep(45)
        onlineDevices = readPresenceData()
        now = time.time()
        for device_mac in onlineDevices:
            if(device_mac in presence_data):
                presence_data[device_mac]["last_seen"] = now 
