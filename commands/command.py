import salute
import help
import system
import build
import random
import jokes
import re

def default(msg, params=None):
    responses = (
        'Wat?',
        "I don't understand...",
        "Please speak clearly!",
        "I'm not sure what you're asking.",
        "Check out my help section.",
        "Dude, you're speaking jibberish.",
    )
    room = msg['room']
    room.message(responses[random.randint(0, len(responses)-1)])

# List of responses to messages
commands = (
    ('hi', salute.respond),
    ('hello', salute.respond),
    ("what's up", salute.respond),
    ('help', help.show),
    ('die', system.exit),
    ('tell me a joke', jokes.tell),
    (r'(?:\w+\s)?build status for (\w+(?:[-\w+])+)', build.status),
    (r'alias build (\w+(?:[-\w+])+) (\w+(?:[-\w+])+)', build.alias),
    (r'start build for (\w+(?:[-\w+])+)', build.start),
    (r'watch build (\w+(?:[-\w+])+)', build.watch),
    (r'.*', default),
)

class Command:
    command = None
    params = None

    def __init__(self, command, params):
        self.command = command
        self.params = params

    def run(self, msg):
        self.command(msg, self.params)

def parse(msg_str):
    cmd = None
    for i in commands:
        r = re.match(i[0], msg_str)
        if r:
            cmd = Command(i[1], r.groups())
            break

    return cmd

