import util
import math
import colorsys

def hsv_to_rgb(h, s, v):
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return int(r * 255), int(g * 255), int(b * 255)

class Circle:
    def __init__(self, x, y, max_radius=10, speed=0.2):
        self.x = x
        self.y = y
        self.hue = 0
        self.max_radius = max_radius
        self.speed = speed
        self.EDGE = 3.0
        self.radius = -self.EDGE

    def update(self):
        self.radius += self.speed
        #self.hue += 0.1

    def is_alive(self):
        return self.radius < self.max_radius

    def draw(self, d):
        for yy in range(d.HEIGHT):
            for xx in range(d.WIDTH):
                dist = math.sqrt((xx - self.x)**2 + (yy - self.y)**2)
                delta = abs(dist - self.radius)

                if delta < self.EDGE:  # soft edge ~2 pixels
                    # brightness factor: 1 at center of ring, 0 at edge
                    brightness = max(0.0, 1.0 - delta / self.EDGE)

                    # fade out as radius increases
                    fade = 1.0 - self.radius / self.max_radius
                    brightness *= fade
                    hue = (dist / 8)
                    color = hsv_to_rgb(hue, 1, 1)
                    d.add(xx, yy, (int(color[0] * brightness), int(color[1] * brightness), int(color[2] * brightness)))

                # Thin outline
                #if abs(dist - self.radius) < 0.5:
                #    eng.color(xx, yy, color)


class Circles_Handler(util.HandlerBase):
    def __init__(self, width, height):
        super().__init__()
        self.d = util.MatCol(width, height)
        
        self.circles = []  # list of active animations

    def on_key_down(self, x, y):
        # Start a new circle centered on key (x, y)
        self.circles.append(Circle(x, y))

    def on_tick(self):
        self.d.fill_elem([0,0,0])

        new_circles = []
        for circle in self.circles:
            circle.draw(self.d)
            circle.update()
            if circle.is_alive():
                new_circles.append(circle)

        self.circles = new_circles
        self.eng.fill_from(self.d)
        self.eng.show()   


if __name__ == "__main__":
    util.main(Circles_Handler)