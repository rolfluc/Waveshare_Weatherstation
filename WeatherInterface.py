import json
import urllib.request
from datetime import datetime
import os
from pathlib import PureWindowsPath

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
        URL_Response = urllib.request.urlopen(query)
        if(URL_Response.getcode() == 200):
            URL_Data = URL_Response.read()
            self.jsonData = json.loads(URL_Data)
            #to dump to file:
            #with open("rain.json","w") as outfile:
            #    outfile.write(json.dumps(self.jsonData))
        else:
            print("Failed to query Weather Data")

    def TestViaFile(self, filename):
        with open(filename) as f:
            self.jsonData = json.load(f)


    def ExtractInfo(self,tmp, hour,moonphase):
        temperature = tmp["temp"]
        precipitation = tmp["preciptype"]
        precipitation_prob = tmp["precipprob"]
        humidity = tmp["humidity"]
        condition = tmp["conditions"]
        snow = tmp["snow"]
        return tuple((temperature,humidity,condition,precipitation,precipitation_prob,snow,hour,moonphase))

    def ExtractNextDayInfo(self,tmp):
        maxTemp = tmp["tempmax"]
        minTemp = tmp["tempmin"]
        sunrise = tmp["sunrise"]
        sunset = tmp["sunset"]
        precipitation = tmp["preciptype"]
        snow = tmp["snow"]
        condition = tmp["conditions"]
        humidity = tmp["humidity"]
        return tuple((maxTemp,minTemp,sunrise,sunset,precipitation,snow,condition,humidity))
    
    #Grabs the the next 3 slots, at 2 hour intervals
    def GetNextHourly(self):
        times = ["","",""]
        days = self.jsonData["days"]
        today = days[0]
        tomorrow = days[1]
        now_Hour = datetime.now().time().hour

        for i in range(0,3):
            data = ""
            if(now_Hour + i*2 > 23):
                tme = now_Hour + i*2 - 24
                tmp = tomorrow["hours"][tme]
                data = self.ExtractInfo(tmp,tme,today["moonphase"])
            else:
                tme = now_Hour + i*2
                tmp = today["hours"][tme]
                data = self.ExtractInfo(tmp,tme,today["moonphase"])
            times[i] = data
        return times
            
    def GetTomorrow(self):
        days = self.jsonData["days"]
        tomorrow = days[1]
        dayInfo = self.ExtractNextDayInfo(tomorrow)
        return dayInfo

    def GetNextDay(self):
        days = self.jsonData["days"]
        nextDay = days[2]
        dayInfo = self.ExtractNextDayInfo(nextDay)
        return dayInfo
    