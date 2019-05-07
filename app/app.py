import sublime
from .cache import Cache
from .docker import Docker
from .package import Package
from .resources import Resources
from .terminal import Terminal
from .filesystem import *


class App:
    def __init__(self, filepath, workdir=None):
        self.filepath = filepath
        self.settings = sublime.load_settings('MagentoWorkflow.sublime-settings')
        self.workdir = self.find_workdir(workdir)
        self.package = Package(self.filepath)
        self.terminal = Terminal(self)
        self.resources = Resources(self)
        self.cache = Cache(self)
        self.docker = Docker(self)

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

    def sync(self):
        if not self.docker.config():
            return
        command = self.settings.get('sync_command')
        folders = self.settings.get('sync_folders', [])
        for folder in folders:
            if folder in self.filepath:
                relative_path = folder + self.filepath.split(folder, 1)[1]
                relative_path = relative_path.lstrip('/')
                command = command.replace(r'{filepath}', relative_path)
                self.terminal.execute(command, self.workdir)
