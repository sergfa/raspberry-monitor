import os, sys, time, logging



def telegram_bot(token, logLevel, commands, logFileName):
    from telegram.ext import Updater
    from telegram.ext import CommandHandler
    from telegram.ext import MessageHandler, Filters
    
    logging.basicConfig(filename=logFileName,level=logLevel, format='%(asctime)s %(message)s')

    	
    updater = Updater(token=token)
    dispatcher = updater.dispatcher
    
    #def start(bot, update):
    #    bot.sendMessage(chat_id=update.message.chat_id, text="Hi from a bot(/start)!")

    #add error handler
    def error(bot, update, error):
        logging.error('Update "%s" caused error "%s"' % (update, error))
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