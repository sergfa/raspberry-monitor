import os, sys, time, logging, telegram

state ={"status": "started", "chat_id" : None}
logger = logging.getLogger('telegram_utils')

def telegram_bot(token, commands):
    from telegram.ext import Updater
    from telegram.ext import CommandHandler
    from telegram.ext import MessageHandler, Filters, RegexHandler
    

    	
    updater = Updater(token=token)
    dispatcher = updater.dispatcher
    
    def save_chat_id(bot, update):
        state["chat_id"] = update.message.chat_id
        
        if(state["status"] == "started"):
            state["status"] = "enabled"
        
    dispatcher.add_handler(RegexHandler('.*', save_chat_id), group=1)
    
    def enable(bot, update):
        state["status"] = "enabled"
        bot.sendMessage(chat_id=update.message.chat_id, text="Bot is enabled")

    dispatcher.add_handler(CommandHandler("enable",enable))
    
    def disable(bot, update):
        state["status"] = "disabled"
        bot.sendMessage(chat_id=update.message.chat_id, text="Bot is disabled")

    dispatcher.add_handler(CommandHandler("disable",disable))
    
    def status(bot, update):
        bot.sendMessage(chat_id=update.message.chat_id, text="Bot status is " + state["status"])

    dispatcher.add_handler(CommandHandler("status", status))
    
    #add error handler
    def error(bot, update, error):
        logger.error('Update "%s" caused error "%s"' % (update, error))
        dispatcher.add_error_handler(error)
    
    
    #add all other commands
    for command in commands:
        #name, callback, pass_args
        command_handler = CommandHandler(command[0], command[1],pass_args = command[2])
        dispatcher.add_handler(command_handler)
    
    #add unknown handler , must be added last
    def unknown(bot, update):
        bot.sendMessage(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")
        unknown_handler = MessageHandler([Filters.command], unknown)
        dispatcher.add_handler(unknown_handler)
    

    updater.start_polling()
 
def get_telegram_state():
    return state; 
    
def telegram_send_message(message, telegram_token):
    
    if(state["status"] != "enabled"):
        logger.info('Cannot send message: "%s" because bot is not enabled' % message)
        return False
        
    try:
        bot = telegram.Bot(token=telegram_token)
        bot.sendMessage(chat_id=state["chat_id"], parse_mode='Markdown', text=message, timeout=10)
    except Exception as e:
        logger.error('Telegram message failed to send message "%s" with exception: %s' % (message, e))
    else:
        logger.debug('Telegram message Sent: "%s"' % message)
        return True
 
