from raspberry.gmail_utils import sendEmail
from threading import Thread
from raspberry.telegram_utils import is_logged_in
from raspberry.presence_utils import loadInitialPresences
from raspberry.presence_utils import monitor_device_state
from raspberry.presence_utils import arp_scan
import logging

presence_data = None
logger = logging.getLogger('presence')

def bot_get_presence(bot, update):
    if(is_logged_in(bot, update) == False):
        return
    try:
        msg = "Devices status:\n\n"
        for presence in presence_data:
            device_status = presence_data[presence]["device"] + ": " + presence_data[presence]["status"]
            msg = msg + device_status + "\n"
        bot.sendMessage(chat_id=update.message.chat_id, text=msg)
    except Exception as err:
         logger.critical("Failed to get presence data: {0}".format(err))


def start_presence_monitor(timeout, config):
    
    from threading import Thread
    global presence_data
    presence_data = loadInitialPresences()
    
    monitor_device_state_thread = Thread(name='monitor_device_state', target=monitor_device_state, kwargs={"presence_data" : presence_data, "timeout":timeout, "config": config})
    monitor_device_state_thread.daemon = True
    monitor_device_state_thread.start()
    
    arp_scan_thread = Thread(name='arp_scan', target=arp_scan, kwargs={'presence_data': presence_data})
    arp_scan_thread.daemon = True
    arp_scan_thread.start()	