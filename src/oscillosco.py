import os
import time

from abc import abstractmethod, ABC

__VERSION__ = "0.1.0"

class Signal(ABC):

    @abstractmethod
    def generate(self, ticks):
        pass

class Scope(object):

    def __init__(self, signal, frames_per_second=1):
        self.fps = frames_per_second
        self.signal = signal
        self.ticker = 0

    def flow(self):
        for s in self.signal.generate(100):
            os.system("clear")
            print(s)
            time.sleep(1 / self.fps)
            self.ticker += 1
