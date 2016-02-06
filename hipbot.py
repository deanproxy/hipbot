#!/usr/bin/env python

import datetime
import time
import pytz
import re

from hypchat import HypChat
from commands import command

bot_name = 'deanjones'

# List of rooms 
rooms = {
    '#dev': None,
    'bottest': None
}

def log(message):
    print message

def is_message_for_me(mentions):
    for_me = False
    for i in mentions:
        if i['mention_name'] == bot_name:
            for_me = True
            break
    return for_me

def strip_names(message):
    return re.sub('\@\w+\s', '', message)

def get_latest_history(last_date):
    latest_history = []
    for i in rooms:
        history = rooms[i].history()
        for h in history['items']:
            if h['date'] > last_date and is_message_for_me(h['mentions']):
                message = {
                    'room': rooms[i],
                    'message': strip_names(h['message']),
                    'mention_name': h['from']['mention_name']
                }
                latest_history.append(message)

    return latest_history

def respond_to_messages(history):
    for h in history:
        cmd = command.parse(h['message'].lower())
        if cmd:
            cmd.run(h)
            break

# Get the id for the rooms we want to pay attention to
hc = HypChat('NbrdgFyybz4SOVpBICsQ3CfoVRVVZhMFAY9NrdE5', endpoint='https://hipchat.pamlabdev.com')
for i in hc.rooms(expand='items')['items']:
    for j in rooms:
        if j == i['name']:
            rooms[j] = hc.get_room(i['id'])

# Listen to the room history every 5 seconds
last_date = datetime.datetime.now(pytz.UTC)
while True:
    # Setting the date first because otherwise there is a potential 
    # for a race condition between the time we retrieve the history
    # and the time we reset the last date we checked messages
    tmp_date = datetime.datetime.now(pytz.UTC)
    history = get_latest_history(last_date)
    last_date = tmp_date

    log("Got {0} messages for me.".format(len(history)))
    respond_to_messages(history)
    time.sleep(10)

