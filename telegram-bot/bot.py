# -*- coding: utf-8 -*-
import telebot
from telebot import types
import cherrypy
import config
from vedis import Vedis

db_file = 'users.vdb'

WEBHOOK_HOST = '185.203.241.113'
WEBHOOK_PORT = 443  # 443, 80, 88 или 8443 (порт должен быть открыт!)
WEBHOOK_LISTEN = '0.0.0.0'  # На некоторых серверах придется указывать такой же IP, что и выше

WEBHOOK_SSL_CERT = './webhook_cert.pem'  # Путь к сертификату
WEBHOOK_SSL_PRIV = './webhook_pkey.pem'  # Путь к приватному ключу

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (config.token)

bot = telebot.TeleBot(config.token)


# Наш вебхук-сервер
class WebhookServer(object):
    @cherrypy.expose
    def index(self):
        if 'content-length' in cherrypy.request.headers and \
                'content-type' in cherrypy.request.headers and \
                cherrypy.request.headers['content-type'] == 'application/json':
            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode("utf-8")
            update = telebot.types.Update.de_json(json_string)
            # Эта функция обеспечивает проверку входящего сообщения
            bot.process_new_updates([update])
            return ''
        else:
            raise cherrypy.HTTPError(403)


currentMenu = []
callbackData = ['']

markupMain = types.ReplyKeyboardMarkup(resize_keyboard=True)
menu = types.KeyboardButton('Главное меню')
contacts = types.KeyboardButton('Контакты')
markupMain.row(menu, contacts)
kb = types.InlineKeyboardMarkup()
btnContinue = types.InlineKeyboardButton("Продолжить", callback_data="Continue")
kb.add(btnContinue)


@bot.message_handler(commands=["start"])
def menu(message):
    bot.send_message(message.chat.id, "Рады приветствовать Вас в Профсоюзном Объединении Республики Татарстан "
                                      "\"Торговое Единство\"!", reply_markup=markupMain)
    bot.send_photo(message.chat.id, 'AgADAgADCakxG0MDeUsPj0k9k-nhRRfzrA4ABEwMX3iWz0NwfF8BAAEC')

    bot.send_message(message.chat.id, "Нажмите Продолжить, чтобы перейти к информации о профсоюзе", reply_markup=kb)


markupMain = types.ReplyKeyboardMarkup(resize_keyboard=True)
menu = types.KeyboardButton('Главное меню')
contacts = types.KeyboardButton('Контакты')
markupMain.row(menu, contacts)

mainMenu = types.InlineKeyboardMarkup()
infOrg = types.InlineKeyboardButton(text='Об организации', callback_data="organization")
news = types.InlineKeyboardButton(text='Новости', url="http://ussrf.ru/novosti")
profCentr = types.InlineKeyboardButton(text='Профцентры стран БРИКС', callback_data="brics")
join = types.InlineKeyboardButton(text='Вступить', callback_data="join")
contacts = types.InlineKeyboardButton(text='Контакты', callback_data="contacts")
mainMenu.add(infOrg)
mainMenu.add(news, profCentr)
mainMenu.add(join, contacts)


# В большинстве случаев целесообразно разбить этот хэндлер на несколько маленьких
@bot.callback_query_handler(func=lambda call: call.data == "Continue")
def callback_inline(call):
    bot.answer_callback_query(call.id)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="выберите один из пунктов меню:", reply_markup=mainMenu)


orgMenu = types.InlineKeyboardMarkup()
service = types.InlineKeyboardButton(text='Услуги', callback_data="services")
memberShip = types.InlineKeyboardButton(text='Членство', callback_data="membership")
back = types.InlineKeyboardButton(text='Вернуться в меню', callback_data="back")
orgMenu.add(service, memberShip)
orgMenu.add(back)

backMenu = types.InlineKeyboardMarkup()
backMenu.add(back)


@bot.callback_query_handler(func=lambda call: call.data == "organization")
def test_callback(call):
    bot.answer_callback_query(call.id)
    bot.send_photo(call.message.chat.id, 'AgADAgADCakxG0MDeUtcJAEGnVb-qRfzrA4ABLjpBqWYVok2fV8BAAEC',
                   reply_markup=markupMain)
    bot.send_message(call.message.chat.id, text="<b>Мы можем и хотим быть партнером для Вас!</b>\r\n\r\n"
                                                "Мы создаем, абсолютно новую для нашей страны модель профессионального "
                                                "союза, способную не только объединить людей, представляющих самую "
                                                "массовую профессию в нашей стране, но и способную решать самые "
                                                "серьезные и большие задачи.\r\n\r\n"
                                                "1. Мы  за то, чтобы каждый специалист в торговой отрасли имел "
                                                "возможность отстаивать свои права и законные интересы!\r\n"
                                                "2. Мы за то, чтобы в нашей отрасли работало больше "
                                                "высококвалифицированных специалистов!\r\n"
                                                "3. Мы за то, чтобы каждый работник мог расчитывать на помощь и "
                                                "поддержку!\r\n\r\n"
                                                "<b>Наш проект реализуется при поддержке органов государственной власти, в "
                                                "рамках государственной программы по развития "
                                                "социального партнерства в нашей стране.</b>\r\n\r\n"
                                                "<i>На сегодняшний день наш Профессиональный союз сумел объединить более "
                                                "22 000 специалистов работающих в 27 торговых направлениях, которые "
                                                "представляют более 160 торговых и производственных компаний. Мы создаем "
                                                "огромную площадку которая позволит нашим специалистам развиваться в "
                                                "своей профессии, получать и обмениваться необходимой информацией.</i>",
                     reply_markup=markupMain, parse_mode="HTML")
    bot.send_message(chat_id=call.message.chat.id,
                     text="Выберете один из пунктов меню:", reply_markup=orgMenu)

    @bot.callback_query_handler(func=lambda call: call.data == "back")
    def test_callback(call):
        bot.answer_callback_query(call.id)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="выберите один из пунктов меню:", reply_markup=mainMenu)


@bot.callback_query_handler(func=lambda call: call.data == "brics")
def bricks_callback(call):
    bot.answer_callback_query(call.id)
    bot.send_photo(chat_id=call.message.chat.id,
                   photo="AgADAgADwagxGwM0mEtln_wUDeCrFC1Pqw4ABA8L_RtwYbH-03YBAAEC", reply_markup=markupMain)
    bot.send_message(chat_id=call.message.chat.id, parse_mode="HTML",
                     reply_markup=backMenu, text="<b>Профцентры стран БРИКС</b>\r\n\r\n"
                                                 "После создания нового международного формата БРИКС национальные "
                                                 "профсоюзные центры входящих в него стран внимательно следили за "
                                                 "процессом его становления и развития с точки зрения возможного "
                                                 "участия в его деятельности. По мнению профсоюзов стран БРИКС эта "
                                                 "структура наглядно символизирует переход от однополярности к более "
                                                 "справедливому мироустройству. При этом профсоюзы выступают за "
                                                 "позиционирование БРИКС как новой модели глобальных отношений, "
                                                 "строящейся поверх старых барьеров Восток-Запад или Север-Юг.Идея "
                                                 "учреждения Профсоюзного Форума в рамках БРИКС получила однозначную "
                                                 "поддержку на 2-ом Конгрессе Международной конфедерации профсоюзов "
                                                 "(МКП) в Ванкувере в 2010 году и развивалась в ходе ряда консультаций, "
                                                 "проведенных во время заседаний руководящих органов МКП и МОТ.Результатом "
                                                 "этой работы стало подписание Декларации Профсоюзного форума стран "
                                                 "БРИКС в ходе Конференции высокого уровня по вопросам достойного "
                                                 "труда, проходившей в Москве в декабре 2012 г. под эгидой МОТ "
                                                 "(Декларация I Профсоюзного Форума 12 декабря 2012 года). Создание "
                                                 "новой глобальной профсоюзной структуры, объединяющей крупнейшие "
                                                 "объединения трудящихся стран, занимающих 30% территории Земли, в "
                                                 "которых проживает 43% ее населения и производится около четверти "
                                                 "мирового ВВП, «будет содействовать развитию диалога и сотрудничества "
                                                 "между народами, придаст работе БРИКС социальное измерение на основе "
                                                 "концепции Достойного труда МОТ», говорится в Декларации. Кроме того, "
                                                 "такой шаг способствовал бы расширению уже созданных в БРИКС форматов "
                                                 "сотрудничества.Включение представителей трудящихся в официальный "
                                                 "формат БРИКС даст дополнительную возможность для ускорения "
                                                 "всестороннего развития наших стран и покажет всему миру, что этот "
                                                 "форум может стать реальным противовесом тем силам, которые сегодня "
                                                 "стремятся диктовать ход мирового развития.")

    @bot.callback_query_handler(func=lambda call: call.data == "back")
    def test_callback(call):
        bot.answer_callback_query(call.id)
        bot.send_message(chat_id=call.message.chat.id, text="Выберите один из пунктов меню:", reply_markup=mainMenu)


contactsMenu = types.InlineKeyboardMarkup()
ourSite = types.InlineKeyboardButton(text="Наш сайт", url="http://ussrf.ru/")
chanel = types.InlineKeyboardButton(text=" Наш канал", url="t.me/ussrf")
fnpr = types.InlineKeyboardButton(text="ФНПР", url="http://www.fnpr.ru/")
fprt = types.InlineKeyboardButton(text="Федерация Профсоюзов Республики Татасрстан", url="http://proftat.ru/")
contactsMenu.add(ourSite, fnpr)
contactsMenu.add(chanel, fprt)
contactsMenu.add(back)


@bot.callback_query_handler(func=lambda call: call.data == "contacts")
def bricks_callback(call):
    bot.answer_callback_query(call.id)
    bot.send_message(reply_markup=markupMain, chat_id=call.message.chat.id, parse_mode="HTML",
                     text="<b>Наш адрес:</b>\r\n"
                          "<i>Россия, г. Казань, ул. Муштари, дом. 9, кабинет 215</i>\r\n\r\n"
                          "<b>Телефон:</b>\r\n"
                          "<i>+7 (843) 253-14-82</i>\r\n"
                          "<i>+7 (917) 267-56-70</i>\r\n"
                          "Правовая поддержка: <i>8 (800) 350-94-14</i>\r\n\r\n"
                          "<b>Почта:</b>\r\n"
                          "<i>info@ussrf.ru</i>\r\n\r\n"
                     )
    bot.send_message(chat_id=call.message.chat.id, text="<b>Сайты:</b>", reply_markup=contactsMenu,
                     parse_mode="HTML")

    @bot.callback_query_handler(func=lambda call: call.data == "back")
    def test_callback(call):
        bot.answer_callback_query(call.id)
        bot.send_message(chat_id=call.message.chat.id, text="Выберите один из пунктов меню:", reply_markup=mainMenu)


@bot.message_handler(regexp="Главное меню")
def print_menu(message):
    bot.send_message(chat_id=message.chat.id,
                     text="выберите один из пунктов меню:", reply_markup=mainMenu)


@bot.message_handler(regexp="Контакты")
def print_contacts(message):
    bot.send_message(reply_markup=markupMain, chat_id=message.chat.id, parse_mode="HTML",
                     text="<b>Наш адрес:</b>\r\n"
                          "<i>Россия, г. Казань, ул. Муштари, дом. 9, кабинет 215</i>\r\n\r\n"
                          "<b>Телефон:</b>\r\n"
                          "<i>+7 (843) 253-14-82</i>\r\n"
                          "<i>+7 (917) 267-56-70</i>\r\n"
                          "Правовая поддержка: <i>8 (800) 350-94-14</i>\r\n\r\n"
                          "<b>Почта:</b>\r\n"
                          "<i>info@ussrf.ru</i>\r\n\r\n"
                     )
    bot.send_message(chat_id=message.chat.id, text="<b>Сайты:</b>", reply_markup=contactsMenu,
                     parse_mode="HTML")


keyboard_send = types.ReplyKeyboardMarkup(row_width=1)
keyboard_send.add(types.KeyboardButton(text="Отправить"))

keyboard_phone = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
button_phone = types.KeyboardButton(text="Отправить номер телефона", request_contact=True)
keyboard_phone.add(button_phone)

user = {}


def set_current_state(user_id):
    with Vedis(db_file) as db:
        try:
            db.hmset(user_id,
                     {'last_name_flag': True, 'name_flag': False, 'organization_flag': False, 'email_flag': False,
                      'phone_number_flag': False})
            print(db.hgetall(user_id))

        except KeyError:
            print('ошибка')


def change_current_state(user_id, param, value):
    with Vedis(db_file) as db:
        try:
            db.hset(user_id, param, value)
            print(db.hgetall(user_id))
        except KeyError:
            print('ошибка')


def get_current_state(user_id, param):
    with Vedis(db_file) as db:
        try:
            return db.hget(user_id, param)

        except KeyError:
            print('ошибка')


@bot.callback_query_handler(func=lambda call: call.data == "join")
def contact_query(call):
    bot.answer_callback_query(call.id)
    if call.message:
        print(user)
        bot.send_message(call.message.chat.id, text="Введите вашу фамилию:", reply_markup=markupMain)
        user[call.message.chat.id] = {}
        set_current_state(call.message.chat.id)

        # user[call.message.chat.id].update({'last_name_flag': True, 'name_flag': False, 'organization_flag': False,
        #                             'email_flag': False, 'phone_number_flag': False})

        @bot.message_handler(func=lambda message: get_current_state(message.chat.id, 'last_name_flag') == b'True')
        def test_name(message):
            change_current_state(message.chat.id, 'last_name_flag', False)
            user[message.chat.id].update({'last_name': message.text})

            bot.send_message(message.chat.id, text="Введите ваше имя:")
            change_current_state(message.chat.id, 'name_flag', True)
            user[message.chat.id].update({'name_flag': True})

        @bot.message_handler(func=lambda message: get_current_state(message.chat.id, 'name_flag') == b'True')
        def test_fam(message):
            change_current_state(message.chat.id, 'name_flag', False)
            # user[message.chat.id].update({'name_flag': False})
            user[message.chat.id].update({'name': message.text})

            bot.send_message(message.chat.id, text="Введите вашу организацию:")
            change_current_state(message.chat.id, 'organization_flag', True)
            # user[message.chat.id].update({'organization_flag': True})

        @bot.message_handler(
            func=lambda message: get_current_state(message.chat.id, 'organization_flag') == b'True')
        def test_org(message):
            change_current_state(message.chat.id, 'organization_flag', False)
            # user[message.chat.id].update({'organization_flag': False})
            user[message.chat.id].update({'organization': message.text})

            bot.send_message(message.chat.id, text="Введите ваш email:")
            change_current_state(message.chat.id, 'email_flag', True)
            # user[message.chat.id].update({'email_flag': True})

        @bot.message_handler(func=lambda message: get_current_state(message.chat.id, 'email_flag') == b'True')
        def test_em(message):
            change_current_state(message.chat.id, 'email_flag', False)
            # user[message.chat.id].update({'email_flag': False})
            user[message.chat.id].update({'email': message.text})

            bot.send_message(message.chat.id, text="Отправьте свой номер телефона:")
            change_current_state(message.chat.id, 'phone_number_flag', True)
            # user[message.chat.id].update({'phone_number_flag': True})

        @bot.message_handler(func=lambda message: get_current_state(message.chat.id, 'phone_number_flag') == b'True')
        def print_number(message):
            change_current_state(message.chat.id, 'phone_number', False)
            # user[message.chat.id].update({'phone_number_flag': False})

            user[message.chat.id].update({'phone_number': message.text})

            bot.send_message(message.chat.id,
                             text="Спасибо. В ближайшее время наш сотрудник свяжется с вами!",
                             reply_markup=markupMain)

            bot.send_message(chat_id=-250283845,
                             text="==========================\r\n\r\n" + "Новая заявка!\r\n\r\n" + "<b>Имя: </b>" + str(
                                 user[message.chat.id]['name']) + "\r\n" + "<b>Фамилия: </b>" + str(
                                 user[message.chat.id]['last_name']) + "\r\n" + "<b>Организация: </b>" + str(
                                 user[message.chat.id]['organization']) + "\r\n" + "<b>Email: </b>" + str(
                                 user[message.chat.id]['email']) + "\r\n" + "<b>Телефон: </b>" + str(
                                 user[message.chat.id][
                                     'phone_number']) + "\r\n\r\n" + "==========================\r\n\r\n",
                             parse_mode="HTML")
            user.pop(message.chat.id)
            print(user)
            # user[message.chat.id].update({'last_name_flag': False, 'name_flag': False, 'organization_flag': False,
            # 'email_flag': False, 'phone_number_flag': False})


# Снимаем вебхук перед повторной установкой (избавляет от некоторых проблем)
bot.remove_webhook()

# Ставим заново вебхук
bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
                certificate=open(WEBHOOK_SSL_CERT, 'r'))

# Указываем настройки сервера CherryPy
cherrypy.config.update({
    'server.socket_host': WEBHOOK_LISTEN,
    'server.socket_port': WEBHOOK_PORT,
    'server.ssl_module': 'builtin',
    'server.ssl_certificate': WEBHOOK_SSL_CERT,
    'server.ssl_private_key': WEBHOOK_SSL_PRIV
})

# Собственно, запуск!
cherrypy.quickstart(WebhookServer(), WEBHOOK_URL_PATH, {'/': {}})
