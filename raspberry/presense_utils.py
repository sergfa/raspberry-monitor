import  subprocess, sys, os, socket, time


def loadInitialPresenses():
    data = {}
    presenseFilename = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../env', 'presense.txt')
    with open(presenseFilename, "r") as lines:
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




def monitor_device_state(presense_data, timeout):
    def update_device_state(presense, new_state):
        if(presense['status'] != new_state):
            presense['status'] = new_state

    while True:
        time.sleep(3)
        now = time.time()
        for mac_address in presense_data:
            if now - presense_data[mac_address]['last_seen'] > timeout:
                update_device_state(presense_data[mac_address], 'offline')
            else:
                update_device_state(presense_data[mac_address], 'online')

     
def arp_scan(presense_data):
    def readPresenseData():
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
        time.sleep(5)
        onlineDevices = readPresenseData()
        now = time.time()
        for device_mac in onlineDevices:
            if(device_mac in presense_data):
                presense_data[device_mac]["last_seen"] = now 
