from enum import IntEnum

#ScreenWIDTH       = 600
#ScreenHEIGHT      = 448

class Positions(IntEnum):
    Today = 0
    Tomorrow = 1
    Following = 2

class Point:
    x = 0
    y = 0
    def __init__(self,x_pos,y_pos):
        self.x = x_pos
        self.y = y_pos

    def Get(self):
        return tuple(self.x,self.y)


class PositionInterpretter:
    IconWidth_px = 0

    def __init__(self):
        topDefault = 0
