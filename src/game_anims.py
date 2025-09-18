import util
import math
import colorsys
import random

def hsv_to_rgb(h, s, v):
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return int(r * 255), int(g * 255), int(b * 255)

def triangle_wave(x: float, period: float = 2*math.pi) -> float:
    t = (x % period) / period
    if t < 0.25:
        return 4 * t
    elif t < 0.75:
        return 2 - 4 * t
    else:
        return -4 + 4 * t
    
def sawtooth_wave(x: float, period: float = 2*math.pi) -> float:
    return (x % period) / period

class AnimObj:
    def depressed():
        pass

def ramp_with_edges(delta: float, start: float, end: float, v: float) -> float:
    if v <= start or v >= end:
        return 0.0
    elif start + delta <= v <= end - delta:
        return 1.0
    elif v < start + delta:
        # Rising edge: linear from 0 → 1
        return (v - start) / delta
    else:  # v > end - delta
        # Falling edge: linear from 1 → 0
        return (end - v) / delta    
    
def clamp(mn, v, mx):
    return max(mn, min(v, mx))

class Circle(AnimObj):
    def __init__(self, x, y, max_radius=10, speed=0.2):
        self.x = x
        self.y = y
        self.hue = 0
        self.max_radius = max_radius
        self.speed = speed
        self.EDGE = 3.0
        self.outer_radius = 0
        self.is_pressed = True
        self.inner_radius = -self.EDGE*2
        self.start_v = random.random()*6

    def update(self):
        self.outer_radius += self.speed
        self.inner_radius += self.speed
        if self.is_pressed:
            self.inner_radius = min(self.inner_radius, -self.EDGE)


    def is_alive(self):
        return self.inner_radius <= 10
    
    def depressed(self):
        self.is_pressed = False

    def draw(self, d):
        for yy in range(d.HEIGHT):
            for xx in range(d.WIDTH):
                dist = math.sqrt((xx - self.x)**2 + (yy - self.y)**2)

                f = ramp_with_edges(self.EDGE, self.inner_radius, self.outer_radius, dist)
                if f == 0.0:
                    continue

                hue = sawtooth_wave((-dist + self.outer_radius + self.start_v)*0.8)
                #if xx == 0 and yy == 0:
                #    print(self.start_v, hue)
                color = hsv_to_rgb(hue, 1, 1) #(hue*255, 0, 0)
                d.add(xx, yy, (int(color[0] * f), int(color[1] * f), int(color[2] * f)))



class Circles_Handler(util.HandlerBase):
    def __init__(self, width, height):
        super().__init__()
        self.d = util.MatCol(width, height)
        
        self.objmat = util.Mat(width, height, None)
        self.objects = [] 

    def on_key_down(self, x, y):
        obj = Circle(x, y)
        self.objmat.set(x, y, obj)
        self.objects.append(obj)

    def on_key_up(self, x, y):
        obj = self.objmat.get(x, y)
        if obj is not None:
            obj.depressed()
            
    def on_tick(self):
        self.d.fill_elem([0,0,0])

        new_objects = []
        for circle in self.objects:
            circle.draw(self.d)
            circle.update()
            if circle.is_alive():
                new_objects.append(circle)
            else:
                pass
                #print("Removed")


        self.objects = new_objects
        self.eng.fill_from(self.d)
        self.eng.show()   


if __name__ == "__main__":
    util.main(Circles_Handler)