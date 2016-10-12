#!/usr/bin/env python3
from raspberry.telegram_utils import telegram_bot
from raspberry.telegram_utils import is_logged_in
from raspberry.ip_utils import is_connected
from raspberry.temperature import bot_get_temperature
from raspberry.temperature import checkTemp
from raspberry.ip import checkIP
from raspberry.ip import bot_get_ip
from raspberry.presence import bot_get_presence
from raspberry.presence import start_presence_monitor



from threading import Thread
import os, sys, configparser, time, logging


config = configparser.ConfigParser()
config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'env', 'config.cfg'))

logFileName =  os.path.join(os.path.abspath(os.path.dirname(__file__)), 'logs', 'rpi_monitor.log')
loggingLevel =  config.get('env', 'loggingLevel')
logging.basicConfig(filename=logFileName,level=loggingLevel, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')

logger = logging.getLogger('rpi-monitor')


telegram_token = config.get('TELEGRAM', 'bot-token')
telegram_bot_password = config.get('TELEGRAM', 'bot-password')

def exit_clean(signal=None, frame=None):
    logger.info("RPI monitoring stopping...")
    sys.exit(0)      
        

def bot_help(bot, update):
    if(is_logged_in(bot, update) == False):
        return
    msg = "Use commands /ip, /temperature, /presense to recieve information from the Bot"
    bot.sendMessage(chat_id=update.message.chat_id, text=msg)
    

def main():	
    bot_commands = [("presence", bot_get_presence, False), ("ip", bot_get_ip, False),("temperature", bot_get_temperature, False),("help", bot_help, False)]
    telegram_bot_thread = Thread(name='telegram_bot', target=telegram_bot, kwargs={'token': telegram_token, 'commands': bot_commands, 'passw' : telegram_bot_password})
    telegram_bot_thread.daemon =  True
    telegram_bot_thread.start()
    
    if (config.getint('TEMPERATURE_MONITOR', 'enable') == 1):
        monitor_temp_thread = Thread(name='monitor_temp', target=checkTemp, kwargs={'config': config})
        monitor_temp_thread.daemon = True
        monitor_temp_thread.start()
    
    if (config.getint('IP_MONITOR', 'enable') == 1):
        monitor_ip_thread = Thread(name='monitor_ip', target=checkIP, kwargs={'config': config})
        monitor_ip_thread.daemon = True
        monitor_ip_thread.start()
    
    start_presence_monitor(config.getint('PRESENCE_MONITOR', 'device_disconnected_time'))
    
try:
    logger.info("RPI monitoring is starting...")
    #check if network is up, otherwise sleep a bit and check it again
    while (is_connected() == False):
        time.sleep(60)
    main()
    logger.info("RPI monitoring is started")
    while True:
            time.sleep(100)
except KeyboardInterrupt:
    exit_clean()
		
