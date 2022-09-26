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
        startYPos = self.Humidity_SaturatedHeight_px + posStart.y - (percent * self.Humidity_SaturatedHeight_px / 100)
        #Add a black outline
        self.Screen.DrawRectangle(posStart.x-1,posStart.y-1,posStart.x+self.HumidityBarWidth_px+1,self.Humidity_SaturatedHeight_px + posStart.y +1,fillcolor="black",doDraw=False)
        #fill the void with white again
        self.Screen.DrawRectangle(posStart.x,posStart.y,posStart.x+self.HumidityBarWidth_px,self.Humidity_SaturatedHeight_px + posStart.y,fillcolor="white",doDraw=False)
        self.Screen.DrawRectangle(posStart.x,startYPos,posStart.x+self.HumidityBarWidth_px,self.Humidity_SaturatedHeight_px + posStart.y,fillcolor="blue",doDraw=False)

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

    def DisplayFog(self,position):
        setPos = self.PosInterpreter.ResolvePosition(position,SubPositions.Icon)
        data = self.IconInterpreter.GetFogImage()
        self.DoDraw(setPos,data)

    def DisplayHail(self,position):
        setPos = self.PosInterpreter.ResolvePosition(position,SubPositions.Icon)
        data = self.IconInterpreter.GetHailImage()
        self.DoDraw(setPos,data)

    def DisplaySunData(self,position,rise,set):
        rise = rise[0:5] #crop the seconds off.
        set = set[0:5]
        setPos = self.PosInterpreter.ResolvePosition(position,SubPositions.SunDataStart)
        setPos2 = self.PosInterpreter.ResolvePosition(position,SubPositions.SunDataStop)
        displayText = str(rise) 
        self.DoDrawText(setPos,displayText)
        displayText = str(set) 
        self.DoDrawText(setPos2,displayText)

    def ManageCondition(self,position,con,hour,phase):
        condition = con.lower()
        if ("snow" in condition): #Snow intentionally before rain
            self.DisplaySnow(position)
        elif ("fog" in condition): #Fog before freezing 
            self.DisplayFog(position)
        elif ("hail" in condition):
            self.DisplayHail(position)
        elif ("freezing" in condition):
            self.DisplayFreezingRain(position)
        elif ("drizzle" in condition or "rain" in condition):
            self.DisplayRain(position)
        elif ("thunderstorm" in condition):
            self.DisplayThunderstorm(position)
        elif ("ice" in condition or "hail" in condition):
            self.DisplayIce(position)
        elif("partially cloudy" in condition):
            self.DisplayPartlyCloudy(position)
        elif ("cloudy" in condition or "overcast" in condition):
            self.DisplayCloudy(position)
        else:
            if(phase == -1): #Day Condition -1 is not a valid phase
                self.DisplaySunny(position)
            else:
                if(hour < 6 or hour > 20):
                    self.DisplayMoon(position,phase)
                else:
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
            hour = curHour[6]
            moonphase = curHour[7]

            #Display Condition first always
            self.ManageCondition(CurrentPos,condition,hour,moonphase)
            self.DisplayTemp(CurrentPos,temperature)
            self.DisplayHumidity(CurrentPos,humidity)
            self.DisplayPrecipProbability(CurrentPos,precipitation_prob)
            self.DisplaySnowAmt(CurrentPos,snow)
            #TODO display precipitation - what to do here?
            CurrentPos = CurrentPos + 1

    def DisplayDay(self,tmrDat,position):
        maxTemp = tmrDat[0]
        minTemp = tmrDat[1]
        sunrise = tmrDat[2]
        sunset = tmrDat[3]
        precipitation = tmrDat[4]
        snow = tmrDat[5]
        condition = tmrDat[6]
        humidity = tmrDat[7]

        #Display Condition first always
        self.ManageCondition(position,condition,0,-1)
        self.DisplayTemp(position,maxTemp)
        self.DisplayMinTemp(position,minTemp)
        self.DisplaySunData(position,sunrise,sunset)
        self.DisplayHumidity(position,humidity)
        #TODO display precipitation
        #TODO display conditions
        #TODO selectively Display snow

        
    def DisplayTomorrow(self,tmrDat):
        self.DisplayDay(tmrDat,Positions.Tomorrow)
    
    def DisplayNextDay(self,tmrDat):
        self.DisplayDay(tmrDat,Positions.Following)
        self.DoShow()
    