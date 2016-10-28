

class Beacon:
    def __init__(self, metric_type, metric_value, timestamp):
         self._type = metric_type
         self._value = metric_value
         self._timestamp = timestamp
     
       
    @property
    def type(self):
        return self._type
    
    @property
    def value(self):
        return self._value
    
    @property
    def timestamp(self):
        return self._timestamp
        
    def TYPE_CPU_TEMPERATURE():
        return "rpi-cpu-temperature"
    
    def TYPE_GPU_TEMPERATURE():
        return "rpi-gpu-temperature"
        
    def TYPE_PUBLIC_IP():
        return "rpi-public-ip"
    
    def TYPE_PRESENSE(id):
        return "device-presense-" + id
        
    