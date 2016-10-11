import os, sys, time, logging, telegram

logger = logging.getLogger('telegram_utils')

logins = dict()
    
def telegram_bot(token, commands, passw):
    from telegram.ext import Updater
    from telegram.ext import CommandHandler
    from telegram.ext import MessageHandler, Filters, RegexHandler, Job
    

    	
    updater = Updater(token=token)
    dispatcher = updater.dispatcher
    
    def logout_timeout(bot, job):
        if(job.context in logins):
            del logins[job.context]
            bot.sendMessage(job.context, text='Session timeout')
            
    def login(bot, update, args, job_queue):
        if(len(args) < 1):
            update.message.reply_text('Password is missing, use command /login <password>')
            return
        if(passw != args[0]):
            update.message.reply_text('Password is incorrect.')
            return   
        chat_id = update.message.chat_id
        logins[chat_id] = True
        # Add job to session timeout (1 hour) queue
        job = Job(logout_timeout, 3600, repeat=False, context=chat_id)
        job_queue.put(job)
        update.message.reply_text('Hi there! You are logged in')

    def logout(bot, update):
        chat_id = update.message.chat_id
        if(chat_id in logins):
            del logins[chat_id]
        update.message.reply_text('Hi there! You are logged out')
    
    def start(bot, update):
        update.message.reply_text('Hi! This is a private bot, you must have password to use it. Use /login <password> to log in.')
    
    #add error handler
    def error(bot, update, error):
        logger.error('Update "%s" caused error "%s"' % (update, error))
        dispatcher.add_error_handler(error)
    
    
    #add all other commands
    for command in commands:
        #name, callback, pass_args
        command_handler = CommandHandler(command[0], command[1],pass_args = command[2])
        dispatcher.add_handler(command_handler)
    
    
    
    dispatcher.add_handler(CommandHandler("login", login, pass_args = True, pass_job_queue = True))
    dispatcher.add_handler(CommandHandler("logout", logout))
    dispatcher.add_handler(CommandHandler("start", start))
    
    
    #add unknown handler , must be added last
    def unknown(bot, update):
        bot.sendMessage(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")
        unknown_handler = MessageHandler([Filters.command], unknown)
        dispatcher.add_handler(unknown_handler)
    

    updater.start_polling()
 
def is_logged_in(bot, update):
    chat_id=update.message.chat_id
    logged_in = chat_id in logins
    if(logged_in == False):
        update.message.reply_text('Sorry I cannot respond to this command beacuse you are not logged in, use command /login <password>')
    return logged_in
