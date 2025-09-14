import math

OFF = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (255, 0, 255)

class Mat:
    def __init__(self, w, h, def_val):
        self.HEIGHT = w
        self.WIDTH = h
        if def_val is not None:
            self.d = [[ def_val for _ in range(w)] for _ in range(h)]
    
    def get(self, x, y):
        return self.d[y][x]
    
    def set(self, x, y, v):
        self.d[y][x] = v
    
    def copy(self):
        new_mat = Mat(self.WIDTH, self.HEIGHT, None)  # temporary def_val, will be replaced
        new_mat.d = [row[:] for row in self.d]
        return new_mat
    
    def fill(self, color):
        for y in range(self.HEIGHT):
            for x in range(self.WIDTH):
                self.set(x, y, color)

    def fill_gen(self, gen):
        for y in range(self.HEIGHT):
            for x in range(self.WIDTH):
                self.set(x, y, gen())

class MatCol(Mat):
    def __init__(self, width, height):
        super().__init__(width, height, 0)
        self.fill_gen(lambda: [0,0,0])

    def fill_elem(self, v):
        for y in range(self.HEIGHT):
            for x in range(self.WIDTH):
                self.set_elem(x, y, v)

    def set_elem(self, x, y, v):
        cell = self.d[y][x]
        cell[0] = v[0]
        cell[1] = v[1]
        cell[2] = v[2]

    def add(self, x, y, v):
        cell = self.d[y][x]
        cell[0] = min(cell[0] + v[0], 255)
        cell[1] = min(cell[1] + v[1], 255)
        cell[2] = min(cell[2] + v[2], 255)


class EngBase:
    def __init__(self, width, height):
        self.WIDTH = width
        self.HEIGHT = height

    def color(self, x, y, c):
        # set color but don't don't commit to display, c is tuple of 3 numbers (r, b, g)
        pass

    def show(self):
        # commit colors to display
        pass

    def fill(self, color):
        for y in range(self.HEIGHT):
            for x in range(self.WIDTH):
                self.color(x, y, color)

    def fill_from(self, mat):
        for y in range(self.HEIGHT):
            for x in range(self.WIDTH):
                self.color(x, y, mat.get(x, y))


class HandlerBase:
    def __init__(self):
        self.eng = None
    def on_key_up(self, x, y):
        pass
    def on_key_down(self, x, y):
        pass
    def on_tick():
        # called 30 times a second
        pass


def main(handler_cls):
    import eng_sim
    eng = eng_sim.SimEng()
    eng.main(handler_cls)