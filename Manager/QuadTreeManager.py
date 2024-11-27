class Quadtree:
    def __init__(self, w, h, y, x, capacity):
        self.width = w
        self.x = x
        self.y = y
        self.height = h
        self.capacity = capacity
        self.points = []
        self.divided = False

    def insert(self, point):
        if not self.contains(point):
            return
        if not(self.divided) and len(self.points) < self.capacity:
            self.points.append(point)
        else:
            if not self.divided:
                self.subdivide()
            self.northeast.insert(point)
            self.northwest.insert(point)
            self.southeast.insert(point)
            self.southwest.insert(point)

    def contains(self, point):
        return (point.x >= self.x and point.x < self.x + self.width and
                point.y >= self.y and point.y < self.y + self.height)

    def subdivide(self):
        x = self.x + self.width / 2
        y = self.y + self.height / 2
        self.northeast = Quadtree(self.x + self.width / 2, self.y, self.width / 2, self.height / 2, self.capacity)
        self.northwest = Quadtree(self.x, self.y, self.width / 2, self.height / 2, self.capacity)
        self.southeast = Quadtree(self.x + self.width / 2, self.y + self.height / 2, self.width / 2, self.height / 2, self.capacity)
        self.southwest = Quadtree(self.x, self.y + self.height / 2, self.width / 2, self.height / 2, self.capacity)
        self.divided = True
        self.points = []

    def isSubdivided(self):
        return self.divided

    def intersects(self, range):
        return not (range.x > self.x + self.width or
                    range.x + range.width < self.x or
                    range.y > self.y + self.height or
                    range.y + range.height < self.y)

    def query(self, range, level=0):
        found = []
        if not self.intersects(range):
            return found
        for p in self.points:
            if range.contains(p):
                found.append((level, p))
        if self.divided:
            found += self.northeast.query(range, level + 1)
            found += self.northwest.query(range, level + 1)
            found += self.southeast.query(range, level + 1)
            found += self.southwest.query(range, level + 1)
        return found

    def remove(self, point):
        if not self.contains(point):
            return
        if point in self.points:
            self.points.remove(point)
        elif self.divided:
            self.northeast.remove(point)
            self.northwest.remove(point)
            self.southeast.remove(point)
            self.southwest.remove(point)
        if len(self.points) == 0:
            self.divided = False

    def clear(self):
        self.points = []
        self.divided = False
        self.northeast = None
        self.northwest = None
        self.southeast = None
        self.southwest = None

class rect:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def contains(self, point):
        return (point.x >= self.x and point.x < self.x + self.width and
                point.y >= self.y and point.y < self.y + self.height)