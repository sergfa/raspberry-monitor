

class Beacon:
    def __init__(self, metric_key, metric_type, metric_value, timestamp):
         self._key = metric_key     
         self._type = metric_type
         self._value = metric_value
         self._timestamp = timestamp
     
    @property
    def key(self):
        return self._key
        
    
    @property
    def type(self):
        return self._type
    
    @property
    def value(self):
        return self._value
    
    @property
    def timestamp(self):
        return self._timestamp
    
        
    def KEY_CPU_TEMPERATURE():
        return "RpiCpuTemperature"
    
    def KEY_GPU_TEMPERATURE():
        return "RpiGpuTemperature"
        
    def KEY_PRESENSE(id):
        return "DevicePresense" + id
    
    def KEY_PUBLIC_IP():
        return "RpiPublicIp"
    
    def KEY_SENSE_HAT_TEMP():
        return "SenseHatTemperature"
    
    def KEY_SENSE_HAT_PRESSURE():
        return "SenseHatPressure"
    
    def KEY_SENSE_HAT_HUMIDITY():
        return "SenseHatHumidity"
        
    def TYPE_TEMPERATURE():
        return "TEMPERATURE_MONITOR"

    def TYPE_PUBLIC_IP():
        return "IP_MONITOR"
    
    def TYPE_PRESENSE():
        return "PRESENCE_MONITOR"
   
    def TYPE_SENSE_HAT():
        return "SENSE_HAT"
      
        
    