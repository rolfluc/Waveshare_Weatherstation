from enum import IntEnum

ScreenWIDTH       = 600
ScreenHEIGHT      = 448

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
    def GetTodayTopLeft():
        return (30,50)
    def GetTodayBottomRight():
        return (575,200)
    def GetTomorrowTopLeft():
        return (30,250)
    def GetTomorrowBottomRight():
        return (275,420)
    def GetNextTopLeft():
        return (325,250)
    def GetNextBottomRight():
        return (575,420)
