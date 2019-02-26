from .cache import Cache
from .package import Package
from .resources import Resources
from .timer import Timer
from .terminal import Terminal
from .filesystem import *


class App:
    def __init__(self, filepath, workdir=None):
        self.filepath = filepath
        self.workdir = self.find_workdir(workdir)
        self.timer = Timer()
        self.package = Package(self.filepath)
        self.terminal = Terminal(self.workdir)
        self.resources = Resources(self)
        self.cache = Cache(self)

    def find_workdir(self, fallback=None):
        workdir = closest('bin/magento', self.filepath, True)
        if fallback and workdir is None:
            workdir = closest('bin/magento', fallback, True)
        return workdir

    def cleanup(self):
        self.timer.start()
        self.resources.remove()
        self.cache.clean()
        self.timer.end()

    def clear_cache(self, type=None):
        self.timer.start()
        self.cache.clean(type)
        self.timer.end()

    def flush_cache(self):
        self.timer.start()
        self.cache.flush()
        self.timer.end()

    def elapsed(self):
        return self.timer.time()
