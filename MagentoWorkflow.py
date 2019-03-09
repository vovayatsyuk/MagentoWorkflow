import sublime
import sublime_plugin

from subprocess import CalledProcessError
from .app.app import App
from .app.progress import Progress


def get_app(view):
    return App(
        view.file_name(),
        view.window().extract_variables().get('folder')
    )


def run(object, command, args=None):
    progress = Progress('MagentoWorkflow is working')

    try:
        func = getattr(object, command)
        if args:
            result = func(*args)
        else:
            result = func()
        progress.stop(
            'MagentoWorkflow succeded in %.2f seconds'
            % object.elapsed()
        )
    except CalledProcessError as err:
        print(
            'MagentoWorkflow failed to execute: "%s"'
            % err.output
        )
        progress.stop(
            'MagentoWorkflow error. See more information in console'
        )

    return result


class ClearCacheCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        app = get_app(self.view)
        if app.workdir:
            run(app, 'clear_cache')


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
        run(self.app, 'clear_cache', [self.app.cache.type(index)])


class FlushCacheCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        app = get_app(self.view)
        if app.workdir:
            run(app, 'flush_cache')


class CleanupOnFileSave(sublime_plugin.EventListener):
    def on_post_save_async(self, view):
        app = App(view.file_name())
        if app.package.type:
            run(app, 'cleanup')
