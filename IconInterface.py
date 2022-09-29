from PIL import Image
import os
from enum import IntEnum
from pathlib import PureWindowsPath
from IsPy import *

isPi = IsPi()

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
    HailName = ""
    FogName = ""
    MoonPhasesNames  = ["","","","","","","",""]
    FileType = ".bmp"
    cwd = ""


    def __init__(self):
        self.cwd = "" 
        if isPi:
            self.cwd = os.getcwd() + "/"
        else:
            self.cwd = os.getcwd() + str(PureWindowsPath("\\Waveshare_Weatherstation\\")) + "\\"

        self.RainName = self.cwd + "Rain"
        self.SnowName = self.cwd + "Snow"
        self.IceName = self.cwd + "Ice"
        self.FreezingRainName = self.cwd + "FreezingRain"
        self.CloudyName = self.cwd + "Cloudy"
        self.SunnyName = self.cwd + "Sunny"
        self.PartlyCloudyName = self.cwd + "PartlyCloudy"
        self.ThunderstormName = self.cwd + "Thunderstorm"
        self.HailName = self.cwd + "Hail"
        self.FogName = self.cwd + "Fog"
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
        files = [self.RainName,self.SnowName,self.IceName,self.FreezingRainName,self.CloudyName,self.SunnyName,self.PartlyCloudyName,self.ThunderstormName,self.FogName,self.HailName]
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

    def GetMoonImage(self, phaseFloat):
        if(phaseFloat == 0):
            return self.ReadFile(self.MoonPhasesNames[MoonPhases.New] + self.FileType)
        elif(phaseFloat < 0.25):
            return self.ReadFile(self.MoonPhasesNames[MoonPhases.WaxingCrescent] + self.FileType)
        elif(phaseFloat == 0.25):
            return self.ReadFile(self.MoonPhasesNames[MoonPhases.FirstQuarter] + self.FileType)
        elif(phaseFloat < 0.5):
            return self.ReadFile(self.MoonPhasesNames[MoonPhases.WaxingGibbous] + self.FileType)
        elif(phaseFloat == 0.5):
            return self.ReadFile(self.MoonPhasesNames[MoonPhases.Full] + self.FileType)
        elif(phaseFloat < 0.75):
            return self.ReadFile(self.MoonPhasesNames[MoonPhases.WaningGibbous] + self.FileType)
        elif(phaseFloat == 0.75):
            return self.ReadFile(self.MoonPhasesNames[MoonPhases.LastQuarter] + self.FileType)
        else:
            return self.ReadFile(self.MoonPhasesNames[MoonPhases.WaningCrescent] + self.FileType)
        

    def GetHailImage(self):
        return self.ReadFile(self.HailName + self.FileType)

    def GetFogImage(self):
        return self.ReadFile(self.FogName + self.FileType)