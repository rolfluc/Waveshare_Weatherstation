import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)
from PIL import Image,ImageDraw,ImageFont
from waveshare_epd import epd5in65f

class ScreenInterface:
    EPD_WIDTH       = 600
    EPD_HEIGHT      = 448
    screendata = ""
    Himage = ""
    font = ""
    epd = ""
    draw = ""

    def __init__(self):
        self.Himage = Image.new('RGB', (self.EPD_WIDTH, self.EPD_HEIGHT), 0xffffff)  # 255: clear the frame
        self.font = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
        self.epd = epd5in65f.EPD()
        self.epd.init()
        self.epd.Clear()
        self.draw = ImageDraw.Draw(self.Himage)
        screendata = ""

    def DrawImage(self):
        self.epd.display(self.epd.getbuffer(self.Himage))

    def DrawRectangle(self,x,y,x_2,y_2,fillcolor)
        self.draw.rectangle((x, y, x_2, y_2), fill = fillcolor)

    def DrawIcon(self,position,dataBuffer, doDraw):
        #TODO this is not defined. Examples show how to do a full image, not a 
        #epd.display(epd.getbuffer(Himage))
        #Himage = Image.open(os.path.join(picdir, '5in65f0.bmp'))
        if(doDraw):
            self.DrawImage()

    def DrawText(self,position,text, doDraw):
        self.draw.text(position, text, font = self.font, fill = self.epd.BLACK)
        if(doDraw):
            self.DrawImage()
