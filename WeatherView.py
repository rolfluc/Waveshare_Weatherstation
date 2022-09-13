from cgi import test
from turtle import setpos
from UIPositions import *
from IconInterface import *
from ScreenInterface import *

picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')

class WeatherViewer:
    PosInterpreter = PositionInterpretter()
    IconInterpreter = IconInterface()
    Screen = ScreenInterface()
    WeatherData = ""
    precipitationTypes = ['rain','snow','ice','freezingrain']
    Himage = ""

    def __init__(self):
        testWorked = self.IconInterpreter.DirTest()
        if(not testWorked):
            print("Exiting as necessary files don't")
            exit()

    def DoDraw(self,pos,data):
        self.Screen.DrawIcon(pos,data,False)

    def DoDrawText(self,pos,text):
        self.Screen.DrawIcon(pos,text,False)

    def DoDrawHumidity(self,posStart,percent):
        self.Screen.Draw

    def DisplayRain(self,position):
        setPos = self.PosInterpreter.ResolvePosition(position,SubPositions.Icon)
        data = self.IconInterpreter.GetRainImage()
        self.DoDraw(setPos,data)
        
    def DisplaySnow(self,position):
        setPos = self.PosInterpreter.ResolvePosition(position,SubPositions.Icon)
        data = self.IconInterpreter.GetSnowImage()
        self.DoDraw(setPos,data)

    def DisplayIce(self,position):
        setPos = self.PosInterpreter.ResolvePosition(position,SubPositions.Icon)
        data = self.IconInterpreter.GetIceImage()
        self.DoDraw(setPos,data)

    def DisplayFreezingRain(self,position):
        setPos = self.PosInterpreter.ResolvePosition(position,SubPositions.Icon)
        data = self.IconInterpreter.GetFreezingRainImage()
        self.DoDraw(setPos,data)

    def DisplayCloudy(self,position):
        setPos = self.PosInterpreter.ResolvePosition(position,SubPositions.Icon)
        data = self.IconInterpreter.GetCloudyImage()
        self.DoDraw(setPos,data)

    def DisplaySunny(self,position):
        setPos = self.PosInterpreter.ResolvePosition(position,SubPositions.Icon)
        data = self.IconInterpreter.GetSunnyImage()
        self.DoDraw(setPos,data)

    def DisplayPartlyCloudy(self,position):
        setPos = self.PosInterpreter.ResolvePosition(position,SubPositions.Icon)
        data = self.IconInterpreter.GetPartlyCloudyImage()
        self.DoDraw(setPos,data)
    
    def DisplayThunderstorm(self,position):
        setPos = self.PosInterpreter.ResolvePosition(position,SubPositions.Icon)
        data = self.IconInterpreter.GetThunderstormImage()
        self.DoDraw(setPos,data)

    def DisplayMoon(self,position,level):
        setPos = self.PosInterpreter.ResolvePosition(position,SubPositions.Icon)
        data = self.IconInterpreter.GetMoonImage(level) 
        self.DoDraw(setPos,data)

    def DisplayMinTemp(self,position,level):
        setPos = self.PosInterpreter.ResolvePosition(position,SubPositions.SubTemperature)
        displayText = level + u"°C"
        self.DoDrawText(setPos,displayText)

    #Acts doubly as Max temp
    def DisplayTemp(self,position,level):
        setPos = self.PosInterpreter.ResolvePosition(position,SubPositions.Temperature)
        displayText = level + u"°C"
        self.DoDrawText(setPos,displayText)

    def DisplayPrecipProbability(self,position,level):
        setPos = self.PosInterpreter.ResolvePosition(position,SubPositions.PrecipitationChance)
        displayText = level + "%"
        self.DoDrawText(setPos,displayText)

    #Display as a bar graph
    def DisplayHumidity(self,position,level):
        setPos = self.PosInterpreter.ResolvePosition(position,SubPositions.Humidity)
        self.DoDrawHumidity(setPos,level)

    #cm expected
    def DisplaySnowAmt(self,position,level):
        setPos = self.PosInterpreter.ResolvePosition(position,SubPositions.PercipitationAmount)
        displayText = level + "cm"
        self.DoDrawText(setPos,displayText)

    def DisplaySunData(self,position,rise,set):
        setPos = self.PosInterpreter.ResolvePosition(position,SubPositions.PercipitationAmount)
        setPos2 = self.PosInterpreter.ResolvePosition(position,SubPositions.PercipitationAmount)
        displayText = rise
        self.DoDrawText(setPos,displayText)
        displayText = set
        self.DoDrawText(setPos2,displayText)


    def DisplayHours(self,hoursData):
        CurrentPos = Positions.Hour_0
        for x in range(0,len(hoursData)):
            curHour = hoursData[x]
            temperature = curHour[0]
            precipitation = curHour[3]
            precipitation_prob = curHour[4]
            humidity = curHour[1]
            condition = curHour[2]
            snow = curHour[5]

            self.DisplayTemp(Positions.Tomorrow,temperature)
            self.DisplayHumidity(humidity)
            self.DisplayPrecipProbability(precipitation_prob)
            #TODO display precipitation
            #TODO display conditions
            #TODO selectively Display snow

            CurrentPos = CurrentPos + 1

        
    def DisplayTomorrow(self,tmrDat):
        maxTemp = tmrDat[0]
        minTemp = tmrDat[1]
        sunrise = tmrDat[2]
        sunset = tmrDat[3]
        precipitation = tmrDat[4]
        snow = tmrDat[5]

        self.DisplayTemp(Positions.Tomorrow,maxTemp)
        self.DisplayMinTemp(Positions.Tomorrow,minTemp)
        self.DisplaySunData(Positions.Tomorrow,sunrise,sunset)

        #TODO display precipitation
        #TODO display conditions
        #TODO selectively Display snow
    
    def DisplayNextDay(self,tmrDat):
        maxTemp = tmrDat[0]
        minTemp = tmrDat[1]
        sunrise = tmrDat[2]
        sunset = tmrDat[3]
        precipitation = tmrDat[4]
        snow = tmrDat[5]

        self.DisplayTemp(Positions.Tomorrow,maxTemp)
        self.DisplayMinTemp(Positions.Tomorrow,minTemp)
        self.DisplaySunData(Positions.Tomorrow,sunrise,sunset)
        #TODO display precipitation
        #TODO display conditions
        #TODO selectively Display snow
    