from raspberry.gmail_utils import sendEmail
from threading import Thread
from raspberry.telegram_utils import is_logged_in
from raspberry.presense_utils import loadInitialPresenses
from raspberry.presense_utils import monitor_device_state
from raspberry.presense_utils import arp_scan
import logging

presense_data = None
logger = logging.getLogger('presense')

def bot_get_presense(bot, update):
    if(is_logged_in(bot, update) == False):
        return
    try:
        msg = "Presense status:\n\n"
        for presense in presense_data:
            device_status = presense_data[presense]["device"] + ": " + presense_data[presense]["status"]
            msg = msg + device_status + "\n"
        bot.sendMessage(chat_id=update.message.chat_id, text=msg)
    except Exception as err:
         logger.critical("Failed to get presense data: {0}".format(err))


def start_presense_monitor(timeout):
    
    from threading import Thread
    global presense_data
    presense_data = loadInitialPresenses()
    
    monitor_device_state_thread = Thread(name='monitor_device_state', target=monitor_device_state, kwargs={"presense_data" : presense_data, "timeout":timeout})
    #monitor_device_state_thread.daemon = True
    monitor_device_state_thread.start()
    
    arp_scan_thread = Thread(name='arp_scan', target=arp_scan, kwargs={'presense_data': presense_data})
    #arp_scan_thread.daemon = True
    arp_scan_thread.start()	