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
        sublime.active_window().show_quick_panel(
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
    def run(self, edit):
        self.app = get_app(self.view)

        initial_value = 'Magento_Catalog'
        if self.app.package.type is 'module':
            initial_value = self.app.package.code

        sublime.active_window().show_input_panel(
            'Enter module name',
            initial_value,
            self.on_done,
            None,
            None
        )

    def on_done(self, module):
        self.app.package.type = 'module'
        self.app.package.code = module
        run(self.app, 'cleanup', [module])


class CleanupThemeCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.app = get_app(self.view)

        initial_value = 'Magento/luma'
        if self.app.package.type is 'theme':
            initial_value = self.app.package.code

        sublime.active_window().show_input_panel(
            'Enter theme name',
            initial_value,
            self.on_done,
            None,
            None
        )

    def on_done(self, theme):
        self.app.package.type = 'theme'
        self.app.package.code = theme
        run(self.app, 'cleanup', [theme])


class CleanupOnFileSave(sublime_plugin.EventListener):
    def on_post_save_async(self, view):
        app = App(view.file_name())
        if app.package.type:
            run(app, 'cleanup')
