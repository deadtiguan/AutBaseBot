from variables import *
import telebot
import time
from telebot import apihelper

bot = telebot.TeleBot(TOKEN)


def access_handler(message):
    if message.chat.id in Access_chat:
        return True
    else:
        bot.send_message(message.chat.id, message.chat.id)
        bot.send_message(message.chat.id, "Чат не подтвержден. Ливаю..")
        bot.leave_chat(message.chat.id)
        return False


@bot.message_handler(commands=['start'])
def start_mes(message):
    if message.chat.type == "private":
        bot.send_message(message.chat.id, "Да, привет")
    elif message.chat.type in ["group", "supergroup"]:
        bot.reply_to(message, "Ответ бота, если написано в группе.")


@bot.message_handler(commands=['ping'])
def ping_handler(message):
    bot.reply_to(message, "Pong")


@bot.message_handler(commands=['chatid'])
def ping_handler(message):
    bot.reply_to(message, message.chat.id)


@bot.message_handler(content_types=['text'])
def zahochesh(message):
    if "не хочу" in message.text.lower():
        bot.reply_to(message, "Захочешь")
    else:
        pass


@bot.message_handler(commands=['kick'])
def kick_handler(message):
    id_chat = message.chat.id
    from_why = message.from_user.id
    user_admin = bot.get_chat_member(id_chat, from_why).status in ['creator', 'administrator']
    user_reply_admin = bot.get_chat_member(id_chat, message.reply_to_message.from_user.id).status \
                         in ['creator', 'administrator']

    if not user_admin:
        bot.reply_to(message, "Ты не админ, УхАди!")
    elif user_reply_admin:
        bot.reply_to(message, "Это админ!")
    else:
        bot.kick_chat_member(id_chat, message.reply_to_message.from_user.id)
        bot.unban_chat_member(id_chat, message.reply_to_message.from_user.id)
        bot.reply_to(message, "Выполнено!")

    # if bot.get_chat_member(id_chat, message.reply_to_message.from_user.id).status in ['creator', 'administrator']:
    #     bot.reply_to(message, "Это админ, не трож")
    # elif bot.get_chat_member(id_chat, from_why).status in ['creator', 'administrator']:
    #     bot.kick_chat_member(id_chat, message.reply_to_message.from_user.id)
    #     bot.unban_chat_member(id_chat, message.reply_to_message.from_user.id)
    #     bot.reply_to(message, "Выполнено!")
    # else:
    #     bot.reply_to(message, "Идешь нахуй")


# @bot.message_handler(commands=['mute'])
# def mute_handler(message):
#     id_chat = message.chat.id
#     from_why = message.from_user.id
#
#     if bot.get_chat_member(id_chat, message.reply_to_message.from_user.id).status in ['creator', 'administrator']:
#         bot.reply_to(message, "Это админ, не трож")
#     elif bot.get_chat_member(id_chat, from_why).status in ['creator', 'administrator']:
#        bot.restrict_chat_member(id_chat, message.reply_to_message.from_user.id, until_date=time.time() + 60,
#                                  can_send_messages=False)
#     else:
#         bot.reply_to(message, "Идешь нахуй")


@bot.message_handler(commands=['setwelcome'])
def setwelcome_handler(message):
    new_welcome = message.text[11:]
    file = open('welcome.txt', 'w')
    file.write(new_welcome)
    file.close()
    bot.send_message(message.chat.id, "Текущее приветствие теперь:\n" + new_welcome)


@bot.message_handler(func=access_handler, content_types=['new_chat_members'])
def hello_handler(message):
    try:
        bot.reply_to(message, open("welcome.txt", "r").read())
    except:
        bot.reply_to(message, "Заглушка")


bot.polling(none_stop=True)
