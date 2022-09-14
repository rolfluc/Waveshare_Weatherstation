from genericpath import exists
from PIL import Image
import os

from enum import Enum

class MoonPhases(Enum):
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


    def __init__(self):
        self.RainName = "Rain"
        self.SnowName = "Snow"
        self.IceName = "Ice"
        self.FreezingRainName = "FreezingRain"
        self.CloudyName = "Cloudy"
        self.SunnyName = "Sunny"
        self.PartlyCloudyName = "PartlyCloudy"
        self.ThunderstormName = "Thunderstorm"
        self.MoonPhasesNames[MoonPhases.New] = "Moon_0"
        self.MoonPhasesNames[MoonPhases.WaxingCrescent] = "Moon_1"
        self.MoonPhasesNames[MoonPhases.FirstQuarter] = "Moon_2"
        self.MoonPhasesNames[MoonPhases.WaxingGibbous] = "Moon_3"
        self.MoonPhasesNames[MoonPhases.Full] = "Moon_4"
        self.MoonPhasesNames[MoonPhases.WaningGibbous] = "Moon_5"
        self.MoonPhasesNames[MoonPhases.LastQuarter] = "Moon_6"
        self.MoonPhasesNames[MoonPhases.WaningCrescent] = "Moon_7"

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

