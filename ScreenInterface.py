import os
import sys
import io
from pathlib import PureWindowsPath
from IsPy import *

#determine if running on a Pi or not. If running on a Pi, we want to use the actual EPD firmware images.
#if running on windows, or not a pi, run a PIL image

isPi = IsPi()
if isPi:
    cwd = os.getcwd()
    sys.path.append(os.getcwd())
    print(cwd)
    from epd5in65f import *

from PIL import Image,ImageDraw,ImageFont


class ScreenInterface:
    EPD_WIDTH       = 600
    EPD_HEIGHT      = 448
    screendata = ""
    Himage = ""
    font = ""
    epd = ""
    draw = ""
    #only used if not running on the pi
    buffer = ""
    cwd = ""
        
    def __init__(self):
        self.cwd = os.getcwd()
        self.Himage = Image.new('RGB', (self.EPD_WIDTH, self.EPD_HEIGHT), 0xffffff)  # 255: clear the frame
        self.font = ""
        if isPi:
            self.epd = EPD()
            self.epd.init()
            self.epd.Clear()
            with open("Font.txt") as f:
                txt = f.readline()
                fle = self.cwd + txt
                self.font = ImageFont.load_default()
                #self.font = ImageFont.truetype(fle,20)
        else:
            with open(self.cwd + "\\Waveshare_Weatherstation\\Font.txt") as f:
                txt = f.readline()
                fle = self.cwd + txt
                self.font = ImageFont.load_default()
                #self.font = ImageFont.truetype(fle,20)
        self.draw = ImageDraw.Draw(self.Himage)

    def SleepScreen(self):
        if isPi:
            self.epd.sleep()

    def DrawImage(self):
        if isPi:
            self.epd.display(self.epd.getbuffer(self.Himage))
        else:
            self.Himage.show()

    def DrawIcon(self,position,dataBuffer, doDraw):
        #TODO this is not defined. Examples show how to do a full image, not a 
        #epd.display(epd.getbuffer(Himage))
        #Himage = Image.open(os.path.join(picdir, '5in65f0.bmp'))
        self.Himage.paste(dataBuffer,box=(position.x,position.y))
        #if isPi:
        #    if(doDraw):
        #        self.DrawImage()
        #else:
            #Assumes the databuffer is actually a PIL image
        #    self.Himage.paste(dataBuffer,box=(position.x,position.y))
        if doDraw:
            self.DrawImage()
            