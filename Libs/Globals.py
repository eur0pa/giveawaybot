import sys
import time


CONFIG_FILE = 'bot.ini'
BACKLOG_FILE = 'giveaway.txt'

Config = {}
Backlog = {}


class Save(object):
    """docstring for Save"""
    def __init__(self):
        super(Save, self).__init__()
        self.save_config(CONFIG_FILE)

    def save_config(self, config_file):
        pass


class Init(object):
    """docstring for Init"""
    def __init__(self):
        super(Init, self).__init__()
        self.read_config(CONFIG_FILE)
        self.read_backlog(BACKLOG_FILE)

    def read_backlog(self, backlog_file):
        try:
            with open(backlog_file) as f:
                for entry in f.read().split(','):
                    Backlog[entry] = True
        except IOError:
            file(backlog_file, 'w').close()

    def read_config(self, config_file):
        with open(config_file) as f:
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
                Config[section] = values


class Utils(object):
    """docstring for Print"""
    def __init__(self):
        super(Utils, self).__init__()

    def Print(self, msg):
        clock = "[" + time.asctime(time.localtime()) + "] "
        sys.stdout.write("\r" + clock + msg)
        sys.stdout.write("\033[K")
        sys.stdout.flush()
