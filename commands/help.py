
def show(msg, params=None):
    room = msg['room']
    room.message('Here is a list of things I can do...')
    room.message('/code * get build status for _branch_.\n' +
            '* alias build _name_ _buildkey_\n' + 
            '* die (do you really want to hurt me?).')

