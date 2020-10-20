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


class MagentoWorkflowState():
    def __init__(self):
        self._eventListenersState = True

    def toggleEventListenersState(self):
        self._eventListenersState = not self._eventListenersState
        return self._eventListenersState

    def getEventListenersState(self):
        return self._eventListenersState


state = MagentoWorkflowState()


class NameInputHandler(sublime_plugin.TextInputHandler):
    def __init__(self, placeholder, initial_text):
        self._placeholder = placeholder
        self._initial_text = initial_text

    def placeholder(self):
        return self._placeholder

    def initial_text(self):
        return self._initial_text


class CacheInputHandler(sublime_plugin.ListInputHandler):
    def __init__(self, app):
        self.app = app

    def placeholder(self):
        return 'Cache Type'

    def list_items(self):
        caches = self.app.cache.type()
        caches.insert(0, ['All', 'All'])
        return caches


class MagentoWorkflowClearSelectedCacheCommand(sublime_plugin.TextCommand):
    def run(self, edit, cache):
        if cache != 'All':
            cache = [cache, 'full_page']

        run(self.app, 'clear_cache', [cache])

    def input(self, args):
        self.app = get_app(self.view)

        if self.app.workdir is None:
            return

        return CacheInputHandler(self.app)


class MagentoWorkflowFlushCacheCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        app = get_app(self.view)
        if app.workdir:
            run(app, 'flush_cache')


class MagentoWorkflowCleanupModuleCommand(sublime_plugin.TextCommand):
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


class MagentoWorkflowCleanupThemeCommand(sublime_plugin.TextCommand):
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


class MagentoWorkflowWipeCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        app = get_app(self.view)
        if app.workdir:
            run(app, 'wipe')


class MagentoWorkflowToggleEventListenersCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        if state.toggleEventListenersState():
            sublime.status_message('Event listeners are enabled now')
        else:
            sublime.status_message('Event listeners are disabled now')


class MagentoWorkflowEventListener(sublime_plugin.EventListener):
    def on_post_save_async(self, view):
        if not state.getEventListenersState():
            return

        app = App(view.file_name())
        if app.package.type:
            run(app, 'sync')
            run(app, 'cleanup')
        elif app.workdir:
            run(app, 'flush_cache')
