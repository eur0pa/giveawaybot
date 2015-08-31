#!/usr/bin/env python2
# -*- coding: utf-8 -*-


import sys
import time
import threading

from lib import common
from lib import irc
from lib import lurker

reload(sys)
sys.setdefaultencoding('utf-8')


def main():
    irc_thread = None
    lurk_thread = None
    threads = []

    common.init_globals()
    common.sprint("reddit giveaway grabber [rev. %s]\n" % common.Version)

    while threading.active_count() > 0:
        if not irc_thread or not irc_thread.is_alive():
            common.init_globals()
            common.sprint('starting irc thread...\n')
            irc_thread = irc.Client()
            irc_thread.daemon = True
            threads.append(irc_thread)
            irc_thread.start()
            time.sleep(1)
        irc_thread.join(1)

        if not lurk_thread or not lurk_thread.is_alive():
            common.sprint('starting reddit thread...\n')
            lurk_thread = lurker.Lurk(irc_thread)
            lurk_thread.daemon = True
            threads.append(lurk_thread)
            lurk_thread.start()
            time.sleep(1)
        lurk_thread.join(1)


if __name__ == '__main__':
    main()
