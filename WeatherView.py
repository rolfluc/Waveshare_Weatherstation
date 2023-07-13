from UIPositions import *
from IconInterface import *
from ScreenInterface import *
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import numpy as np
from datetime import datetime
from PIL import Image
import io
from Dither import *
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

class WeatherViewer:
    PosInterpreter = PositionInterpretter()
    IconInterpreter = IconInterface()
    Screen = ScreenInterface()
    WeatherData = ""
    precipitationTypes = ['rain','snow','ice','freezingrain']
    daysOfTheWeek = ["Montag","Dienstag","Mittwoch","Donnerstag","Freitag","Samstag","Sonntag"]
    Himage = ""
    trackingCondition = ''
    HumidityBarWidth_px = 10
    Humidity_SaturatedHeight_px = 100
    fig = plt.figure()

    today = fig.add_subplot(211)
    tomorrowGraph = fig.add_subplot(223)
    nextGraph = fig.add_subplot(224)

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
    dpi = 100 # set desired dpi (dots per inch)

    def __init__(self):
        todayDay = datetime.today().weekday()

        self.today.set_title(self.daysOfTheWeek[todayDay])
        self.today.tick_params(labelsize=8)
        self.today.title.set_fontsize(14)
        #self.today.set(ylabel=None)
        #self.today.set(yticklabels=[])
        self.today.tick_params(left=False)
        #self.today.set(xlabel=None)
        #self.today.set(xticklabels=[])
        #self.today.tick_params(bottom=False)
        todayDay = todayDay + 1
        if todayDay > 6:
            todayDay = 0
        self.tomorrowGraph.set_title(self.daysOfTheWeek[todayDay])
        self.tomorrowGraph.tick_params(labelsize=8)
        self.tomorrowGraph.title.set_fontsize(14)
        #self.tomorrowGraph.set(ylabel=None)
        #self.tomorrowGraph.set(yticklabels=[])
        self.tomorrowGraph.tick_params(left=False)
        #self.tomorrowGraph.set(xlabel=None)
        #self.tomorrowGraph.set(xticklabels=[])
        #self.tomorrowGraph.tick_params(bottom=False)

        todayDay = todayDay + 1
        if todayDay > 6:
            todayDay = 0
        self.nextGraph.set_title(self.daysOfTheWeek[todayDay])
        self.nextGraph.tick_params(labelsize=8)
        self.nextGraph.title.set_fontsize(14)
        #self.nextGraph.set(ylabel=None)
        #self.nextGraph.set(yticklabels=[])
        self.nextGraph.tick_params(left=False)
        #self.nextGraph.set(xlabel=None)
        #self.nextGraph.set(xticklabels=[])
        #self.nextGraph.tick_params(bottom=False)

        rainImage = plt.imread('rain_smol.png')
        tmpNp = np.array(rainImage)
        self.rainNp = np.zeros(tmpNp.shape[:2], dtype=np.bool8)
        self.rainNp[tmpNp[..., 0] < 0.5] = True

        snowImage = plt.imread('Snow_smol.bmp')
        tmpNp = np.array(snowImage)
        self.snowNp = np.zeros(tmpNp.shape[:2], dtype=np.bool8)
        self.snowNp[tmpNp[..., 0] < 0.5] = True

        FRainImage = plt.imread('FreezingRain.png')
        tmpNp = np.array(FRainImage)
        self.FRainNp = np.zeros(tmpNp.shape[:2], dtype=np.bool8)
        self.FRainNp[tmpNp[..., 0] < 0.5] = True

        ThunderstormImage = plt.imread('Thunder_smol.png')
        tmpNp = np.array(ThunderstormImage)
        self.ThunderstormNp = np.zeros(tmpNp.shape[:2], dtype=np.bool8)
        self.ThunderstormNp[tmpNp[..., 0] < 0.5] = True

        fogImage = plt.imread('fog_smol.png')
        tmpNp = np.array(fogImage)
        self.fogNp = np.zeros(tmpNp.shape[:2], dtype=np.bool8)
        self.fogNp[tmpNp[..., 0] < 0.5] = True

        hailImage = plt.imread('Hail_smol.png')
        tmpNp = np.array(hailImage)
        self.hailNp = np.zeros(tmpNp.shape[:2], dtype=np.bool8)
        self.hailNp[tmpNp[..., 0] < 0.5] = True
        
        #self.fig.tight_layout()
        plt.subplots_adjust(hspace=0.5)

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
        
        imagebox = OffsetImage(image,zoom=0.4,dpi_cor=False,resample=False,filternorm=False)
        ab = AnnotationBbox(imagebox,xy,frameon=False)
        graph.add_artist(ab)



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


    def PlotSunData(self,graph,rise,set,xHours,yDat):
        firstHour = xHours[0]
        displayBoth = True
        riseTime = self.GetHourFractionFromTime(rise)
        setTime = self.GetHourFractionFromTime(set)
        firstPlotHour  = 0
        plotX = [None] * 0
        plotY = [None] * 0

        #if the set time is before the first hour, do not display
        if (setTime < firstHour):
            return
        
        #if the rise time is after the first hour on the plot, find the first hour to plot on
        if(riseTime < firstHour):
            displayBoth = False
            firstPlotHour = firstHour
        else:
            displayBoth = True
            firstPlotHour = riseTime

        #plotIndex = int(firstPlotHour)
        plotIndex = 0
        currentPlot = firstPlotHour
        plotDistance = 24
        #find the closest x data from xHours, and grab the Y data
        #
        for x in range(0,len(xHours)):
            if abs(xHours[x] - firstPlotHour) < plotDistance:
                plotDistance = abs(xHours[x] - firstPlotHour)
                currentPlot = xHours[x]
                plotIndex = x
        plotX.append(plotIndex)
        plotY.append(yDat[plotIndex])
        plotIndex += 1
        #from here, grab each hour, and the y data, until the setTime is reached
        while currentPlot <= int(setTime) and plotIndex < len(xHours):
            if xHours[plotIndex] < int(setTime):
                currentPlot = xHours[plotIndex]
                plotX.append(plotIndex)
                plotY.append(yDat[plotIndex])
                plotIndex += 1
            else:
                break


        #graph.fill_between(plotX,plotY,min(yDat),facecolor='gray',alpha=0.5)
        #TODO a lot of the above is now completely pointless, as just two yellow lines suffice
        #leaving for posterity

        #If nothing is populated, do not show.
        #if one thing is populated, do not care.

        #TODO get the slope of the line between [0] + 1, and end + end+1, and draw the y to that point, as a percentage of the additional.
        additionalXRise = riseTime - int(riseTime)
        additionalXSet = setTime - int(setTime)

        minY = min(yDat)
        maxY = max(yDat)
        delta = maxY - minY

        if len(plotY) > 1:
            additionalYRise = ((plotY[1] - plotY[0]) / delta) * additionalXRise/2
            additionalYSet = ((plotY[len(plotY)-2] - plotY[len(plotY)-1]) / delta)
        else:
            additionalYRise = 0
            additionalYSet = 0

        if(len(plotX) > 1):
            if(displayBoth is True):
                yTarget = (abs(plotY[0]) - additionalYRise - minY) / delta
                graph.axvline(x=plotX[0]+ additionalXRise, ymin=0, ymax=max(yTarget,0.025),color=self.color_orange)
            yTarget = (abs(plotY[len(plotY)-1]) - additionalYSet - minY) / delta
            graph.axvline(x=plotX[len(plotX)-1] + additionalXSet, ymin=0, ymax=max(yTarget,0.025),color=self.color_orange)

    def DisplayToday(self,hoursData):
        self.DisplayDay(hoursData,self.today)
    
    def DisplayDay(self,hoursData,graph):
        tempDat = np.zeros(dtype=np.float64,shape=len(hoursData[1]))
        humidDat = np.zeros(dtype=np.int8,shape=len(hoursData[1]))
        conditionDat = np.empty(dtype=object,shape=len(hoursData[1]))
        precipDat = np.empty(dtype=object,shape=len(hoursData[1]))
        precipPercentDat = np.zeros(dtype=np.int8,shape=len(hoursData[1]))
        xAxis = [None] * 24
        xLabels = [None] * 24
        xIndex = 0
        
        for x in range(0,len(hoursData[1])):
            tempDat[x] = hoursData[1][x][0]
            humidDat[x] = hoursData[1][x][1]
            conditionDat[x] = hoursData[1][x][2].lower()
            precipDat[x] = hoursData[1][x][3]
            precipPercentDat[x] = hoursData[1][x][4]
            xAxis[xIndex] = hoursData[1][x][6]
            if x % 4 == 0:
                xLabels[xIndex] = str(hoursData[1][x][6])
                xIndex = xIndex + 1
            else:
                xLabels[xIndex] = str("")
                xIndex = xIndex + 1

        xLabels[len(xLabels)-1] = hoursData[1][len(hoursData[1])-1][6]
        minmax = self.GetMinMax(hoursData)
        graph.set_yticks([minmax[0][0], minmax[1][0]])
        graph.set_yticklabels([str(minmax[0][0]) + "°C", str(minmax[1][0])+"°C"]) 
        graph.tick_params(axis='y',pad=-3)
        
        graph.set_xticks(range(len(xAxis)))
        graph.set_xticklabels(xLabels)
        self.PlotSunData(graph,hoursData[0][0], hoursData[0][1],xAxis,tempDat)
        self.DisplayCondition(graph,conditionDat,precipDat,precipPercentDat,tempDat)
        graph.plot(tempDat, color=self.color_red)
        
    def DisplayTomorrow(self,tmrDat):
        self.DisplayDay(tmrDat,self.tomorrowGraph)
    
    def DisplayNextDay(self,tmrDat):
        self.DisplayDay(tmrDat,self.nextGraph)

        self.fig.align_labels()
        #plt.show()

    def SendToScreen(self):
        # Save figure, with specific DPI and size
        width_px,height_px=(600,400) # set desired figure size in pixels (width,height)
        self.fig.set_size_inches(width_px/self.dpi,height_px/self.dpi) # convert pixel dimensions to inches and set figure size accordingly

        #do image conversion
        imageBuffer = io.BytesIO()
        #plt.show()
        plt.savefig(imageBuffer, dpi=self.dpi, format='png') 
        im = Image.open(imageBuffer)
        baseImage = im
        self.Screen.DrawIcon((Point(0,0)),im,True)

        #for x in range(0,5):
        #    im = baseImage.copy()
        #    ApplyDither(im)
        #    self.Screen.DrawIcon((Point(0,0)),im,True)
        
        