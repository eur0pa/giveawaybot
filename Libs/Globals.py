import sys
import time


CONFIG_FILE = 'bot.ini'
BACKLOG_FILE = 'giveaway.txt'

Config = {}
Backlog = {}


class Save(object):
    """not implemented yet"""
    def __init__(self):
        super(Save, self).__init__()
        self.save_config(CONFIG_FILE)

    def save_config(self, config_file):
        raise NotImplementedError


class Init(object):
    """Inits backlog and config global variables"""

    def __init__(self):
        super(Init, self).__init__()
        self.read_config(CONFIG_FILE)
        self.read_backlog(BACKLOG_FILE)

    def read_config(self, config_file):
        """reads the config file

        reads the config file specified in the config_file argument and
        populates the global Config dict accordingly.

        args:
            config_file: the config file to read and parse
        """
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

    def read_backlog(self, backlog_file):
        """reads the backlog file

        reads the backlog file specified in the backlog_file argument and
        populates the global Backlog dict accordingly.

        args:
            backlog_file: the backlog file to read and parse

        raises: IOError when the file doesn't exist, and proceeds to create one
        """
        try:
            f = open(backlog_file)
            f.close()
        except IOError:
            with open(backlog_file, 'w') as f:
                f.write('bogus')

        with open(backlog_file, 'r') as f:
            for entry in f.read().split(','):
                Backlog[entry] = True


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

    def reset(self):
        """resets filters"""
        del Config['CustomFilter'][:]
