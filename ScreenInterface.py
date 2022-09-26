import os
import sys
import io
from pathlib import PureWindowsPath

#determine if running on a Pi or not. If running on a Pi, we want to use the actual EPD firmware images.
#if running on windows, or not a pi, run a PIL image

isPi = False
osval = os.name
if osval == 'posix':
    try:
        with io.open('/proc/cpuinfo','r') as cpuinfo:
            for line in cpuinfo:
                if line.startswith('Hardware'):
                    if "BCM" in line:
                        isPi = True
                        break
    except Exception:
        isPi = False

if isPi:
    cwd = os.getcwd()
    picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
    libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'Waveshare')
    if os.path.exists(libdir):
        sys.path.append(libdir)
    sys.path.append(cwd + "/Waveshare/")
    print(cwd + "/Waveshare/")
    from waveshare_epd import epd5in65f

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
        self.cwd = os.getcwd() + str(PureWindowsPath("\\Waveshare_Weatherstation\\")) + "\\"
        self.Himage = Image.new('RGB', (self.EPD_WIDTH, self.EPD_HEIGHT), 0xffffff)  # 255: clear the frame
        self.font = ""
        if isPi:
            self.font = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
            self.epd = epd5in65f.EPD()
            self.epd.init()
            self.epd.Clear()
        else:
            #todo temporary:
            with open(self.cwd + "Font.txt") as f:
                txt = f.readline()
                fle = self.cwd + txt
                self.font = ImageFont.truetype(fle,20)
        self.draw = ImageDraw.Draw(self.Himage)

    def DrawImage(self):
        if isPi:
            self.epd.display(self.epd.getbuffer(self.Himage))
        else:
            self.Himage.show()

    def DrawRectangle(self,x,y,x_2,y_2,fillcolor,doDraw):
        if isPi:
            self.draw.rectangle((x, y, x_2, y_2), fill = fillcolor)
        else:
            rect = ImageDraw.Draw(self.Himage)
            rect.rectangle((x, y, x_2, y_2), fill = fillcolor)
            if doDraw:
                self.DrawImage()


    def DrawIcon(self,position,dataBuffer, doDraw):
        #TODO this is not defined. Examples show how to do a full image, not a 
        #epd.display(epd.getbuffer(Himage))
        #Himage = Image.open(os.path.join(picdir, '5in65f0.bmp'))
        if isPi:
            if(doDraw):
                self.DrawImage()
        else:
            #Assumes the databuffer is actually a PIL image
            self.Himage.paste(dataBuffer,box=(position.x,position.y))
            if doDraw:
                self.DrawImage()

    def DrawText(self,position,input, doDraw):
        if isPi:
            self.draw.text(position, input, font = self.font, fill = self.epd.BLACK)
            if(doDraw):
                self.DrawImage()
        else:
            self.draw.text(xy=(position.x,position.y),text=input,font=self.font,align="center",fill="black")
            if doDraw:
                self.DrawImage()
