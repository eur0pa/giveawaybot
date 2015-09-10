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

    common.init_globals()
    common.sprint("reddit giveaway grabber [rev. %s]\n" % common.Version)

    while True:
        if not irc_thread or not irc_thread.is_alive():
            common.init_globals()
            common.sprint('starting irc thread...\n')
            irc_thread = irc.Client()
            irc_thread.daemon = True
            irc_thread.start()

        if not lurk_thread or not lurk_thread.is_alive():
            common.sprint('starting reddit thread...\n')
            lurk_thread = lurker.Lurk(irc_thread)
            lurk_thread.daemon = True
            lurk_thread.start()

        irc_thread.join(0)
        lurk_thread.join(0)

        time.sleep(1)


if __name__ == '__main__':
    main()
