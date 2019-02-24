import sublime
import sublime_plugin

from subprocess import CalledProcessError
from .app.app import App


class CleanupOnFileSave(sublime_plugin.EventListener):
    def on_post_save_async(self, view):
        app = App(view.file_name())

        if app.package.type is None:
            return

        sublime.status_message('MagentoWorkflow is working...')

        try:
            app.cleanup()
            sublime.status_message(
                'MagentoWorkflow succeded in %.2f seconds'
                % app.elapsed()
            )
        except CalledProcessError as err:
            print(
                'MagentoWorkflow failed to execute: "%s"'
                % err.output
            )
            sublime.status_message(
                'MagentoWorkflow error. See more information in console'
            )
