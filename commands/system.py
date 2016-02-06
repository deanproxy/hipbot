import sys

def exit(msg, params=None):
    name = msg['mention_name']
    room = msg['room']

    if name != 'deanjones':
        room.message("I'm sorry, this command is only allowed by my master.")
    else:
        room.message("Okay. I'll kill myself now... :(")
        sys.exit(1)

