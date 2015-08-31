import time
import threading
import praw

import common


class Lurk(threading.Thread):
    def __init__(self, irc_thread):
        self.thread = threading.Thread.__init__(self)
        self._stop = threading.Event()
        self.irc = irc_thread
        self.r = praw.Reddit('Diochan PRAW Test')

    def run(self):
        while not self._stop.isSet():
            self._lurk()

    def stop(self):
        self._stop.set()

    def _lurk(self):
        for sub in common.Config['Subs']:
            subreddit = self.r.get_subreddit(sub)
            common.sprint('lurking /r/%s' % sub)
            for post in subreddit.get_new(limit=2):
                if post.id in common.Backlog:
                    continue
                common.sprint('checking /r/%s post #%s' % (sub, post.id))
                common.Backlog[post.id] = True
                if self._check_submission(post, sub):
                    s = post.short_link + ' - ' + post.title
                    t = threading.Thread(
                        target=self.irc.sendirc,
                        args=(s, 0, None))
                    t.daemon = True
                    t.start()
                    common.add_backlog_entry(post.id)
                    common.sprint(s + '\n')
            time.sleep(3)

    def _check_submission(self, post, sub):
        title = unicode(post.title).lower()
        text = unicode(post.selftext).lower()
        flair = unicode(post.link_flair_text).lower()
        url = unicode(post.url).lower()
        sub = sub.lower()

        if any(x in title for x in common.Config['CustomFilter']): return 0
        if any(x in title for x in common.Config['Exclude']): return 0
        if any(x in url for x in common.Config['ExcludeUrls']): return 0
        if any(x in flair for x in common.Config['ExcludeFlairs']): return 0

        if sub in common.Config['SuperSubs']: return 1
        if sub in common.Config['DealsSubs']: return 1
        if any(i in url for i in common.Config['IncludeUrls']) and not post.is_self: return 1
        if any(i in title for i in common.Config['Include']): return 1
