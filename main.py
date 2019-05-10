import telebot
import meduza
import constant
import time


bot = telebot.TeleBot(constant.token)

subscribers = []


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    start = "Привет! Начни со свежих новостей. Для этого введи команду /news"
    bot.send_message(message.chat.id,
                     start)


@bot.message_handler(commands=['last_news'])
def news(message):
    url_out = meduza.latest_push()['url']
    title_out = meduza.get(url_out)['title']
    bot.send_message(message.chat.id,
                     '{a} \n {b}'.format(a=title_out, b=url_out))


@bot.message_handler(commands=['news', 'shapito', 'articles',
                               'games', 'razbor', 'podcasts'])
def news(message):
    section = message.text[1:]
    for article in meduza.section(section, n=3, lang='ru'):
        title_out = article['title']
        url = article['url']
        url_for_out = "https://meduza.io/" + url

        bot.send_message(message.chat.id,
                         '{a} \n {b}'.format(a=title_out, b=url_for_out))


@bot.message_handler(commands=['top'])
def top(message):
    max_reactions = 0
    global url_of_news
    url_of_news = ''
    global title_of_news
    title_of_news = ''
    for article in meduza.section('news', n=5, lang='ru'):
        url = article['url']
        cur_reactions = int(meduza.reactions_for(url)[url]['stats']['fb'])
        if cur_reactions > max_reactions:
            url_of_news = url
            title_of_news = article['title']
            max_reactions = cur_reactions

    url_of_news = "https://meduza.io/" + url_of_news
    bot.send_message(message.chat.id,
                     '{a} \n {b}'.format(a=title_of_news, b=url_of_news))


bot.polling(none_stop=True, interval=0.5)
