import telebot
from BotCommands import *

bot = telebot.TeleBot(tiket)


@bot.message_handler(commands=['reg'])
def get_info(message):
    name = '';
    surname = '';
    age = 0;
    bot.send_message(message.from_user.id, "Как тебя зовут?");
    bot.register_next_step_handler(message, get_name); #следующий шаг – функция get_name

def get_name(message): #получаем фамилию
    name = message.text;
    print(name)
    bot.send_message(message.from_user.id, 'Какая у тебя фамилия?');
    bot.register_next_step_handler(message, get_surnme);

def get_surname(message):
    surname = message.text;
    print(surname)
    bot.send_message('Сколько тебе лет?');
    bot.register_next_step_handler(message, get_age);

def get_age(message):
    while age == 0: #проверяем что возраст изменился
        try:
             age = int(message.text) #проверяем, что возраст введен корректно
        except Exception:
             bot.send_message(message.from_user.id, 'Цифрами, пожалуйста');
        bot.send_message(message.from_user.id, 'Спасибо '+name+ + '!')

@bot.message_handler(commands=['help'])  
def help_command(message):   
    bot.send_message(  
        message.chat.id,  
        'Привет, я тебе помогу разобаться с основными командами\n'+
        'Я сделан для того, чтобы '
    )


@bot.message_handler(commands=['start'])  
def start_command(message):
    keyboard = telebot.types.InlineKeyboardMarkup()  
    keyboard.row(  
        telebot.types.InlineKeyboardButton('Войти', callback_data='get-in')  
    )  
    keyboard.row(  
        telebot.types.InlineKeyboardButton('Зарегистрироваться', callback_data='get-reg')  
    )  
    bot.send_message(  
        message.chat.id, 
        'Приветствую, мы собираем статистику,\n' +  
        'Я помогу тебе с выбором преметов в этом семестре\n' +  
        'Если тебе нужно узнать обо мне подробнее? - /help.' +  
        'Click on the currency of choice:',  
        reply_markup=keyboard  
    )


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes": #call.data это callback_data, которую мы указали при объявлении кнопки
        bot.send_message(call.message.chat.id, 'Запомню : )');
    elif call.data == "get-reg":
        get_info(command = ['reg'] )


bot.polling(none_stop=True, interval= 3) 


def main():
    LOGGER.log('bot is running...')
    bot.infinity_polling()

if __name__ == '__main__':  
    try:
        main()
    except KeyboardInterrupt:
        exit()