import  time, logging
from raspberry.beacon import Beacon
from sense_hat import SenseHat
from threading import Thread


class SenseHatMonitor:
    
    logger = logging.getLogger('sense_hat_monitor')

    def __init__(self, beaconQueue, checkInterval):
        self._beaconQueue = beaconQueue
        self._interval = checkInterval
    
    def start_monitor(self):
       def do_monitor():
           sense = SenseHat()
           while True:
               t = round(sense.get_temperature(),1)
               p = round(sense.get_pressure(), 1)
               h = round(sense.get_humidity(), 1)
               t_beacon = Beacon(Beacon.KEY_SENSE_HAT_TEMP(),Beacon.TYPE_SENSE_HAT(), t, time.time())
               p_beacon = Beacon(Beacon.KEY_SENSE_HAT_PRESSURE(),Beacon.TYPE_SENSE_HAT(), p, time.time())
               h_beacon = Beacon(Beacon.KEY_SENSE_HAT_HUMIDITY(),Beacon.TYPE_SENSE_HAT(), h, time.time())
               print("{0}={1}".format(t_beacon.key, t_beacon.value))
               self._beaconQueue.put(t_beacon)
               self._beaconQueue.put(p_beacon)
               self._beaconQueue.put(h_beacon)
               time.sleep(self._interval)
       sense_thread = Thread(name='check_sense_hat', target=do_monitor)
       sense_thread.daemon = True
       sense_thread.start()
   
def test():
    import queue
    beaconQueue = queue.Queue()
    monitor = SenseHatMonitor(beaconQueue, 30)
    monitor.start_monitor()
    while True:
        time.sleep(100)
    