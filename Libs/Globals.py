import sys
import time


CONFIG_FILE = 'bot.ini'
BACKLOG_FILE = 'giveaway.txt'

Config = {}
Backlog = {}


class Init(object):
    """Inits backlog and config global variables"""
    def __init__(self):
        super(Init, self).__init__()
        u = Utils()
        u.read_config()
        u.read_backlog()


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
        """saves the current config to disk

        args:
            config_file: the config file to write to
        """
        with open(CONFIG_FILE, 'w') as f:
            for section in Config:
                f.write('>>%s\n' % section)
                for entry in Config[key]:
                    f.write('%s\n' % entry)
                f.write('\n')

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
