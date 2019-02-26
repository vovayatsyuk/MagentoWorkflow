import sublime
import sublime_plugin

from subprocess import CalledProcessError
from .app.app import App


def run(object, command, args=None):
    sublime.status_message('MagentoWorkflow is working...')

    try:
        func = getattr(object, command)
        if args:
            result = func(*args)
        else:
            result = func()
        sublime.status_message(
            'MagentoWorkflow succeded in %.2f seconds'
            % object.elapsed()
        )
    except CalledProcessError as err:
        print(
            'MagentoWorkflow failed to execute: "%s"'
            % err.output
        )
        sublime.status_message(
            'MagentoWorkflow error. See more information in console'
        )

    return result


class ClearCacheCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        app = App(self.view.file_name())
        if app.workdir:
            run(app, 'clear_cache')


class ClearSelectedCacheCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.app = App(self.view.file_name())
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
        app = App(self.view.file_name())
        if app.workdir:
            run(app, 'flush_cache')


class CleanupOnFileSave(sublime_plugin.EventListener):
    def on_post_save_async(self, view):
        app = App(view.file_name())
        if app.package.type:
            run(app, 'cleanup')
