#!/usr/bin/env python

from bs4 import BeautifulSoup
import requests
import json
import hashlib
import logging
from datetime import datetime, timedelta
import configparser


# HOW to:
# - calculate hash of given sting?
# - how to save data as JSON?
# - how to convert string to time object?
# - add date format to logger
# - add job to CRON
# - check logs from CRON

def get_current_data():
    '''
    Returns list of dicts with details information
    '''
    url = 'https://lowcygier.pl/'
    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')
    articles = soup.select('article.post-widget.post.entry.clearfix')

    data = {}
    for article in articles:
        title = article.select('h2.post-title a')[0].get_text()
        date = article.select('time')[0]['datetime']
        m = hashlib.sha256()
        # unicode must be encoded before hashing
        m.update(title.encode('utf-8'))
        m.digest()

        value = {}
        value['datetime'] = date
        value['title'] = title

        key = m.hexdigest()
        data[key] = value

    return data

def save_JSON(file_name: str, data):
    with open(file_name, 'w') as f:
        json.dump(data, f)

def load_JSON(file_name: str):
    # TODO: if file do not exist return empty dict
    with open(file_name, 'r') as f:
        loaded_data = json.load(f)
    return loaded_data


def main():
    # Read secrets
    config = configparser.ConfigParser()
    config.read('config.cfg')
    
    data = get_current_data()
    seen = load_JSON('test.json')
    seen = cleanse_data(seen)
    # seen = {}
    for item in data:
        if item not in seen:
            logging.debug(data[item]['title'])
            # Update seen dict.
            seen[item] = data[item]
            telegram_bot_sendtext(
                data[item]['title'],
                bot_token=config['telegram']['token'],
                bot_chatID=config['telegram']['id'],
                )
    save_JSON('test.json', seen)
    pass


def cleanse_data(data):
    now = datetime.now()
    delta = timedelta(days=5)
    for key in data:
        timestamp = data[key]['datetime']
        timestamp = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S+00:00')
        if now > timestamp + delta:
            del data[key]
    return data


def telegram_bot_sendtext(bot_message, bot_token, bot_chatID):
    
    # bot_token =  
    # bot_chatID = 
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s')
    logging.debug('START')
    main()
    pass