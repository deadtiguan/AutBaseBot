from pymongo import MongoClient
import telebot
import time
from telebot import types
from telebot import apihelper
import os


MONGO_DB = "tgbot"
Access_chat = [-1001303494318, -281779600]


try:
    TOKEN = os.environ['token']
    MONGO_LINK = os.environ['mongo_link']
except:
    from variables import *


mdb = MongoClient(MONGO_LINK)[MONGO_DB]
def addtobase()




bot = telebot.TeleBot(TOKEN)


#apihelper.proxy = {'http': 'http://46.235.53.26:3128'}


def access_handler(message):
    if message.chat.id in Access_chat:
        return True
    elif message.chat.type in ["group", "supergroup"]:
        bot.send_message(message.chat.id, "Чат не подтвержден. Ливаю..")
        bot.leave_chat(message.chat.id)
        return False
    else:
        return False


def access_member(message):
        if not bot.get_chat_member(message.chat.id, message.from_user.id).status in ['creator', 'administrator']:
            bot.delete_message(message.chat.id, message.message_id)
            return False
        else:
            return True


@bot.message_handler(commands=['start', 'help'])
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


@bot.inline_handler(lambda query: query.query == '')
def query_text(inline_query):
    try:
        shrug = types.InlineQueryResultArticle('1', 'Shrug', types.InputTextMessageContent('¯\_(ツ)_/¯'))
        bot.answer_inline_query(inline_query.id, [shrug])
    except Exception as e:
        print(e)


@bot.message_handler(commands=['kick'], func=access_member)
def kick_handler(message):
    if message.reply_to_message:
        if bot.get_chat_member(message.chat.id, message.reply_to_message.from_user.id).status \
                       in ['creator', 'administrator']:
            bot.reply_to(message, "Это админ!")
        else:
            bot.kick_chat_member(message.chat.id, message.reply_to_message.from_user.id)
            bot.unban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
            bot.reply_to(message, "Выполнено!")
    else:
        bot.reply_to(message, "Нужно присылать в ответ на сообщение юзера!")


@bot.message_handler(commands=['mute'], func=access_member)
def mute_handler(message):
    if message.reply_to_message:
        if bot.get_chat_member(message.chat.id, message.reply_to_message.from_user.id).status \
                       in ['creator', 'administrator']:
            bot.reply_to(message, "Это админ!")
        else:
            try:
                time_mute = ''
                unit = "5 минут"
                for i in message.text.split(maxsplit=2)[1]:
                    if i.isdigit():
                        time_mute += i
                    if i.isspace():
                        pass
                for i in ['м', 'm']:
                    if i in message.text.split(maxsplit=2)[1]:
                         unit = time_mute + ' minutes'
                         time_mute = int(time_mute) * 60

                for i in ['h', 'ч']:
                    if i in message.text.split(maxsplit=2)[1]:
                        if int(time_mute) <= 1:
                            unit = time_mute + ' hour'
                        else:
                            unit = time_mute + ' hours'
                        time_mute = int(time_mute) * 60 * 60
                for i in ['d', 'д']:
                    if i in message.text.split( maxsplit=2)[1]:
                        if int(time_mute) <= 1:
                            unit = time_mute + ' day'
                        else:
                            unit = time_mute + ' days'
                        time_mute = int(time_mute) * 60 * 24
                else:
                    unit = time_mute + " секунд"
            except:
                time_mute = '300'
            bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id,
                                 until_date=time.time() + int(time_mute),
                                 can_send_messages=False)
            if len(message.text.split()) > 2:
                comment = "\nПричина:\n "+message.text.split(maxsplit=2)[2]
            else:
                comment = ''
            bot.reply_to(message, "Выполнено! Мут на " + unit + comment)
    else:
        bot.reply_to(message, "Нужно присылать в ответ на сообщение юзера в формате: \n /mute {время}{m/d/h} {причина}")


@bot.message_handler(commands=['um', 'un', 'unmute', 'unban'], func=access_member)
def unmute_handler(message):
    if bot.get_chat_member(message.chat.id, message.reply_to_message.from_user.id).status \
            in ['creator', 'administrator']:
        bot.reply_to(message, "Это админ!")
    elif message.reply_to_message:
        bot.promote_chat_member(message.chat.id, message.reply_to_message.from_user.id)
        bot.reply_to(message, "Выполнено! Снял ограничения.")
    else:
        bot.reply_to(message, "Нужно присылать в ответ на сообщение юзера!")


@bot.message_handler(commands=['setwelcome'], func=access_member)
def setwelcome_handler(message):
    id_from_who = message.from_user.id
    x = [bot.reply_to(message, "Напиши мне текст приветствия в отдельном сообщении."), message.message_id]

    bot.register_next_step_handler(message, newwelcome, id_from_who, x)



def newwelcome(message, id_from_who, x):
    if id_from_who == message.from_user.id:
        new_welcome = message.text
        file = open('welcome.txt', 'w')
        file.write(new_welcome)
        file.close()
        bot.send_message(message.chat.id, "Текущее приветствие теперь:\n" + new_welcome)
        bot.delete_message(message.chat.id, message.message_id)
        bot.delete_message(message.chat.id, x[0].message_id)
        bot.delete_message(message.chat.id, x[1])

    else:
        bot.register_next_step_handler(message, newwelcome, id_from_who)


@bot.message_handler(func=lambda m: str(m.text).lower().startswith("#help") or str(m.text).lower().startswith("#start"))
def start_mes_alt(message):
    start_mes(message)


@bot.message_handler(func=access_handler, content_types=['new_chat_members'])
def hello_handler(message):
    try:
        bot.reply_to(message, open("welcome.txt", "r").read())
    except:
        bot.reply_to(message, "Заглушка")


@bot.message_handler(content_types=['left_chat_member'])
def leave_member_handler(message):
    bot.reply_to(message, "Земля ему пухом")


@bot.message_handler(content_types=['text'])
def zahochesh(message):
    if "не хочу" in message.text.lower():
        bot.reply_to(message, "Захочешь")
    elif "не дрочи на ближнего своего" in message.text.lower():
        bot.reply_to(message, "Аминь.")
    else:
        pass


bot.polling(none_stop=True)
