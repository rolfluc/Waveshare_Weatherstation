from enum import Enum
from msilib.schema import Class

#ScreenWIDTH       = 600
#ScreenHEIGHT      = 448

class Positions(Enum):
    Hour_0 = 0
    Hour_1 = 1
    Hour_2 = 2
    Tomorrow = 3
    Following = 4

class SubPositions(Enum):
    Temperature = 0
    SubTemperature = 1
    Humidity = 2
    Icon = 3
    PrecipitationChance =  4
    PercipitationAmount = 5
    SunDataStart = 6
    SunDataStop = 7
    Header = 8

class Point:
    x = 0
    y = 0
    def __init__(self,x_pos,y_pos):
        self.x = x_pos
        self.y = y_pos

    def Get(self):
        return tuple(self.x,self.y)

class PositionInterpretter:
    IconWidth_px = 160
    IconHeight_px = 100
    TopPadding_px = 40
    ElementPadding_px = 5
    TopRow_LeftPadding_px = 20
    TopRow_Icon_Padding_px = 40
    BottomRow_Icon_Padding_px = 120
    HumidityWidth = 10
    CharacterHeight_px = 25 #TODO confirm
    CharacterWidth_px = 25 #TODO confirm
    Positions_ = []
    Positions_Hour0 = [0,0,0,0,0,0,0,0,0]
    Positions_Hour1 = [0,0,0,0,0,0,0,0,0]
    Positions_Hour2 = [0,0,0,0,0,0,0,0,0]
    Positions_Tomorrow = [0,0,0,0,0,0,0,0,0]
    Positions_Following = [0,0,0,0,0,0,0,0,0]
    def __init__(self):
        topDefault = self.TopPadding_px
        leftDefault = self.TopRow_LeftPadding_px
        self.Positions_Hour0[SubPositions.Temperature] = Point(leftDefault + self.IconWidth_px/2,topDefault + self.IconHeight_px + self.ElementPadding_px)
        self.Positions_Hour0[SubPositions.SubTemperature] = Point(leftDefault + self.IconWidth_px/2,topDefault + self.IconHeight_px + self.ElementPadding_px*2 + self.HeaderHeight_px)
        self.Positions_Hour0[SubPositions.Humidity] = Point(leftDefault - self.HumidityWidth,topDefault)
        self.Positions_Hour0[SubPositions.Icon] = Point(leftDefault,topDefault)
        self.Positions_Hour0[SubPositions.PrecipitationChance] = Point(leftDefault + self.IconWidth_px - self.CharacterWidth_px*3,topDefault)
        self.Positions_Hour0[SubPositions.PercipitationAmount] = Point(leftDefault + self.IconWidth_px - self.CharacterWidth_px*4,topDefault + self.IconHeight_px - self.CharacterHeight_px)
        self.Positions_Hour0[SubPositions.SunDataStart] = Point(0,0) #Not defined for hours
        self.Positions_Hour0[SubPositions.SunDataStop] = Point(0,0) #Not defined for hours
        self.Positions_Hour0[SubPositions.Header] = Point(leftDefault + self.IconWidth_px/2,topDefault - self.CharacterHeight_px)

        leftDefault = self.TopRow_LeftPadding_px + self.IconWidth_px + self.TopRow_Icon_Padding_px
        self.Positions_Hour1[SubPositions.Temperature] = Point(leftDefault + self.IconWidth_px/2,topDefault + self.IconHeight_px + self.ElementPadding_px)
        self.Positions_Hour1[SubPositions.SubTemperature] = Point(leftDefault + self.IconWidth_px/2,topDefault + self.IconHeight_px + self.ElementPadding_px*2 + self.HeaderHeight_px)
        self.Positions_Hour1[SubPositions.Humidity] = Point(leftDefault - self.HumidityWidth,topDefault)
        self.Positions_Hour1[SubPositions.Icon] = Point(leftDefault,topDefault)
        self.Positions_Hour1[SubPositions.PrecipitationChance] = Point(leftDefault + self.IconWidth_px - self.CharacterWidth_px*3,topDefault)
        self.Positions_Hour1[SubPositions.PercipitationAmount] = Point(leftDefault + self.IconWidth_px - self.CharacterWidth_px*4,topDefault + self.IconHeight_px - self.CharacterHeight_px)
        self.Positions_Hour1[SubPositions.SunDataStart] = Point(0,0) #Not defined for hours
        self.Positions_Hour1[SubPositions.SunDataStop] = Point(0,0) #Not defined for hours
        self.Positions_Hour1[SubPositions.Header] = Point(leftDefault + self.IconWidth_px/2,topDefault - self.CharacterHeight_px)

        leftDefault = self.TopRow_LeftPadding_px + self.IconWidth_px*2 + self.TopRow_Icon_Padding_px*2
        self.Positions_Hour2[SubPositions.Temperature] = Point(leftDefault + self.IconWidth_px/2,topDefault + self.IconHeight_px + self.ElementPadding_px)
        self.Positions_Hour2[SubPositions.SubTemperature] = Point(leftDefault + self.IconWidth_px/2,topDefault + self.IconHeight_px + self.ElementPadding_px*2 + self.HeaderHeight_px)
        self.Positions_Hour2[SubPositions.Humidity] = Point(leftDefault - self.HumidityWidth,topDefault)
        self.Positions_Hour2[SubPositions.Icon] = Point(leftDefault,topDefault)
        self.Positions_Hour2[SubPositions.PrecipitationChance] = Point(leftDefault + self.IconWidth_px - self.CharacterWidth_px*3,topDefault)
        self.Positions_Hour2[SubPositions.PercipitationAmount] = Point(leftDefault + self.IconWidth_px - self.CharacterWidth_px*4,topDefault + self.IconHeight_px - self.CharacterHeight_px)
        self.Positions_Hour2[SubPositions.SunDataStart] = Point(0,0) #Not defined for hours
        self.Positions_Hour2[SubPositions.SunDataStop] = Point(0,0) #Not defined for hours
        self.Positions_Hour2[SubPositions.Header] = Point(leftDefault + self.IconWidth_px/2,topDefault - self.CharacterHeight_px)

        topDefault = self.TopPadding_px + self.IconHeight_px*2
        leftDefault = self.BottomRow_Icon_Padding_px
        self.Positions_Tomorrow[SubPositions.Temperature] = Point(leftDefault + self.IconWidth_px/2,topDefault + self.IconHeight_px + self.ElementPadding_px)
        self.Positions_Tomorrow[SubPositions.SubTemperature] = Point(leftDefault + self.IconWidth_px/2,topDefault + self.IconHeight_px + self.ElementPadding_px*2 + self.HeaderHeight_px)
        self.Positions_Tomorrow[SubPositions.Humidity] = Point(leftDefault - self.HumidityWidth,topDefault)
        self.Positions_Tomorrow[SubPositions.Icon] = Point(leftDefault,topDefault)
        self.Positions_Tomorrow[SubPositions.PrecipitationChance] = Point(leftDefault + self.IconWidth_px - self.CharacterWidth_px*3,topDefault)
        self.Positions_Tomorrow[SubPositions.PercipitationAmount] = Point(leftDefault + self.IconWidth_px - self.CharacterWidth_px*4,topDefault + self.IconHeight_px - self.CharacterHeight_px)
        self.Positions_Tomorrow[SubPositions.SunDataStart] = Point(leftDefault,topDefault) 
        self.Positions_Tomorrow[SubPositions.SunDataStop] = Point(leftDefault,topDefault + self.IconHeight_px - self.CharacterHeight_px) 
        self.Positions_Tomorrow[SubPositions.Header] = Point(leftDefault + self.IconWidth_px/2,topDefault - self.CharacterHeight_px)

        leftDefault = self.BottomRow_Icon_Padding_px + self.IconWidth_px + self.TopRow_Icon_Padding_px
        self.Positions_Following[SubPositions.Temperature] = Point(leftDefault + self.IconWidth_px/2,topDefault + self.IconHeight_px + self.ElementPadding_px)
        self.Positions_Following[SubPositions.SubTemperature] = Point(leftDefault + self.IconWidth_px/2,topDefault + self.IconHeight_px + self.ElementPadding_px*2 + self.HeaderHeight_px)
        self.Positions_Following[SubPositions.Humidity] = Point(leftDefault - self.HumidityWidth,topDefault)
        self.Positions_Following[SubPositions.Icon] = Point(leftDefault,topDefault)
        self.Positions_Following[SubPositions.PrecipitationChance] = Point(leftDefault + self.IconWidth_px - self.CharacterWidth_px*3,topDefault)
        self.Positions_Following[SubPositions.PercipitationAmount] = Point(leftDefault + self.IconWidth_px - self.CharacterWidth_px*4,topDefault + self.IconHeight_px - self.CharacterHeight_px)
        self.Positions_Following[SubPositions.SunDataStart] = Point(leftDefault,topDefault) 
        self.Positions_Following[SubPositions.SunDataStop] = Point(leftDefault,topDefault + self.IconHeight_px - self.CharacterHeight_px) 
        self.Positions_Following[SubPositions.Header] = Point(leftDefault + self.IconWidth_px/2,topDefault - self.CharacterHeight_px)

        self.Positions_ = [self.Positions_Hour0,self.Positions_Hour1,self.Positions_Hour2,self.Positions_Tomorrow,self.Positions_Following]

    def ResolvePosition(self,primarypos,secondarypos):
        return self.Positions_[primarypos][secondarypos]
