#Simple python implementation of a Floyd Steinberg dithering algorithm
#Takes in a color map to apply to the dithering, and an image input
#and an expected name output

from PIL import Image
from PIL import ImageEnhance
from PIL import ImageDraw
import sys
from scipy.spatial import distance
from math import sqrt
import csv

usage = '''usage: python3 fs_dither.py colorfile.dat inimage.ext outimage.ext'''

'''
if(len(sys.argv) < 4):
    print(usage)
    exit(-1)

color_name = sys.argv[1]
in_name = sys.argv[2]
out_name = sys.argv[3]
'''

color_name = "color.dat"
colors = list()

def ExtractColors(imName):
    colorPixel = (0,0,0)
    with open(imName) as colorFile:
        csvReader = csv.reader(colorFile)
        for row in csvReader:
            red = row[0]
            green = row[1]
            blue = row[2]
            colorPixel = (red,green,blue)

        colors.append(colorPixel)

color_blue = (0,0,255)
color_green = (0,255,0)
color_red = (255,0,0)
color_white = (255,255,255)
color_yellow = (255,255,0)
color_orange = (255,128,0)
color_black = (0,0,0)


colors = (color_blue,color_green,color_red,color_yellow,color_orange,color_black,color_white)

def findNearest(pixel):
    #https://en.wikipedia.org/wiki/Nearest_neighbor_search
    minDistanceIndex = 0
    minDistance = sqrt(255*255*255)
    for x in range(0,len(colors)):
        d = (pixel[0] - colors[x][0]) * (pixel[0] - colors[x][0])
        d += (pixel[1] - colors[x][1]) * (pixel[1] - colors[x][1])
        d += (pixel[2] - colors[x][2]) * (pixel[2] - colors[x][2])
        d = sqrt(d)
        if d <= minDistance:
            minDistance = d
            minDistanceIndex = x
    return colors[minDistanceIndex]

def GetError(oldpixel,newPixel):
    return [oldpixel[0] - newPixel[0],oldpixel[1] - newPixel[1],oldpixel[2] - newPixel[2]]

def ApplyError(pixelVal, quanterr, mult):
    applied = [quanterr[0]*mult,quanterr[1]*mult,quanterr[2]*mult]
    return tuple([int(min(pixelVal[0] + applied[0],255)),int(min(pixelVal[1] + applied[1],255)),int(min(pixelVal[2] + applied[2],255))])


def ValidateColors(image):
    for y in range(0,image.height):
        for x in range(0,image.width):
            pixel = fle.getpixel((x,y))
            if pixel not in colors:
                return False
    return True


in_name = 'Waveshare_Weatherstation\cloud-vector-icon.bmp'
y = 0
x = 0


try:
    fle = Image.open(in_name)
    fle.show()

    for y in range(0,fle.height):
        for x in range(0,fle.width):
            #https://en.wikipedia.org/wiki/Floyd%E2%80%93Steinberg_dithering
            pixel = fle.getpixel((x,y))
            newPixel = findNearest(pixel)

            fle.putpixel((x,y),newPixel)
            err = GetError(pixel, newPixel)
            
            if x < fle.width-1:
                upPix = fle.getpixel((x+1,y))
                fle.putpixel((x+1,y), ApplyError(upPix,err,(7 / 16)))

            if x > 0 and y < fle.height-1:
                upPix = fle.getpixel((x-1,y+1))
                fle.putpixel((x-1,y+1),ApplyError(upPix,err,(3 / 16)))

            if y < fle.height-1:
                upPix = fle.getpixel((x,y+1))
                fle.putpixel((x,y+1),ApplyError(upPix,err,(5 / 16)))

            if x < fle.width-1 and y < fle.height-1:
                upPix = fle.getpixel((x+1,y+1))
                fle.putpixel((x+1,y+1),ApplyError(upPix,err,(1 / 16)))
    
    correct = ValidateColors(fle)
    if correct: 
        fle.show()

except Exception as E:
    print("File Error")

