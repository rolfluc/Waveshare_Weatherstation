from UIPositions import *
from IconInterface import *
from ScreenInterface import *
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import numpy as np
from datetime import datetime
from PIL import Image
import io

class WeatherViewer:
    PosInterpreter = PositionInterpretter()
    IconInterpreter = IconInterface()
    Screen = ScreenInterface()
    WeatherData = ""
    precipitationTypes = ['rain','snow','ice','freezingrain']
    daysOfTheWeek = ["Montag","Dienstag","Mittwoch","Donnerstag","Freitag","Samstag","Sonntag"]
    Himage = ""
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
    color_black = (0,0,0)

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

        
        #self.fig.tight_layout()
        plt.subplots_adjust(hspace=0.5)

    def DoSleep(self):
        self.Screen.SleepScreen()

    def DoShow(self):
        a = 0

    def DoDraw(self,pos,data):
        self.Screen.DrawIcon(pos,data,False)

    def DoDrawText(self,pos,text):
        self.Screen.DrawText(pos,text,False)

    def DoDrawHumidity(self,posStart,percent):
        a = 0

    def DisplayRain(self,position):
        setPos = 0
        
    def DisplaySnow(self,position):
        setPos = 0

    def DisplayIce(self,position):
        setPos = 0

    def DisplayFreezingRain(self,position):
        setPos = 0

    def DisplayCloudy(self,position):
        setPos = 0

    def DisplaySunny(self,position):
        setPos = 0

    def DisplayPartlyCloudy(self,position):
        setPos = 0
    
    def DisplayThunderstorm(self,position):
        setPos = 0

    def DisplayPrecipProbability(self,position,level):
        setPos = 0

    #Display as a bar graph
    def DisplayHumidity(self,position,level):
        setPos = 0

    #cm expected
    def DisplaySnowAmt(self,position,level):
        setPos = 0

    def DisplayFog(self,position):
        setPos = 0

    def DisplayHail(self,position):
        setPos = 0

    def DisplaySunData(self,position,rise,set):
        rise = rise[0:5] #crop the seconds off.
        set = set[0:5]

    def ManageCondition(self,position,condition,hour,phase):
        condition = condition.lower()
        #if ("snow" in condition): #Snow intentionally before rain
        #    self.DisplaySnow(position)
        #elif ("hail" in condition):
        #    self.DisplayHail(position)
        #elif ("freezing" in condition):
        #    self.DisplayFreezingRain(position)
        #elif ("drizzle" in condition or "rain" in condition):
        #    self.DisplayRain(position)
        #elif ("thunderstorm" in condition):
        #    self.DisplayThunderstorm(position)
        #elif ("ice" in condition or "hail" in condition):
        #    self.DisplayIce(position)
        #elif ("fog" in condition): #Fog before freezing 
        #    self.DisplayFog(position)
        #elif("partly cloudy" in condition):
        #    self.DisplayPartlyCloudy(position)
        #elif ("cloudy" in condition or "overcast" in condition):
        #    self.DisplayCloudy(position)
        #else:
        #    if(phase == -1): #Day Condition -1 is not a valid phase
        #        self.DisplaySunny(position)
        #    else:
        #        if(hour < 6 or hour > 20):
        #            self.DisplayMoon(position,phase)
        #        else:
        #            self.DisplaySunny(position)

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
        while currentPlot < setTime and plotIndex < len(xHours):
            if xHours[plotIndex] < setTime:
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
        additionalYRise = 0
        additionalYSet = 0

        minY = min(yDat)
        maxY = max(yDat)
        delta = maxY - minY

        if(len(plotX) > 1):
            if(displayBoth is True):
                yTarget = (abs(plotY[0]) + additionalYRise - minY) / delta
                graph.axvline(x=plotX[0]+ additionalXRise, ymin=0, ymax=yTarget,color=self.color_orange)
                #graph.plot([plotX[0] + additionalXRise, plotX[0] + additionalXRise], [plotY[0] + additionalYRise, min(yDat)],'k-', color=self.color_orange,scaley = False) 
            yTarget = (abs(plotY[len(plotY)-1]) + additionalYSet - minY) / delta
            graph.axvline(x=plotX[len(plotX)-1] + additionalXSet, ymin=0, ymax=yTarget,color=self.color_orange)
            #graph.plot([plotX[len(plotX)-1] + additionalXSet, plotX[len(plotX)-1] + additionalXSet], [plotY[len(plotY)-1] + additionalYSet, min(yDat)],'k-', color=self.color_orange, scaley = False) 

    def DisplayToday(self,hoursData):
        self.DisplayDay(hoursData,self.today)
    
    def DisplayDay(self,hoursData,graph):
        tempDat = np.zeros(dtype=np.float64,shape=len(hoursData[1]))
        humidDat = np.zeros(dtype=np.int8,shape=len(hoursData[1]))
        #conditionDat = np.empty(dtype='s256',shape=len(hoursData[1]))
        precipPercentDat = np.zeros(dtype=np.int8,shape=len(hoursData[1]))
        xAxis = [None] * 24
        xLabels = [None] * 24
        xIndex = 0
        
        for x in range(0,len(hoursData[1])):
            tempDat[x] = hoursData[1][x][0]
            humidDat[x] = hoursData[1][x][1]
            #conditionDat[x] = hoursData[1][x][2]
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
        graph.plot(tempDat, color=self.color_blue)
        
    def DisplayTomorrow(self,tmrDat):
        self.DisplayDay(tmrDat,self.tomorrowGraph)
    
    def DisplayNextDay(self,tmrDat):
        self.DisplayDay(tmrDat,self.nextGraph)

        self.fig.align_labels()
        #plt.show()

    def SendToScreen(self):
        # Save figure
        dpi = 100 # set desired dpi (dots per inch)
        width_px,height_px=(600,400) # set desired figure size in pixels (width,height)
        self.fig.set_size_inches(width_px/dpi,height_px/dpi) # convert pixel dimensions to inches and set figure size accordingly
        imageBuffer = io.BytesIO()
        plt.savefig(imageBuffer, dpi=dpi, format='jpeg') # save figure as png with specified dpi
        im = Image.open(imageBuffer)
        #todo maybe dither here.
        self.Screen.DrawIcon((Point(0,0)),im,True)
        