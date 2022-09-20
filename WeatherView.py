from cgi import test
from turtle import pos, setpos
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
    HumidityBarWidth_px = 10
    Humidity_SaturatedHeight_px = 100

    def __init__(self):
        testWorked = self.IconInterpreter.DirTest()
        if(not testWorked):
            print("Exiting as necessary files don't exist.")
            exit()

    def DoShow(self):
        self.Screen.DrawImage()

    def DoDraw(self,pos,data):
        self.Screen.DrawIcon(pos,data,False)

    def DoDrawText(self,pos,text):
        self.Screen.DrawText(pos,text,False)

    def DoDrawHumidity(self,posStart,percent):
        endYPos = posStart.y + percent * self.Humidity_SaturatedHeight_px / 100
        self.Screen.DrawRectangle(posStart.x-1,posStart.y-1,posStart.x+self.HumidityBarWidth_px+1,self.Humidity_SaturatedHeight_px + posStart.y +1,fillcolor="black",doDraw=False)
        #Add a black outline
        self.Screen.DrawRectangle(posStart.x,posStart.y,posStart.x+self.HumidityBarWidth_px,endYPos,fillcolor="blue",doDraw=False)

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
        displayText = str(level) + u"°C"
        self.DoDrawText(setPos,displayText)

    #Acts doubly as Max temp
    def DisplayTemp(self,position,level):
        setPos = self.PosInterpreter.ResolvePosition(position,SubPositions.Temperature)
        displayText = str(level) + u"°C"
        self.DoDrawText(setPos,displayText)

    def DisplayPrecipProbability(self,position,level):
        setPos = self.PosInterpreter.ResolvePosition(position,SubPositions.PrecipitationChance)
        displayText = str(level) + "%"
        self.DoDrawText(setPos,displayText)

    #Display as a bar graph
    def DisplayHumidity(self,position,level):
        setPos = self.PosInterpreter.ResolvePosition(position,SubPositions.Humidity)
        self.DoDrawHumidity(setPos,level)

    #cm expected
    def DisplaySnowAmt(self,position,level):
        setPos = self.PosInterpreter.ResolvePosition(position,SubPositions.PercipitationAmount)
        displayText = str(level) + "cm"
        if(level == 0):
            return
        self.DoDrawText(setPos,displayText)

    def DisplaySunData(self,position,rise,set):
        setPos = self.PosInterpreter.ResolvePosition(position,SubPositions.PercipitationAmount)
        setPos2 = self.PosInterpreter.ResolvePosition(position,SubPositions.PercipitationAmount)
        displayText = str(rise)
        self.DoDrawText(setPos,displayText)
        displayText = str(set)
        self.DoDrawText(setPos2,displayText)

    #todo Add Fog?
    #todo add hail?
    def ManageCondition(self,position,condition):
        conidition = condition.lower()
        if ("cloudy" in condition or "overcast" in condition):
            self.DisplayCloudy(position)
        elif ("snow" in conidition): #Snow intentionally before rain
            self.DisplaySnow(position)
        elif ("freezing" in condition):
            if("fog" not in condition):
                self.DisplayFreezingRain(position)
        elif ("drizzle" in condition or "rain" in condition):
            self.DisplayRain(position)
        elif ("thunderstorm" in condition):
            self.DisplayThunderstorm(position)
        elif ("ice" in condition or "hail" in condition):
            self.DisplayIce(position)
        else:
            #todo what is the logic here. We need to display clear skies, so sunny or moon.
            self.DisplaySunny(position)

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

            self.DisplayTemp(CurrentPos,temperature)
            self.DisplayHumidity(CurrentPos,humidity)
            self.DisplayPrecipProbability(CurrentPos,precipitation_prob)
            self.ManageCondition(CurrentPos,condition)
            self.DisplaySnowAmt(CurrentPos,snow)
            #TODO display precipitation - what to do here?
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
        #NextDay is last displayed.
        self.DoShow()
    