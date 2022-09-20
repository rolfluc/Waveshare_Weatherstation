from genericpath import exists
from PIL import Image
import os
from enum import IntEnum

class MoonPhases(IntEnum):
    New = 0,
    WaxingCrescent = 1,
    FirstQuarter = 2,
    WaxingGibbous = 3,
    Full = 4,
    WaningGibbous = 5,
    LastQuarter = 6,
    WaningCrescent = 7,


class IconInterface:
    RainName = ""
    SnowName = ""
    IceName = ""
    FreezingRainName = ""
    CloudyName = ""
    SunnyName = ""
    PartlyCloudyName = ""
    ThunderstormName = ""
    MoonPhasesNames  = ["","","","","","","",""]
    FileType = ".bmp"
    cwd = ""


    def __init__(self):
        self.cwd = os.getcwd() + "\\Waveshare_Weatherstation\\"
        self.RainName = self.cwd + "Rain"
        self.SnowName = self.cwd + "Snow"
        self.IceName = self.cwd + "Ice"
        self.FreezingRainName = self.cwd + "FreezingRain"
        self.CloudyName = self.cwd + "Cloudy"
        self.SunnyName = self.cwd + "Sunny"
        self.PartlyCloudyName = self.cwd + "PartlyCloudy"
        self.ThunderstormName = self.cwd + "Thunderstorm"
        self.MoonPhasesNames[MoonPhases.New] = self.cwd + "Moon_0"
        self.MoonPhasesNames[MoonPhases.WaxingCrescent] = self.cwd + "Moon_1"
        self.MoonPhasesNames[MoonPhases.FirstQuarter] = self.cwd + "Moon_2"
        self.MoonPhasesNames[MoonPhases.WaxingGibbous] = self.cwd + "Moon_3"
        self.MoonPhasesNames[MoonPhases.Full] = self.cwd + "Moon_4"
        self.MoonPhasesNames[MoonPhases.WaningGibbous] = self.cwd + "Moon_5"
        self.MoonPhasesNames[MoonPhases.LastQuarter] = self.cwd + "Moon_6"
        self.MoonPhasesNames[MoonPhases.WaningCrescent] = self.cwd + "Moon_7"
        

    def FileExists(self,name):
        exist = os.path.exists(name)
        return exist

    def ReadFile(self, name):
        exist = self.FileExists(name)
        if(not exist):
            raise Exception(name + " file does not exist.")
        dat = Image.open(name)
        return dat

    def DirTest(self):
        retVal = True
        files = [self.RainName,self.SnowName,self.IceName,self.FreezingRainName,self.CloudyName,self.SunnyName,self.PartlyCloudyName,self.ThunderstormName]
        for each in self.MoonPhasesNames:
            files.append(each)
        for each in files:
            exists = self.FileExists(each + self.FileType)
            if(not exists):
                print(each + self.FileType + " is needed for the app.")
                retVal = False
        return retVal

    def GetRainImage(self):
        return self.ReadFile(self.RainName + self.FileType)

    def GetSnowImage(self):
        return self.ReadFile(self.SnowName + self.FileType)
    
    def GetIceImage(self):
        return self.ReadFile(self.IceName + self.FileType)

    def GetFreezingRainImage(self):
        return self.ReadFile(self.FreezingRainName + self.FileType)

    def GetCloudyImage(self):
        return self.ReadFile(self.CloudyName + self.FileType)
        
    def GetSunnyImage(self):
        return self.ReadFile(self.SunnyName + self.FileType)

    def GetPartlyCloudyImage(self):
        return self.ReadFile(self.PartlyCloudyName + self.FileType)

    def GetThunderstormImage(self):
        return self.ReadFile(self.ThunderstormName + self.FileType)

    def GetMoonImage(self, tbdInput):
        #TODO input is not defined in terms of what will be passed here.
        return self.ReadFile(self.MoonPhasesNames[MoonPhases.Full] + self.FileType)

