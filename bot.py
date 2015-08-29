#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import threading
import time

from Libs import IRC
from Libs import Lurker
from Libs import Globals


def main():
    irc_thread = None
    lurk_thread = None
    threads = []

    Globals.Init()
    utils = Globals.Utils()
    utils.Print("reddit giveaway grabber\n")

    while threading.active_count() > 0:
        if not irc_thread or not irc_thread.is_alive():
            utils.Print('starting irc thread...\n')
            irc_thread = IRC.Client()
            irc_thread.daemon = True
            threads.append(irc_thread)
            irc_thread.start()
            time.sleep(1)
        irc_thread.join(1)

if __name__ == '__main__':
    main()
