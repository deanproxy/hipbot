import requests
import thread
import time
import re
from bamboo_server import auth, headers, url_base

def get(url):
    print "Bamboo: Calling GET on {0}".format(url)
    return requests.get(url, auth=auth, headers=headers)

def post(url):
    print "Bamboo: Calling POST on {0}".format(url)
    return requests.post(url, auth=auth, headers=headers)

def get_latest_result(project):
    global auth, headers, url_base
    response = None

    url = url_base + '/result/' + project
    r = get(url)
    if r.status_code == 200:
        json = r.json()['results']['result'][0]
        response = {
            'id': json['number'], 
            'state': json['buildState']
        }

    return response

def get_build_alias(alias):
    f = open('hipbot.bamboo.txt')
    for line in f:
        key,val = line.strip().split(':')
        if alias.upper() == key:
            return val
    return None

def status(msg, params=None):
    room = msg['room']
    key = get_build_alias(params[0])
    if key == None:
        key = params[0]
    result = get_latest_result(key)
    if result:
        emoticon = "(greendot)"
        if result['state'] == 'Failed':
            light = "(reddot)"
        room.message('{3} The latest build for {0} was {2} (build ID {1})'.
                format(params[0], result['id'], result['state'], emoticon))
    else:
        room.message("I'm sorry, I couldn't find a build with the alias or key of {0}".format(params[0]))

def alias(msg, params=None):
    room = msg['room']
    f = open('hipbot.bamboo.txt', 'a')
    f.write('{0}:{1}\n'.format(params[0].upper(), params[1].upper()))
    room.message('Okay. Saved a build alias {0} -> {1}'.format(params[0], params[1]))

def _watch(room, plan, build_id):
    while True:
        r = get("{0}/result/{1}/{2}".format(url_base, plan, build_id))
        j = r.json()
        if r.status_code == 200:
            if j['state'] == "Unknown":
                room.message("The build I'm watching ({0}-{1}) is {2} complete.".
                        format(plan, build_id, j['progress']['percentageCompletedPretty']))
                time.sleep(60)
            else:
                emoticon = "(greendot)"
                if j['state'] == 'Failed':
                    light = "(reddot)"
                room.message("{0} The build {1}-{2} is finished. It's status is: {3}".
                    format(emoticon, plan, build_id, j['state']))
                break

def watch(msg, params=None):
    room = msg['room']
    
    build_key = re.match(r'(\w+-\w+)-(\w+)', params[0])
    if build_key:
        plan,build_id = build_key.groups()
    else:
        room.message("Parse error. You sent me: {0}".format(params[0]))
        return

    r = get("{0}/result/{1}/{2}".format(url_base, plan.upper(), build_id))
    j = r.json()
    if r.status_code == 404:
        room.message("I'm sorry, I can't watch that build. Here's the reason: {0}".format(j['message']))
        return
    else:
        thread.start_new_thread(_watch, (room, plan.upper(), build_id,))


def start(msg, params=None):
    room = msg['room']
    alias = get_build_alias(params[0])
    if alias == None:
        alias = params[0]
    url = '{0}/queue/{1}?executeAllStages=True'.format(url_base, alias)
    r = post(url)
    if r.status_code == 200:
        room.message("Okay. I started a build for {0}. I'll keep an eye on it for you.".format(params[0]))
        j = r.json()
        new_params = ['{0}-{1}'.format(alias, j['buildNumber'])]
        watch(msg, new_params)
    else:
        room.message("Oops. Couldn't run that build for some reason. Response from build server was:")
        room.message("/code {0}".format(r.json()['message']))
        room.message("Do you have an alias setup for {0}?".format(params[0]))


