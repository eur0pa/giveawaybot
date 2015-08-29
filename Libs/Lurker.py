import time
import threading
import praw

import Globals


class Lurk(threading.Thread):
    """docstring for Lurk"""
    def __init__(self, irc_thread):
        self.thread = threading.Thread.__init__(self)
        self._stop = threading.Event()
        self.irc = irc_thread
        self.r = praw.Reddit('Diochan PRAW Test')
        self.u = Globals.Utils()

    def run(self):
        while not self._stop.isSet():
            self._lurk()

    def stop(self):
        self._stop.set()

    def _lurk(self):
        for sub in Globals.Config['Subs']:
            subreddit = self.r.get_subreddit(sub)
            self.u.sprint('lurking /r/%s' % sub)
            for post in subreddit.get_new(limit=2):
                if post.id in Globals.Backlog:
                    continue
                self.u.sprint('checking /r/%s post #%s' % (sub, post.id))
                Globals.Backlog[post.id] = True
                if self._check_submission(post, sub):
                    s = post.short_link + ' - ' + post.title
                    t = threading.Thread(
                        target=self.irc.sendirc,
                        args=(s, 0, None))
                    t.daemon = True
                    t.start()
                    self.u.add_backlog_entry(post.id)
                    self.u.sprint(s + '\n')
            time.sleep(3)

    def _check_submission(self, post, sub):
        title = unicode(post.title).lower()
        text = unicode(post.selftext).lower()
        flair = unicode(post.link_flair_text).lower()
        url = unicode(post.url).lower()
        sub = sub.lower()

        if title in Globals.Config['Exclude']: return 0
        if url in Globals.Config['ExcludeUrls']: return 0
        if flair in Globals.Config['ExcludeFlairs']: return 0

        if sub in Globals.Config['SuperSubs']: return 1
        if sub in Globals.Config['DealsSubs']: return 1
        if url in Globals.Config['IncludeUrls'] and not post.is_self: return 1
        if title in Globals.Config['Include'] or \
           text in Globals.Config['Include']: return 1
