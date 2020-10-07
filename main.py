import telebot
#import config

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
    keyboard = telebot.types.InlineKeyboardMarkup()  
    keyboard.add(  
        telebot.types.InlineKeyboardButton(  
            'Message the developer', url='telegram.me/artiomtb'  
  )  
    )  
    bot.send_message(  
        message.chat.id,  
        '1) To receive a list of available currencies press /exchange.\n' +  
        '2) Click on the currency you are interested in.\n' +  
        '3) You will receive a message containing information regarding the source and the target currencies, ' +  
        'buying rates and selling rates.\n' +  
        '4) Click “Update” to receive the current information regarding the request. ' +  
        'The bot will also show the difference between the previous and the current exchange rates.\n' +  
        '5) The bot supports inline. Type @<botusername> in any chat and the first letters of a currency.',  
        reply_markup=keyboard  
    )