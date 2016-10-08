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
    """
    This function monitors and updates the alarm state based on data from Telegram and the alarm_state dictionary.
    """
    while True:
        time.sleep(3)
        now = time.time()
        for mac_address in presense_data:
            if now - presense_data[mac_address]['last_seen'] > timeout:
                update_device_state(presense_data[mac_address], 'offline')
            else:
                update_device_state(presense_data[mac_address], 'online')

def update_device_state(presense, new_state):
    if(presense['status'] != new_state):
        presense['status'] = new_state
        print("The state of " + presense['device'] + " is changed to " + new_state)

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
		
def start_monitor(timeout):
    
    from threading import Thread
    presense_data = loadInitialPresenses()
    
    monitor_device_state_thread = Thread(name='monitor_device_state', target=monitor_device_state, kwargs={"presense_data" : presense_data, "timeout":timeout})
    #monitor_device_state_thread.daemon = True
    monitor_device_state_thread.start()
    
    arp_scan_thread = Thread(name='arp_scan', target=arp_scan, kwargs={'presense_data': presense_data})
    #arp_scan_thread.daemon = True
    arp_scan_thread.start()	