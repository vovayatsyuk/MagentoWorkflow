import sublime


class ThreadProgress:

    """
    Animates an indicator, [=   ], in the status area while a thread runs

    This code is taken from
        https://github.com/wbond/package_control/blob/master/package_control/thread_progress.py
    """

    def __init__(self, thread):
        self.message = 'MagentoWorkflow is working'
        self.success_message = 'MagentoWorkflow succeded in %.2f seconds'
        self.error_message = 'MagentoWorkflow errored'
        self.thread = thread
        self.addend = 1
        self.size = 8
        self.last_view = None
        self.window = None
        sublime.set_timeout(lambda: self.run(0), 100)

    def run(self, i):
        if not self.thread.is_alive():
            if hasattr(self.thread, 'result') and not self.thread.result:
                return sublime.status_message(self.error_message)
            return sublime.status_message(
                self.success_message % self.thread.elapsed()
            )

        before = i % self.size
        after = (self.size - 1) - before

        sublime.status_message(
            '%s [%s=%s]' % (self.message, ' ' * before, ' ' * after)
        )

        if not after:
            self.addend = -1
        if not before:
            self.addend = 1
        i += self.addend

        sublime.set_timeout(lambda: self.run(i), 100)
