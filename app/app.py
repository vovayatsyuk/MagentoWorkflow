from .cache import Cache
from .package import Package
from .resources import Resources
from .terminal import Terminal
from .filesystem import *


class App:
    def __init__(self, filepath, workdir=None):
        self.filepath = filepath
        self.workdir = self.find_workdir(workdir)
        self.package = Package(self.filepath)
        self.terminal = Terminal(self.workdir)
        self.resources = Resources(self)
        self.cache = Cache(self)

    def find_workdir(self, fallback=None):
        workdir = None
        if self.filepath:
            workdir = closest('bin/magento', self.filepath, True)
        if fallback and workdir is None:
            workdir = closest('bin/magento', fallback, True)
        return workdir

    def cleanup(self, code=None):
        self.resources.remove(code)
        self.cache.clean('All' if code else None)

    def clear_cache(self, type=None):
        self.cache.clean(type)

    def flush_cache(self):
        self.cache.flush()
