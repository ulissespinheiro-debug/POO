import math

class point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class circle:
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

def point_in_circle(c1, c2):
    dx = c2.center.x - c1.center.x
    dy = c2.center.y - c1.center.y
    distancia = math.sqrt((dx ** 2) + (dy ** 2))
    return distancia + c2.radius <= c1.radius

p = point(300, 150)
circulo1 = circle(p, 200)

p2 = point(320,160)
circulo2 = circle(p2, 50)

print(point_in_circle(circulo1, circulo2))

def rect_in_circle(circle, vertices):
    for v in vertices:
        dx = v.x - circle.center.x
        dy = v.y - circle.center.y
        distancia = math.sqrt(dx**2 + dy**2)
        if distancia > circle.radius:
            return False
    return False

c = circle(point(0,0), 10)

rect = [point(2,2), point(2,-2), point(-2,2), point(-2,-2)]

print(rect_in_circle(c, rect))