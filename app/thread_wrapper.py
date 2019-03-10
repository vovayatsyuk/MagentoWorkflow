from threading import Thread
from subprocess import CalledProcessError

from .timer import Timer


class ThreadWrapper(Thread):
    def __init__(self, object, method, args=None):
        Thread.__init__(self)
        self.timer = Timer()
        self.object = object
        self.method = method
        self.args = args

    def run(self):
        self.timer.start()
        try:
            func = getattr(self.object, self.method)
            if self.args:
                func(*self.args)
            else:
                func()
        except CalledProcessError as err:
            print(
                'MagentoWorkflow failed to execute: "%s"'
                % err.output
            )
        self.timer.end()

    def elapsed(self):
        return self.timer.time()
