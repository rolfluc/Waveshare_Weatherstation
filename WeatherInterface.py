import json
import urllib.request
from datetime import datetime
import os
from pathlib import PureWindowsPath
from IsPy import *

#sample query
#"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Minneapolis?unitGroup=uk&include=days%2Chours%2Ccurrent&key=________&contentType=json"

class Weather:
    BaseURL = ""
    Location = ""
    API_Key = ""
    unitString = ""
    parameterString = ""
    contentType = ""
    jsonData = ""
    precipitationTypes = [] 

    def __init__(self):
        self.BaseURL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"
        self.Location = "Minneapolis"
        self.unitString = "?unitGroup=uk"
        self.parameterString = "&include=days%2Chours%2Ccurrent"
        self.contentType = "&contentType=json"
        self.precipitationTypes = ['rain','snow','ice','freezingrain']

        try:
            cwd = ""
            if IsPi():
                cwd = os.getcwd() + "/"
            else:
                cwd = os.getcwd() + str(PureWindowsPath("\\Waveshare_Weatherstation\\")) + "\\"
            keyfile = open(cwd + "API_Key.txt","r",encoding="utf-8")
            #Assumes there is one key
            for line in keyfile:
                self.API_Key = line
            keyfile.close()
        except Exception as e:
            print("Key File Missing")
 
    def BuildQuery(self):
        retString = ""
        retString = self.BaseURL + self.Location + self.unitString + self.parameterString + "&key=" + self.API_Key + self.contentType
        return retString
    
    def GetNewTime(self):
        query = self.BuildQuery()
        try:
            URL_Response = urllib.request.urlopen(query)
        except:
            print("URL Request failed")
        if(URL_Response.getcode() == 200):
            URL_Data = URL_Response.read()
            self.jsonData = json.loads(URL_Data)
            #with open("snow_real.json", "w") as outfile:
            #    json.dump(self.jsonData,outfile)
        else:
            print("Failed to query Weather Data")

    def TestViaFile(self, filename):
        with open(filename) as f:
            self.jsonData = json.load(f)


    def ExtractInfo(self,hourData,hourIndex):
        temperature = hourData["temp"]
        precipitation = hourData["preciptype"]
        precipitation_prob = hourData["precipprob"]
        humidity = hourData["humidity"]
        condition = hourData["conditions"]
        snow = hourData["snow"]
        return tuple((temperature,humidity,condition,precipitation,precipitation_prob,snow,hourIndex))

    def GetHourly(self,day,next,isToday):
        times  = list()
        if(isToday):
            now_Hour = datetime.now().time().hour
            for hourIndex in range(now_Hour,24):
                hourData = day["hours"][hourIndex]
                tupleDat = self.ExtractInfo(hourData,hourIndex)
                times.append(tupleDat)
            for hourIndex in range(0,now_Hour):
                hourData = next["hours"][hourIndex]
                times.append(self.ExtractInfo(hourData,hourIndex))
        else:
            for hourIndex in range(0,24):
                hourData = day["hours"][hourIndex]
                times.append(self.ExtractInfo(hourData,hourIndex))
        rise = day["sunrise"]
        set = day["sunset"]
        dayDat = tuple((rise,set))
        return tuple((dayDat,times))
    
    def GetDay(self,dayIndex):
        days = self.jsonData["days"]
        return self.GetHourly(days[dayIndex],days[dayIndex+1],dayIndex==0)

    def GetToday(self):
        return self.GetDay(0)
            
    def GetTomorrow(self):
        return self.GetDay(1)

    def GetNextDay(self):
        return self.GetDay(2)
    