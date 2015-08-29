import socket
import threading
import time

import Globals


class Client(threading.Thread):
    """docstring for Client"""
    def __init__(self):
        threading.Thread.__init__(self)
        self.host = Globals.Config['IRC'][0]
        self.port = int(Globals.Config['IRC'][1])
        self.nick = Globals.Config['IRC'][2]
        self.chan = Globals.Config['IRC'][3]
        self.s = socket.socket()

    def run(self):
        self._login()
        self._idle()

    def stop(self):
        self._quit()
        self._Thread_stop()

    def _send(self, msg, type=0, dest=None):
        if not dest:
            dest = self.chan
        if type == 0:
            s = u'PRIVMSG %s :%s\n' % (dest, msg)
        elif type == 1:
            s = u'%s\n' % msg
        self.s.send(s)

    def _login(self):
        self.s.connect((self.host, self.port))
        self._send('NICK %s' % self.nick, type=1)
        self._send('USER %s %s 0: %s' % (self.nick, self.host, self.nick), type=1)
        self._send('JOIN %s' % self.chan, type=1)
        time.sleep(1)

    def _quit(self):
        self._send('QUIT *poff*', type=1)
        time.sleep(1)
        self.s.close()

    def _idle(self):
        while True:
            cmd = None
            arg = None
            buf = self.s.recv(1024).strip().split('\n')
            for line in buf:
                clean = line.split()
            try:
                if clean[0] == 'PING':
                    self._send("PONG %s" % clean[1], type=1)

                elif clean[1] == 'PRIVMSG':
                    if clean[2] != self.chan:
                        continue
                    try:
                        cmd = line.split(':')[2].split()[0]
                        arg = line.split(':')[2][len(cmd)+1:]
                        self._handle_commands(cmd, arg)
                    except:
                        pass
            except Exception, err:
                print '>>> IRC EXCEPTION <<< [ ' + str(err) + ' ]'
                pass
            time.sleep(1)

    def _handle_commands(self, cmd, arg):
        if cmd == '!stato':
            gcount = len(Globals.Backlog)
            fcount = len(Globals.Config['CustomFilter'])
            self._send('%d giveaway nel backlog, %d filtri attivi' % (gcount, fcount))

        elif cmd == '!poff':
            self.stop()

        elif cmd == '!filtra':
            if len(arg) < 4:
                self._send('uso: !filtra <almeno 5 char porco dio>')
                return
            Globals.Config['CustomFilter'].append(arg)
            count = len(Globals.Config['CustomFilter'])
            self._send('%s filtrato, %d filtri attivi.' % (arg, count))

        elif cmd == '!filtri':
            count = len(Globals.Config['CustomFilter'])
            filtri = ', '.join(Globals.Config['CustomFilter'])
            self._send('%d filtri attivi: %s.' % (count, filtri))
