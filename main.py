import os
import telebot
from telebot import types
from dotenv import load_dotenv
from quests import *

load_dotenv()
token = os.getenv('TOKEN')
if not token:
    raise Exception('Не задана переменная окружения TOKEN')

bot = telebot.TeleBot(token)
quests = Quests()


def response_start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
    markup.add(types.KeyboardButton('Начать квест'))
    markup.add(types.KeyboardButton('В другой раз'))

    bot.send_message(message.chat.id,
                     text=f'Привет {message.from_user.first_name}, приступим к игре?',
                     reply_markup=markup
                     )


def response_help(message):
    bot.send_message(message.chat.id,
                     parse_mode='MarkdownV2',
                     text='Для работы со мной вы можете использовать одну из команд:\n\n' +
                          commands_to_string()
                     )


def response_start_quest(message):
    bot.send_message(message.chat.id, text=quests.get_start_message())
    start_quest(message.chat.id)


def response_skip_quest(message):
    bot.send_message(message.chat.id, text='Увидимся позже')


def unknown_state(chat_id):
    bot.send_message(chat_id, text='Сожалею, но что-то пошло не так. Попробуйте позже😢')


commands = [
    {
        'command': '/start',
        'description': 'запуск бота',
        'keywords': ['start', 'старт', 'поехали'],
        'handler': response_start
    },
    {
        'command': '/help',
        'description': 'перечень поддерживаемых мной команд',
        'keywords': ['help', 'помощь', 'справка'],
        'handler': response_help
    },
    {
        'command': None,
        'description': 'начало квеста',
        'keywords': ['начать квест'],
        'handler': response_start_quest
    },
    {
        'command': None,
        'description': 'пропустить квеста',
        'keywords': ['в другой раз'],
        'handler': response_skip_quest
    },
]


def commands_to_string():
    result = ''
    for command in commands:
        if command['command'] and command['description']:
            result += f"*{command['command']}* \\- {command['description']}\n"
    return result


def get_image(file_name):
    return open(file_name, 'rb')


def process_command(message, text):
    is_processed = False
    for command in commands:
        handler = None
        if command['command'] == text.lower():
            handler = command['handler']
        else:
            keywords = command['keywords']
            for keyword in keywords:
                if keyword in text.lower():
                    handler = command['handler']
        if handler:
            handler(message)
            is_processed = True
    return is_processed


def process_answer(message, text):
    is_processed = False
    answer = quests.process_answer(message.chat.id, text)
    if answer:
        next_question(message.chat.id, answer)
        is_processed = True
    return is_processed


def create_question(chat_id):
    quest = quests.get_quest(chat_id)
    if quest:
        current_route = quest.get_current_route()
        if current_route:
            markup = types.ReplyKeyboardRemove()
            if 'answers' in current_route:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
                for answer in current_route['answers']:
                    markup.add(
                        types.KeyboardButton(answer['text'])
                    )

            bot.send_message(chat_id,
                             text=current_route['question'],
                             reply_markup=markup
                             )
            if current_route['inventory']:
                bot.send_message(chat_id, text=current_route['inventory'])
            bot.send_photo(chat_id, photo=get_image(current_route['image']))
    else:
        unknown_state(chat_id)


def create_result(chat_id):
    quest = quests.get_quest(chat_id)
    if quest:
        bot.send_message(chat_id,
                         text=quest.get_result_string(),
                         reply_markup=types.ReplyKeyboardRemove()
                         )
        # bot.send_photo(chat_id, photo=quest.get_result_image())
    else:
        unknown_state(chat_id)


def start_quest(chat_id):
    if quests.start_quest(chat_id):
        next_question(chat_id)
    else:
        unknown_state(chat_id)


def next_question(chat_id, answer=None):
    if quests.next_question(chat_id, answer):
        create_question(chat_id)
    else:
        create_result(chat_id)
        quests.finish_quest(chat_id)


def process_message(message, text):
    if not process_command(message, text) and not process_answer(message, text):
        bot.send_message(message.chat.id,
                         parse_mode='MarkdownV2',
                         text=f'К сожалению я не понял вас, попробуйте уточнить свой запрос\n' +
                              'Я понимаю следующие команды:\n\n' +
                              commands_to_string()
                         )


@bot.message_handler(content_types=['text'])
def text_message(message):
    process_message(message, message.text)


@bot.message_handler(content_types=['sticker'])
def media_message(message):
    bot.send_message(message.chat.id, text='Классный стикер👍')


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    process_message(call.message, call.data)
    bot.answer_callback_query(call.id)





menu_commands = []
for command in commands:
    if command['command'] and command['description']:
        menu_commands.append(telebot.types.BotCommand(command['command'], command['description']))

try:
    bot.set_my_commands(menu_commands)
    bot.set_my_short_description("Захватывающая игра-бродилка")
    bot.set_my_description(quests.get_quest_description())
    bot.polling(non_stop=True)
except Exception as e:
    raise Exception(f'Ошибка обращения к Telegram, {e}')
