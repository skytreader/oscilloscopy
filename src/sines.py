from .oscillosco import Signal, Scope

import math

__VERSION__ = "0.1.0"

class Sine(Signal):

    def __init__(self, y_lattice_length=4, x_lattice_length=4, max_x=8, wait_input=False):
        # How many rows until we get one lattick unit of the y-axis
        self.y_lattice_length = y_lattice_length
        # How many characters until we get one lattick unit of the x-axis
        self.x_lattice_length = x_lattice_length
        self.max_x = max_x
        self.wait_input = wait_input

        self.frame_size = max_x * x_lattice_length
        self.window = []
        self.tick = 0

    def __draw_line(self, lineno):
        """
        lineno is 0-indexed
        """
        bufr = []
        is_upper_half = lineno < self.y_lattice_length
        y_unit = 1 / self.y_lattice_length
        if is_upper_half:
            y_val_range_hi = 1 - (lineno * y_unit)
            y_val_range_lo = 1 - ((lineno + 1) * y_unit)

            for val in self.window:
                if y_val_range_lo <= val <= y_val_range_hi:
                    bufr.append("*")
                else:
                    bufr.append(" ")

            bufr.insert(len(bufr) // 2, "|")
        elif lineno == (self.y_lattice_length):
            for val in self.window:
                bufr.append("-")
        else:
            y_val_range_hi = (lineno - self.y_lattice_length) * -y_unit
            y_val_range_lo = (lineno + 1 - self.y_lattice_length) * -y_unit

            for val in self.window:
                if y_val_range_lo <= val <= y_val_range_hi:
                    bufr.append("*")
                else:
                    bufr.append(" ")

            bufr.insert(len(bufr) // 2, "|")

        return "".join(bufr)


    def draw_graph(self):
        height = (self.y_lattice_length * 2) + 1
        bufr = [self.__draw_line(n) for n in range(height)]
        bufr.append("Phase Shift: " + str(self.phase_shift))
        bufr.append("Tick: " + str(self.tick))
        return "\n".join(bufr)
    
    def __make_noise(self):
        self.phase_shift = (math.pi / self.x_lattice_length) * self.tick
        self.window = [math.sin(((ix * math.pi) / self.x_lattice_length) + self.phase_shift) for ix in range(self.frame_size)]
        return self.draw_graph()

    def generate(self, ticks):
        while self.tick < ticks:
            yield self.__make_noise()
            if self.wait_input:
                cmd = input("scroll: ").lower()
                if cmd == "j":
                    self.tick += 1
                elif cmd == "k":
                    self.tick -= 1
            else:
                self.tick += 1

if __name__ == "__main__":
    Scope(Sine(wait_input=True)).flow()
