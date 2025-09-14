import tkinter as tk
import util

MARGIN = 5
SPACING = 2


def rgb_to_color(rgb):
    r, g, b = rgb
    assert(r <= 255)
    assert(g <= 255)
    assert(b <= 255)
    return f"#{r:02x}{g:02x}{b:02x}"


class SimEng(util.EngBase):
    def __init__(self):
        util.EngBase.__init__(self, 8, 8)
        self.root = tk.Tk()
        self.root.title("Neotrellis Sim")

        self.canvas = tk.Canvas(self.root, width=600, height=600, bg="#000000", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Map from canvas item -> (row, col)
        self.item_to_cell = {}
        # Store cell color strings
        self.displayed = util.Mat(self.WIDTH, self.HEIGHT, "#000000")
        self.back_buf = util.Mat(self.WIDTH, self.HEIGHT, "#000000")

        self.canvas.bind("<Configure>", self._recreate)
        self.canvas.bind("<ButtonPress-1>", self._on_down)
        self.canvas.bind("<ButtonRelease-1>", self._on_up)

    def _recreate(self, event=None):
        """Redraw grid and rebuild mapping"""
        self.canvas.delete("all")
        self.item_to_cell.clear()

        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        rect_area_w = width - 2 * MARGIN
        rect_area_h = height - 2 * MARGIN
        rect_size_w = (rect_area_w - (self.WIDTH - 1) * SPACING) / self.WIDTH
        rect_size_h = (rect_area_h - (self.HEIGHT - 1) * SPACING) / self.HEIGHT
        self.rect_size = min(rect_size_w, rect_size_h)

        for y in range(self.HEIGHT):
            for x in range(self.WIDTH):
                x1 = MARGIN + x * (self.rect_size + SPACING)
                y1 = MARGIN + y * (self.rect_size + SPACING)
                x2 = x1 + self.rect_size
                y2 = y1 + self.rect_size
                sc = self.displayed.get(x, y)
                rect = self.canvas.create_rectangle(x1, y1, x2, y2, outline="white", fill=sc)
                self.item_to_cell[rect] = (x, y)
        self._schedule_tick()

    def _get_coord(self, event):
        item = self.canvas.find_closest(event.x, event.y)
        if not item:
            return None,None
        item_id = item[0]

        if item_id not in self.item_to_cell:
            return None,None
        
        return self.item_to_cell[item_id]

    def _on_down(self, event):
        x, y = self._get_coord(event)
        if x is None:
            return
        self.handler.on_key_down(x, y)

    def _on_up(self, event):
        x, y = self._get_coord(event)
        if x is None:
            return
        self.handler.on_key_up(x, y)

    def _schedule_tick(self):
        self.handler.on_tick()
        delay = int(1000 / 30)  # milliseconds
        self.root.after(delay, self._schedule_tick)

    def color(self, x, y, c):
        self.back_buf.set(x, y, rgb_to_color(c))
        

    def show(self):
        self.displayed = self.back_buf.copy()
        for item_id, (x, y) in self.item_to_cell.items():
            sc = self.displayed.get(x, y)
            self.canvas.itemconfig(item_id, fill=sc)     

    def main(self, handler_cls):
        self.handler = handler_cls(self.WIDTH, self.HEIGHT)
        self.handler.eng = self
        self.root.mainloop()


