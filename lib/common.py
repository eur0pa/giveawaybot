import os
import sys
import time
import re


CONFIG_FILE = 'bot.conf'
BACKLOG_FILE = 'giveaway.txt'

Config = {}
Backlog = {}
Version = None


def init_globals():
    global Config
    global Backlog
    global Version

    Config = read_config()
    Backlog = read_backlog()
    Version = get_version()


def sprint(msg):
    clock = "[" + time.asctime(time.localtime()) + "] "
    sys.stdout.write("\r" + clock + msg)
    sys.stdout.write("\033[K")
    sys.stdout.flush()


def add_backlog_entry(id):
    with open(BACKLOG_FILE, 'a') as f:
        f.write(',' + id)


def save_config():
    with open(CONFIG_FILE, 'w') as f:
        for section in Config:
            f.write('>>%s\n' % section)
            for entry in Config[section]:
                f.write('%s\n' % entry)
            f.write('\n')
    read_config()


def read_config(refresh=False):
    if not refresh:
        res = {}
    with open(CONFIG_FILE) as f:
        for line in f.readlines():
            line = line.strip()
            if not line:
                continue
            if line[0:2] == '>>':
                values = []
                section = line.split('>>')[1]
            else:
                if len(line.split('=')) > 1:
                    values.append(line.split('=')[1])
                else:
                    values.append(line)
            if refresh:
                Config[section] = values
            else:
                res[section] = values
    if not refresh:
        return res


def read_backlog():
    res = {}
    try:
        f = open(BACKLOG_FILE)
        f.close()
    except IOError:
        with open(BACKLOG_FILE, 'w') as f:
            f.write('bogus')
    with open(BACKLOG_FILE, 'r') as f:
        for entry in f.read().split(','):
            res[entry] = True
    return res


def get_version():
    file_path = None
    res = None
    _ = os.path.dirname(__file__)
    while True:
        file_path = os.path.join(_, '.git', 'HEAD')
        if os.path.exists(file_path):
            break
        else:
            file_path = None
            if _ == os.path.dirname(_):
                break
            else:
                _ = os.path.dirname(_)
    while True:
        if file_path and os.path.isfile(file_path):
            with open(file_path, 'r') as f:
                res = f.read()
                if res.startswith('ref: '):
                    file_path = os.path.join(_, '.git', res.replace('ref: ', '')).strip()
                else:
                    res = re.match(r'(?i)[0-9a-f]{32}', res)
                    res = res.group(0) if res else None
                    break
        else:
            break
    return res[:7] if res else None
