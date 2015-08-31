import os
import sys
import time
import re


CONFIG_FILE = 'bot.ini'
BACKLOG_FILE = 'giveaway.txt'

Config = {}
Backlog = {}
Version = None


class Init(object):
    """Inits backlog and config global variables"""
    def __init__(self):
        super(Init, self).__init__()
        global Version
        u = Utils()
        u.read_config()
        u.read_backlog()
        Version = u.get_version()


class Utils(object):
    """miscellaneus utilities"""
    def __init__(self):
        super(Utils, self).__init__()

    def sprint(self, msg):
        """a statusbar-like print for console

        args:
            msg: the string to print
        """
        clock = "[" + time.asctime(time.localtime()) + "] "
        sys.stdout.write("\r" + clock + msg)
        sys.stdout.write("\033[K")
        sys.stdout.flush()

    def add_backlog_entry(self, id):
        """adds an entry to the backlog file

        args:
            id: the entry to add
        """
        with open(BACKLOG_FILE, 'a') as f:
            f.write(',' + id)

    def save_config(self):
        """saves and reloads the current config to disk

        args:
            config_file: the config file to write to
        """
        with open(CONFIG_FILE, 'w') as f:
            for section in Config:
                f.write('>>%s\n' % section)
                for entry in Config[section]:
                    f.write('%s\n' % entry)
                f.write('\n')
        self.read_config()

    def read_config(self):
        """reads the config file

        reads the config file specified in the config_file argument and
        populates the global Config dict accordingly.

        args:
            config_file: the config file to read and parse
        """
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
                Config[section] = values

    def read_backlog(self):
        """reads the backlog file

        reads the backlog file specified in the backlog_file argument and
        populates the global Backlog dict accordingly.

        args:
            backlog_file: the backlog file to read and parse

        raises: IOError when the file doesn't exist, and proceeds to create one
        """
        try:
            f = open(BACKLOG_FILE)
            f.close()
        except IOError:
            with open(BACKLOG_FILE, 'w') as f:
                f.write('bogus')

        with open(BACKLOG_FILE, 'r') as f:
            for entry in f.read().split(','):
                Backlog[entry] = True

    def get_version(self):
        """sets the abbreviated commit hash a la git rev-parse --short HEAD"""
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
