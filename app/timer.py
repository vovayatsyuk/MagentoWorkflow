import time


class Timer:
    def __init__(self):
        self.startTime = 0
        self.elapsed = 0

    def start(self):
        self.startTime = time.time()

    def end(self):
        self.elapsed += time.time() - self.startTime

    def time(self):
        return self.elapsed
