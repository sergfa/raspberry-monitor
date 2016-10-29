from raspberry.openhab_rest import OpenhabRestHelper
from raspberry.beacon import Beacon

class OpenhabSender:
    
    def __init__(self, config):
       self._config = config
     
    def send(self, beacon):
        config = self._config
        openhabHelper = OpenhabRestHelper(config.get("OPENHAB","host"), config.get("OPENHAB","port"), config.get("OPENHAB","username"), config.get("OPENHAB","password"))
            
        if(beacon.key == Beacon.KEY_CPU_TEMPERATURE()):
            openhabHelper.put_status(beacon.key, beacon.value)
        elif(beacon.key == Beacon.KEY_GPU_TEMPERATURE()):
           openhabHelper.put_status(beacon.key, beacon.value)
        elif(beacon.key == Beacon.KEY_PUBLIC_IP()):
           openhabHelper.put_status(beacon.key, beacon.value)
        elif(beacon.key == Beacon.KEY_PRESENSE()):
           openhabHelper.post_status(beacon.key, beacon.value == "online")
       
               
        