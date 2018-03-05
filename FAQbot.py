import json
import requests
import time
import urllib
import datetime

TOKEN = "538432470:AAEXxs2UMjT5YLK2Kv73mFYkMmi_31Uu4YA"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


# def echo_all(updates):
#     for update in updates["result"]:
#         try:
#             text = update["message"]["text"]
#             chat = update["message"]["chat"]["id"]
#             send_message(text, chat)
#         except Exception as e:
#             print(e)
weekly_schedule = {
    1: 'Понедельник: 14:30 Сист. Анализ каб. 106, 16:00 Алгоритмы каб. 030, 17:30 Алгоритмы каб. 132',
    2: 'Вторник: Военная подготовка',
    3: 'Среда: Темная 14:30 Психология каб.115, Светлая 16:00 Студии каб. 120',
    4: 'Четверг: Светлая 14:30 Психология каб.117, 16:00 Сист. Анализ каб. 231,',
    5: 'Пятница: Светлая 14:30 Человеко-машинное взаимодействие каб.023, Темная 14:30 Студии каб. 124',
    6: 'Выходной',
    7: 'Выходной',
    }


def schedule(updates):
    for update in updates["result"]:
        try:
            day = datetime.date.today().isoweekday()

            text = weekly_schedule[day]
            chat = update["message"]["chat"]["id"]
            send_message(text, chat)
        except Exception as e:
            print(e)


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def send_message(text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)


def main():
    last_update_id = None
    while True:
        print("getting updates")
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            schedule(updates)
        time.sleep(0.5)


if __name__ == '__main__':
    main()
