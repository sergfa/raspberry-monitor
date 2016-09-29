import subprocess

def getCpuTemperature():
    f = open("/sys/class/thermal/thermal_zone0/temp");
    line = f.readline();
    f.close();
    temprature = float(line)/1000;
    return temprature;


def getGpuTemperature():
    output = subprocess.check_output("/opt/vc/bin/vcgencmd measure_temp", shell=True).decode("ascii");
    temprature = float(output[5:-3]);
    return temprature;
