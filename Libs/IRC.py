import socket
import threading
import time

import Globals


class Client(threading.Thread):
    """docstring for Client"""
    def __init__(self):
        threading.Thread.__init__(self)
        self._stop = threading.Event()
        self.s = socket.socket()
        self.u = Globals.Utils()

        self.host = Globals.Config['IRC'][0]
        self.port = int(Globals.Config['IRC'][1])
        self.nick = Globals.Config['IRC'][2]
        self.chan = Globals.Config['IRC'][3]

    def run(self):
        self._login()
        while not self._stop.isSet():
            self._idle()
            time.sleep(1)
        self._quit()

    def stop(self):
        self._stop.set()

    def sendirc(self, msg, type=0, dest=None):
        if not dest:
            dest = self.chan
        if type == 0:
            s = u'PRIVMSG %s :%s\n' % (dest, msg)
        elif type == 1:
            s = '%s\n' % msg
        self.s.send(s)

    def _login(self):
        self.s.connect((self.host, self.port))
        self.sendirc('NICK %s' % self.nick, type=1)
        self.sendirc('USER %s %s 0: %s' % (self.nick, self.host, self.nick), type=1)
        self.sendirc('JOIN %s' % self.chan, type=1)
        time.sleep(1)

    def _quit(self):
        self.sendirc('QUIT :*poff*' % i, type=1)

    def _idle(self):
        cmd = None
        arg = None
        buf = self.s.recv(1024).strip().split('\n')
        for line in buf:
            clean = line.split()
        try:
            if clean[0] == 'PING':
                self.sendirc("PONG %s" % clean[1], type=1)

            elif clean[1] == 'PRIVMSG':
                if clean[2] != self.chan:
                    return
                try:
                    cmd = line.split(':')[2].split()[0]
                    arg = line.split(':')[2][len(cmd)+1:]
                    self._handle_commands(cmd, arg)
                except:
                    pass
        except Exception, err:
            pass

    def _handle_commands(self, cmd, arg):
        if cmd == '!stato':
            gcount = len(Globals.Backlog)
            fcount = len(Globals.Config['CustomFilter'])
            self.sendirc('%d giveaway nel backlog, %d filtri attivi' % (gcount, fcount))

        elif cmd == '!poff':
            self.sendirc('*poff*')
            self.stop()

        elif cmd == '!salva':
            self.u.save_config()
            self.sendirc('configurazione salvata')

        elif cmd == '!filtra':
            if len(arg) < 4:
                self.sendirc('uso: !filtra <almeno 5 char porco dio>')
                return
            if arg not in Globals.Config['CustomFilter']:
                Globals.Config['CustomFilter'].append(arg)
                count = len(Globals.Config['CustomFilter'])
                self.sendirc('%s filtrato, %d filtri attivi.' % (arg, count))
            else:
                self.sendirc('%s e\' gia\' nei filtri.' % arg)

        elif cmd == '!filtri':
            count = len(Globals.Config['CustomFilter'])
            filtri = ', '.join(Globals.Config['CustomFilter'])
            self.sendirc('%d filtri attivi: %s.' % (count, filtri))

        elif cmd == '!rimuovi':
            if len(arg) < 4:
                self.sendirc('uso: !rimuovi <filtro|tutti>')
                return

            if arg == 'tutti':
                del Globals.Config['CustomFilter'][:]
                self.sendirc('rimossi tutti i filtri.')

            elif arg in Globals.Config['CustomFilter']:
                Globals.Config['CustomFilter'].remove(arg)
                self.sendirc('%s rimosso dai filtri.' % arg)

            else:
                self.sendirc('non ho trovato %s nei filtri.' % arg)
                return

            self.u.save_config()
