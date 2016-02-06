import random

def tell(msg, params=None):
    f = open('hipbot.jokes.txt')
    jokes = f.read().split('\n')
    room = msg['room']
    room.message(jokes[random.randint(0, len(jokes)-1)])

