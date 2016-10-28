

class Beacon:
    def __init__(self, metric_type, metric_value, timestamp):
         self.metric_type = metric_type
         self.metric_value = metric_value
         self.timestamp = timestamp
     
       
    @property
    def type(self):
        return self.metric_type
    
    @property
    def value(self):
        return self.metric_value
    
    @property
    def timestamp(self):
        return self.timestamp
        
    def TYPE_CPU_TEMPERATURE():
        return "rpi-cpu-temperature"
    
    def TYPE_GPU_TEMPERATURE():
        return "rpi-gpu-temperature"
        
    def TYPE_PUBLIC_IP():
        return "rpi-public-ip"
    
    def TYPE_PRESENSE(id):
        return "device-presense-" + id
        
    