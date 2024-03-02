class BoundBox:
    # where x1 is left coord
    # where x2 is right coord
    # where y1 is top 
    # where y2 is bottom 
    # mid is middle of bound box 
    def __init__(self, bound_box: list[float]):
        self.x1 = bound_box[0]
        self.y1 = bound_box[1]
        self.x2 = bound_box[2]
        self.y2 = bound_box[3]
        self.mid = ( (self.x1 + self.x2)/2 + (self.y1 + self.y2)/2)

    # 
    def overlaps(self, box): 
        return self.intersects((box.x1, box.y1)) or self.intersects((box.x1, box.y2)) or self.intersects((box.x2, box.y2)) or self.intersects((box.x2, box.y1))


    # self is BoundBox object  in code using for Dining table points 
    # point is comparison 
    # point[0] is x of ^^ 

    # def intersects(self, point: tuple[float]) -> bool:
    #     return point[0] > self.x1 and point[0] < self.x2 and point[1] > self.y1 and point[1] < self.y2
    
    def intersects(self, point: tuple[float]) -> bool:
        in_x_bounds = point[0] > self.x1 and point[0] < self.x2
        in_y_bounds = point[1] > self.y1 and point[1] < self.y2
        return in_x_bounds and in_y_bounds

