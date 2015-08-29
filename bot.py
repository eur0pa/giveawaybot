#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import threading
import time
import sys

from Libs import IRC
from Libs import Lurker
from Libs import Globals

# default encoding hack
reload(sys)
sys.setdefaultencoding('utf-8')


def main():
    irc_thread = None
    lurk_thread = None
    threads = []

    Globals.Init()
    u = Globals.Utils()
    u.pprint("reddit giveaway grabber\n")

    while threading.active_count() > 0:
        if not irc_thread or not irc_thread.is_alive():
            u.pprint('starting irc thread...\n')
            irc_thread = IRC.Client()
            irc_thread.daemon = True
            threads.append(irc_thread)
            irc_thread.start()
            time.sleep(1)
        irc_thread.join(1)

        if not lurk_thread or not lurk_thread.is_alive():
            u.pprint('starting reddit thread...\n')
            lurk_thread = Lurker.Lurk(irc_thread)
            lurk_thread.daemon = True
            threads.append(lurk_thread)
            lurk_thread.start()
            time.sleep(1)
        lurk_thread.join(1)

if __name__ == '__main__':
    main()
