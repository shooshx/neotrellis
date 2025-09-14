import util

class Paint_Handler(util.HandlerBase):
    def __init__(self, width, height):
        super().__init__()
        self.d = util.Mat(width, height, 0)
        self.COLORS = [util.OFF, util.RED, util.GREEN, util.BLUE, util.YELLOW, util.CYAN, util.PURPLE] 

    def tick(self, time_elapsed):
        pass

    def on_key_down(self, x, y):
        idx = self.d.get(x, y)
        idx = (idx + 1) % len(self.COLORS)
        self.d.set(x, y, idx)
        self.eng.color(x, y, self.COLORS[idx])
        self.eng.show()


if __name__ == "__main__":
    util.main(Paint_Handler)


