from UIPositions import *
from IconInterface import *
from ScreenInterface import *
import numpy as np
from datetime import datetime
from PIL import Image
import io
from Dither import *

class WeatherViewer:
    IconInterpreter = IconInterface()
    Screen = ScreenInterface()
    WeatherData = ""
    precipitationTypes = ['rain','snow','ice','freezingrain']
    daysOfTheWeek = ["Montag","Dienstag","Mittwoch","Donnerstag","Freitag","Samstag","Sonntag"]
    Himage = ""
    trackingCondition = ''
    HumidityBarWidth_px = 10
    Humidity_SaturatedHeight_px = 100
    img = Image.new('RGB', (ScreenWIDTH, ScreenHEIGHT), 'white')
    d = ImageDraw.Draw(img)
    tickFont = ImageFont.truetype("times.ttf", 12)
    titlefont = ImageFont.truetype("times.ttf", 24)

    color_blue = (0,0,255/255)
    color_green = (0,255/255,0)
    color_red = (255/255,0,0)
    color_white = (255/255,255/255,255/255)
    color_yellow = (255/255,255/255,0)
    color_orange = (255/255,128/255,0)
    alphaBlueDisplayColor = (128/255,128/255,255/255)
    color_black = (0,0,0)
    rainNp = ''
    snowNp = ''
    FRainNp = ''
    fogNp = ''
    hailNp = ''
    ThunderstormNp = ''
    heute = 0
    morgan = 0
    ubermorgan = 0

    def __init__(self):
        self.heute = datetime.today().weekday()

        self.morgan = self.heute + 1
        if self.morgan > 6:
            self.morgan = 0

        self.ubermorgan = self.morgan + 1
        if self.ubermorgan > 6:
            self.ubermorgan = 0

        #rainImage = Image.open('rain_smol.bmp')
        #tmpNp = np.array(rainImage)
        #self.rainNp = np.zeros(tmpNp.shape[:2], dtype=np.bool8)
        #self.rainNp[tmpNp[..., 0] < 0.5] = True

        #snowImage = Image.open('Snow_smol.bmp')
        #tmpNp = np.array(snowImage)
        #self.snowNp = np.zeros(tmpNp.shape[:2], dtype=np.bool8)
        #self.snowNp[tmpNp[..., 0] < 0.5] = True

        #FRainImage = Image.open('FreezingRain.bmp')
        #tmpNp = np.array(FRainImage)
        #self.FRainNp = np.zeros(tmpNp.shape[:2], dtype=np.bool8)
        #self.FRainNp[tmpNp[..., 0] < 0.5] = True

        #ThunderstormImage = Image.open('Thunder_smol.bmp')
        #tmpNp = np.array(ThunderstormImage)
        #self.ThunderstormNp = np.zeros(tmpNp.shape[:2], dtype=np.bool8)
        #self.ThunderstormNp[tmpNp[..., 0] < 0.5] = True

        #fogImage = Image.open('fog_smol.bmp')
        #tmpNp = np.array(fogImage)
        #self.fogNp = np.zeros(tmpNp.shape[:2], dtype=np.bool8)
        #self.fogNp[tmpNp[..., 0] < 0.5] = True

        #hailImage = Image.open('Hail_smol.bmp')
        #tmpNp = np.array(hailImage)
        #self.hailNp = np.zeros(tmpNp.shape[:2], dtype=np.bool8)
        #self.hailNp[tmpNp[..., 0] < 0.5] = True
        
    def DoSleep(self):
        self.Screen.SleepScreen()

    def DrawOnGraph(self,xPositions,yPositions,boolArray,graph):
        blackDisplayColor = (0,0,0)
        xy = self.getDrawXY(xPositions,yPositions)
        a = boolArray.shape[0]
        image = np.zeros((a,a,3))
        for y in range(boolArray.shape[0]):
            for x in range(boolArray.shape[1]):
                if boolArray[y][x]:
                    image[y][x] = blackDisplayColor
                else:
                    image[y][x] = self.alphaBlueDisplayColor

        

    def getDrawXY(self,xPositions,yPositions):
        middleX = xPositions[int(len(xPositions) / 2)]
        #len of 2 looks better going left->right instead of on the rightmost boundry.
        yVal =  (yPositions[middleX] + max(yPositions)) / 2
        if(len(xPositions) == 2):
            middleX = middleX - 0.5
        return ((middleX,yVal))

    def DisplayRain(self,graph,xPositions,yPositions):
        self.DrawOnGraph(xPositions,yPositions,self.rainNp,graph)
        
    def DisplaySnow(self,graph,xPositions,yPositions):
        self.DrawOnGraph(xPositions,yPositions,self.snowNp,graph)

    def DisplayIce(self,graph,xPositions,yPositions):
        self.DisplayFreezingRain(graph,xPositions,yPositions)

    def DisplayFreezingRain(self,graph,xPositions,yPositions):
        self.DrawOnGraph(xPositions,yPositions,self.FRainNp,graph)

    def DisplayThunderstorm(self,graph,xPositions,yPositions):
        self.DrawOnGraph(xPositions,yPositions,self.ThunderstormNp,graph)

    def DisplayFog(self,graph,xPositions,yPositions):
        self.DrawOnGraph(xPositions,yPositions,self.fogNp,graph)

    def DisplayHail(self,graph,xPositions,yPositions):
        self.DrawOnGraph(xPositions,yPositions,self.hailNp,graph)

    def DisplayCondition(self,graph,conditionArray,precipDat,precipChance,yDat):
        isOpen = False
        yDelta = max(yDat) - min(yDat)
        conditionXPositions = []*0
        conditionYPositions = []*0
        for index in range(0,len(conditionArray)):
            condFound = False
            condition = conditionArray[index]
            if precipDat[index] is not None and precipChance[index] >= 25.0:
                condition = condition + precipDat[index]
            if ("snow" in condition): #Snow intentionally before rain
                condFound = True
                self.trackingCondition = self.DisplaySnow
            elif ("hail" in condition):
                condFound = True
                self.trackingCondition = self.DisplayHail
            elif ("freezing" in condition):
                condFound = True
                self.trackingCondition = self.DisplayFreezingRain
            elif ("drizzle" in condition or "rain" in condition):
                condFound = True
                self.trackingCondition = self.DisplayRain
            elif ("thunderstorm" in condition):
                condFound = True
                self.trackingCondition = self.DisplayThunderstorm
            elif ("ice" in condition or "hail" in condition):
                condFound = True
                self.trackingCondition = self.DisplayIce
            elif ("fog" in condition): 
                condFound = True
                self.trackingCondition = self.DisplayFog
            if(condFound):
                conditionXPositions.append(index)
                if(not isOpen):
                    #found a condition, and not currently tracking a condition
                    isOpen = True
                    graph.axvline(x=index, ymin=min(((yDat[index]-min(yDat)) / yDelta) + 0.025,0.95), ymax=1,color=self.color_blue)
                #otherwise, we want to add the other y axis
            else:
                if(isOpen):
                    #no longer seeing the condition, drop out
                    isOpen = False
                    conditionXPositions.append(index)
                    graph.axvline(x=index, ymin=min(((yDat[index]-min(yDat)) / yDelta) + 0.025,0.95), ymax=1,color=self.color_blue)
                    for xpos in conditionXPositions:
                        conditionYPositions.append(yDat[xpos])
                    #draw existing shading, reset
                    graph.fill_between(conditionXPositions, conditionYPositions, max(yDat), facecolor=self.color_blue, alpha=0.5)   
                    if len(conditionXPositions) > 1:
                        self.trackingCondition(graph,conditionXPositions,yDat)

                    self.trackingCondition = ''
                    conditionXPositions = []*0
                    conditionYPositions = []*0
                else:
                    #ensure tracking condition is cleared
                    self.trackingCondition = ''
                # If no condition found, and not tracking one, no worries!
        #if didn't close the last one, end here:
        if(isOpen):
            graph.axvline(x=len(conditionArray)-1, ymin=min(((yDat[len(conditionArray)-1]-min(yDat)) / yDelta),0.95), ymax=1,color=self.color_blue)
            if len(conditionXPositions) > 1:
                self.trackingCondition(graph,conditionXPositions,yDat)
        # now draw
        for xpos in conditionXPositions:
            conditionYPositions.append(yDat[xpos])
        graph.fill_between(conditionXPositions, conditionYPositions, max(yDat), facecolor=self.color_blue, alpha=0.5)
                    

    def GetMinMax(self,hoursData):
        minVal = 200
        minIndex = 0
        maxVal = -200
        maxIndex = 0
        for x in range(0,len(hoursData[1])):
            tmp = hoursData[1][x][0] 
            if (tmp > maxVal):
                maxVal = tmp
                maxIndex = x
            if (tmp < minVal):
                minVal = tmp
                minIndex = x
        return tuple((tuple((minVal,minIndex)),tuple((maxVal,maxIndex))))
    
    def GetHourFractionFromTime(self,hourString):
        hourDat = hourString.split(':')
        hour = int(hourDat[0])
        minute = int(hourDat[1])
        fraction = float(hour) + (float(minute) / 60.0)
        return fraction


    def PlotSunData(self,topleft,bottomright,rise,set,xHours,xspan):
        firstHour = xHours[0]
        displayBoth = True
        riseTime = self.GetHourFractionFromTime(rise)
        setTime = self.GetHourFractionFromTime(set)
        riseFound = False
        riseX = 0
        setX = 0

        #if the set time is before the first hour, do not display
        if (setTime < firstHour):
            return
        
        #if the rise time is after the first hour on the plot, find the first hour to plot on
        if(riseTime < firstHour):
            displayBoth = False
        else:
            displayBoth = True

        # find the x target, and just draw the line from top to bottom.
        # Iterate over the list until an hour greater is found. Once greater, find the fraction in the middle, 
        # and use xspan to find the exact x location.
        for x in range(0,len(xHours)):
            if(displayBoth):
                if(xHours[x] > riseTime and not riseFound):
                    if x == 0:
                        print("Error condition")
                    riseX = xspan * x + ((riseTime - int(riseTime)) * xspan) + topleft[0]
                    riseFound = True
            if(xHours[x] > setTime):
                if x == 0:
                    print("Error condition")
                setX = xspan * (x-1) + ((setTime - int(setTime)) * xspan) + topleft[0]
                break

        if(displayBoth is True):
            self.d.line([(riseX,topleft[1]),(riseX,bottomright[1])],fill='blue')
        self.d.line([(setX,topleft[1]),(setX,bottomright[1])],fill='blue')

    def GetLinePoint(self,yDat,ytop,ybot,ytopVal,ybotVal,index,xspacing,xStart):
        xPos = int(xStart + index*xspacing)
        percent = abs(yDat - ybotVal) / (ytopVal - ybotVal)
        yPos = int(percent * (ytop - ybot) + ybot)
        return (xPos,yPos)

    
    def DisplayDay(self,hoursData,topleft,bottomright):
        tempDat = [None] * len(hoursData[1])
        humidDat = [None] * len(hoursData[1])
        conditionDat = [None] * len(hoursData[1])
        precipDat = [None] * len(hoursData[1])
        precipPercentDat =  [None] * len(hoursData[1])
        xLabels = [None] * len(hoursData[1])
        points = [None] * len(hoursData[1])
        hourDat = [None] * len(hoursData[1])
        xIndex = 0

        x1 = topleft[0]
        x2 = bottomright[0]
        y1 = topleft[1]
        y2 = bottomright[1]
        tick_spacing = (x2 - x1) / 24
        
        
        for x in range(0,len(hoursData[1])):
            tempDat[x] = hoursData[1][x][0]
            humidDat[x] = hoursData[1][x][1]
            conditionDat[x] = hoursData[1][x][2].lower()
            precipDat[x] = hoursData[1][x][3]
            precipPercentDat[x] = hoursData[1][x][4]
            hourDat[x] = hoursData[1][x][6]
            if x % 4 == 0:
                xLabels[xIndex] = str(hoursData[1][x][6])
                xIndex = xIndex + 1
            else:
                xLabels[xIndex] = str("")
                xIndex = xIndex + 1

        for j in range(len(xLabels)):
            x = x1 + j * tick_spacing
            self.d.line([(x, y2), (x, y2 + 10)], fill='black')

            # Draw the number below the tick
            self.d.text((x, y2 + 20), xLabels[j], fill='black', anchor='ms', font=self.tickFont)
        yAxisTickLeft = x1 - 5
        yAxisTickRight = x1 + 1
        topTick = y1 + 5
        botTick = y2 - 5
        midTick = (y2 + y1) / 2
        self.d.line([(yAxisTickLeft,topTick),(yAxisTickRight,topTick)],fill='black')
        self.d.line([(yAxisTickLeft,midTick),(yAxisTickRight,midTick)],fill='black')
        self.d.line([(yAxisTickLeft,botTick),(yAxisTickRight,botTick)],fill='black')

        minmax = self.GetMinMax(hoursData)
        minTemp = minmax[0][0]
        midTemp = (minmax[0][0]+minmax[1][0])/2
        maxTemp = minmax[1][0]
        self.d.text((yAxisTickLeft - 6, topTick-1), str(maxTemp).rjust(4), fill='black', anchor='ms', font=self.tickFont)
        self.d.text((yAxisTickLeft - 6, botTick-1), str(minTemp).rjust(4), fill='black', anchor='ms', font=self.tickFont)
        self.d.text((yAxisTickLeft - 6, midTick-1), "{:.1f}".format(midTemp).rjust(4), fill='black', anchor='ms', font=self.tickFont)
        index = 0 
        for each in tempDat:
            points[index] = self.GetLinePoint(each,y1+5,y2-5,maxTemp,minTemp,index,tick_spacing,x1)
            index += 1 
        for x in range(0,len(points) - 1):
            self.d.line([points[x],points[x+1]],fill='black')

        self.PlotSunData(topleft,bottomright,hoursData[0][0],hoursData[0][1],hourDat,tick_spacing)

    def DisplayToday(self,hoursData):
        self.d.rectangle([PositionInterpretter.GetTodayTopLeft(),PositionInterpretter.GetTodayBottomRight()],outline='black')
        self.DisplayDay(hoursData,PositionInterpretter.GetTodayTopLeft(),PositionInterpretter.GetTodayBottomRight())
        self.d.text(((PositionInterpretter.GetTodayTopLeft()[0] + PositionInterpretter.GetTodayBottomRight()[0]) / 2, PositionInterpretter.GetTodayTopLeft()[1] - 10), self.daysOfTheWeek[self.heute], fill='black', anchor='ms', font=self.titlefont)
        
    def DisplayTomorrow(self,tmrDat):
        self.d.rectangle([PositionInterpretter.GetTomorrowTopLeft(),PositionInterpretter.GetTomorrowBottomRight()],outline='black')
        self.DisplayDay(tmrDat,PositionInterpretter.GetTomorrowTopLeft(),PositionInterpretter.GetTomorrowBottomRight())
        self.d.text(((PositionInterpretter.GetTomorrowTopLeft()[0] + PositionInterpretter.GetTomorrowBottomRight()[0]) / 2, PositionInterpretter.GetTomorrowTopLeft()[1] - 10), self.daysOfTheWeek[self.morgan], fill='black', anchor='ms', font=self.titlefont)
    
    def DisplayNextDay(self,tmrDat):
        self.d.rectangle([PositionInterpretter.GetNextTopLeft(),PositionInterpretter.GetNextBottomRight()],outline='black')
        self.DisplayDay(tmrDat,PositionInterpretter.GetNextTopLeft(),PositionInterpretter.GetNextBottomRight())
        self.d.text(((PositionInterpretter.GetNextTopLeft()[0] + PositionInterpretter.GetNextBottomRight()[0]) / 2, PositionInterpretter.GetNextTopLeft()[1] - 10), self.daysOfTheWeek[self.ubermorgan], fill='black', anchor='ms', font=self.titlefont)


    def SendToScreen(self):
        # Save figure, with specific DPI and size
        self.img.show()   