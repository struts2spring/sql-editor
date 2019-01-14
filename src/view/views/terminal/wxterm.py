import threading
import time

import wx
import wx.py
from subprocess import Popen, PIPE
from queue import Queue, Empty

class BashProcessThread(threading.Thread):
    def __init__(self, readlineFunc):
        threading.Thread.__init__(self)

        self.readlineFunc = readlineFunc
        self.outputQueue = Queue()
        self.setDaemon(True)

    def run(self):
        while True:
            line = self.readlineFunc()
            self.outputQueue.put(line)

    def getOutput(self):
        """ called from other thread """
        lines = []
        while True:
            try:
                line = self.outputQueue.get_nowait()
                lines.append(line)
            except Empty:
                break
        return ''.join(lines)

class MyInterpretor(object):
    def __init__(self, locals, rawin, stdin, stdout, stderr):
        self.introText = "Welcome to stackoverflow bash shell"
        self.locals = locals
        self.revision = 1.0
        self.rawin = rawin
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr

        self.more = False

        # bash process
        self.bp = Popen('bash', shell=False, stdout=PIPE, stdin=PIPE, stderr=PIPE)

        # start output grab thread
        self.outputThread = BashProcessThread(self.bp.stdout.readline)
        self.outputThread.start()

        # start err grab thread
        self.errorThread = BashProcessThread(self.bp.stderr.readline)
        self.errorThread.start()

    def getAutoCompleteKeys(self):
        return [ord('\t')]

    def getAutoCompleteList(self, *args, **kwargs):
        return []

    def getCallTip(self, command):
        return ""

    def push(self, command):
        command = command.strip()
        if not command: return

        self.bp.stdin.write(command+"\n")
        # wait a bit
        time.sleep(.1)

        # print output
        self.stdout.write(self.outputThread.getOutput())

        # print error
        self.stderr.write(self.errorThread.getOutput())

app = wx.App()
frame = wx.py.shell.ShellFrame(InterpClass=MyInterpretor)
frame.Show()
app.SetTopWindow(frame)
app.MainLoop()