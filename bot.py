#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import threading

from time import sleep

from Libs import IRC
from Libs import Lurker
from Libs import Globals


def read_backlog(backlog_file):
    backlog = {}
    try:
        with open(backlog_file) as f:
            for entry in f.read().split(','):
                backlog[entry] = True
    except IOError:
        file(backlog_file, 'w').close()
    return backlog


def read_config(cfg_file):
    config = {}
    with open(cfg_file) as f:
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
            config[section] = values
    return config


def main():
    irc_thread = None
    lurk_thread = None
    threads = []

    utils = Globals.Utils()
    utils.Print("reddit giveaway grabber\n")

    Globals.Config = read_config(Globals.CONFIG_FILE)
    Globals.Backlog = read_backlog(Globals.BACKLOG_FILE)

    while threading.active_count() > 0:
        if not irc_thread or not irc_thread.is_alive():
            utils.Print('starting irc thread...\n')
            irc_thread = IRC.Client()
            irc_thread.daemon = True
            threads.append(irc_thread)
            irc_thread.start()
            sleep(1)
        irc_thread.join(1)

if __name__ == '__main__':
    main()
