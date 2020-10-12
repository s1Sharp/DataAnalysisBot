import telebot
#import config

"""
    комментарий
"""

bot = telebot.TeleBot('1027337352:AAHfDMuVygTgw39-oU1YVsFkSz3PJL6GSOA')


@bot.message_handler(commands=['start'])  
def start_command(message):  
    bot.send_message(  
        message.chat.id,  
        'Приветствую, мы собираем статистику,\n' +  
        'Я помогу тебе с выбором преметов в этом семестре\n' +  
        'Если тебе нужно узнать обо мне подробнее? - /help.'  )

#bot.polling(none_stop=True, interval=5) 
bot.polling(none_stop=True, interval= 3) 

@bot.message_handler(commands=['help'])  
def help_command(message):   
    bot.send_message(  
        message.chat.id,  'help here'
    )
