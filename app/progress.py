import sublime


class Progress:

    running = False

    def __init__(self, msg):
        if Progress.running:
            return

        Progress.running = True
        self.message = msg
        self.addend = 1
        self.size = 8
        self.stopped = False
        sublime.set_timeout(lambda: self.run(0), 100)

    def run(self, i):
        if self.stopped:
            Progress.running = False
            sublime.status_message(self.message)
            return

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

    def stop(self, msg):
        self.message = msg
        self.stopped = True
