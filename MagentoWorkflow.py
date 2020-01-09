import sublime
import sublime_plugin

from .app.app import App
from .app.thread_wrapper import ThreadWrapper
from .app.thread_progress import ThreadProgress


def get_app(view):
    return App(
        view.file_name(),
        view.window().extract_variables().get('folder')
    )


def run(object, method, args=None):
    thread = ThreadWrapper(object, method, args)
    thread.start()
    ThreadProgress(thread)


class NameInputHandler(sublime_plugin.TextInputHandler):
    def __init__(self, placeholder, initial_text):
        self._placeholder = placeholder
        self._initial_text = initial_text

    def placeholder(self):
        return self._placeholder

    def initial_text(self):
        return self._initial_text


class ClearCacheCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        app = get_app(self.view)
        if app.workdir:
            run(app, 'clear_cache', ['All'])


class ClearSelectedCacheCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.app = get_app(self.view)
        if self.app.workdir is None:
            return
        self.view.window().show_quick_panel(
            self.app.cache.type(),
            self.on_done,
            sublime.KEEP_OPEN_ON_FOCUS_LOST
        )

    def on_done(self, index):
        if index == -1:
            return
        caches = [self.app.cache.type(index), 'full_page']
        run(self.app, 'clear_cache', [caches])


class FlushCacheCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        app = get_app(self.view)
        if app.workdir:
            run(app, 'flush_cache')


class CleanupModuleCommand(sublime_plugin.TextCommand):
    def run(self, edit, name):
        self.app.package.type = 'module'
        self.app.package.code = name
        run(self.app, 'cleanup', [name])

    def input(self, args):
        self.app = get_app(self.view)

        initial_value = 'Magento_Catalog'
        if self.app.package.type is 'module':
            initial_value = self.app.package.code

        return NameInputHandler('Enter module name', initial_value)


class CleanupThemeCommand(sublime_plugin.TextCommand):
    def run(self, edit, name):
        self.app.package.type = 'theme'
        self.app.package.code = name
        run(self.app, 'cleanup', [name])

    def input(self, args):
        self.app = get_app(self.view)

        initial_value = 'Magento/luma'
        if self.app.package.type is 'theme':
            initial_value = self.app.package.code

        return NameInputHandler('Enter theme name', initial_value)


class CleanupOnFileSave(sublime_plugin.EventListener):
    def on_post_save_async(self, view):
        app = App(view.file_name())
        if app.package.type:
            run(app, 'sync')
            run(app, 'cleanup')
