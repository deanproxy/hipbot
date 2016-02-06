import random

def respond(msg, params=None):
    room = msg['room']
    responses = (
        "What's up",
        "Howdy",
        "Yo",
        "What it is, my main human.."
    )
    room.message(responses[random.randint(0, len(responses)-1)])
