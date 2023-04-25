from NearestNeighbor import *
from PIL import Image
from PIL import ImageEnhance
from PIL import ImageDraw
import sys
from scipy.spatial import distance
from math import sqrt

colors = [
    (0,0,255),
    (0,255,0),
    (255,0,0),
    (255,255,255),
    (255,255,0),
    (255,128,0),
    (0,0,0)
]

def GetError(oldpixel,newPixel):
    return [oldpixel[0] - newPixel[0],oldpixel[1] - newPixel[1],oldpixel[2] - newPixel[2]]

def ApplyError(pixelVal, quanterr, mult):
    applied = [quanterr[0]*mult,quanterr[1]*mult,quanterr[2]*mult]
    return tuple([int(min(pixelVal[0] + applied[0],255)),int(min(pixelVal[1] + applied[1],255)),int(min(pixelVal[2] + applied[2],255))])

def PreProcessDither(image):
    for y in range(0,image.height):
        for x in range(0,image.width):
            pixel = image.getpixel((x,y))

def ApplyFloydSteinberg(image):
    for y in range(0,image.height):
        for x in range(0,image.width):
            #https://en.wikipedia.org/wiki/Floyd%E2%80%93Steinberg_dithering
            pixel = image.getpixel((x,y))
            newPixel = findNearest_distance3D(pixel,colors)
            # _ x 7
            # 3 5 1
            # diviser : 16

            image.putpixel((x,y),newPixel)
            err = GetError(pixel, newPixel)
            
            if x < image.width-1:
                upPix = image.getpixel((x+1,y))
                image.putpixel((x+1,y), ApplyError(upPix,err,(7 / 16)))

            if x > 0 and y < image.height-1:
                upPix = image.getpixel((x-1,y+1))
                image.putpixel((x-1,y+1),ApplyError(upPix,err,(3 / 16)))

            if y < image.height-1:
                upPix = image.getpixel((x,y+1))
                image.putpixel((x,y+1),ApplyError(upPix,err,(5 / 16)))

            if x < image.width-1 and y < image.height-1:
                upPix = image.getpixel((x+1,y+1))
                image.putpixel((x+1,y+1),ApplyError(upPix,err,(1 / 16)))

def ApplyJarvisJudiceNinke(image):
    row0Mults = (7/48, 5/48)
    row1Mults = (3/48, 5/48, 7/48, 5/48, 3/48)
    row2Mults = (1/48, 3/48, 5/48, 3/48, 1/48)
    for y in range(0,image.height):
        for x in range(0,image.width):
            pixel = image.getpixel((x,y))
            newPixel = findNearest_distance3D(pixel,colors)
            image.putpixel((x,y),newPixel)
            err = GetError(pixel, newPixel)
            #first row
            #go from x->x+2, or image.width-1, whichever is smaller
            startX = 0
            startReducer = 0
            endReducer = 0
            # _ _ x 7 5
            # 3 5 7 5 3
            # 1 3 5 3 1
            # diviser : 48

            if(x == image.width - 2):
                endReducer = 2
            elif(x == image.width - 1):
                endReducer = 1
            
            if(x == 0):
                startReducer = 2
                startX = 2
            elif(x == 1):
                startReducer = 1
                startX = 1

            for subX in range(0,len(row0Mults) - endReducer):
                upPix = image.getpixel((startX+x,y))
                image.putpixel((startX+x,y),ApplyError(upPix,err,row0Mults[subX]))
            #second row
            #go from x-2->x+2, or image.width-1, whichever is smaller
            if y < image.height - 1:
                for subX in range(startReducer,len(row1Mults) - endReducer):
                    upPix = image.getpixel((startX+x-2,y+1))
                    image.putpixel((startX+x-2,y+1),ApplyError(upPix,err,row1Mults[subX]))
                if y < image.height - 2:
                    #third row
                    for subX in range(startReducer,len(row2Mults) - endReducer):
                        upPix = image.getpixel((startX+x-2,y+2))
                        image.putpixel((startX+x-2,y+2),ApplyError(upPix,err,row2Mults[subX]))

            
            

def ApplyStucki(image):
    row0Mults = (8/42, 4/42)
    row1Mults = (2/42, 4/42, 8/42, 4/42, 2/42)
    row2Mults = (1/42, 2/42, 4/42, 2/42, 1/42)
    for y in range(0,image.height):
        for x in range(0,image.width):
            pixel = image.getpixel((x,y))
            newPixel = findNearest_distance3D(pixel,colors)
            image.putpixel((x,y),newPixel)
            err = GetError(pixel, newPixel)
            # _ _ x 8 4
            # 2 4 8 4 2
            # 1 2 4 2 1
            # diviser : 42
            startX = 0
            startReducer = 0
            endReducer = 0
            if(x == image.width - 2):
                endReducer = 2
            elif(x == image.width - 1):
                endReducer = 1
            
            if(x == 0):
                startReducer = 2
                startX = 2
            elif(x == 1):
                startReducer = 1
                startX = 1

            for subX in range(0,len(row0Mults) - endReducer):
                upPix = image.getpixel((startX+x,y))
                image.putpixel((startX+x,y),ApplyError(upPix,err,row0Mults[subX]))
            #second row
            #go from x-2->x+2, or image.width-1, whichever is smaller
            if y < image.height - 1:
                for subX in range(startReducer,len(row1Mults) - endReducer):
                    upPix = image.getpixel((startX+x-2,y+1))
                    image.putpixel((startX+x-2,y+1),ApplyError(upPix,err,row1Mults[subX]))
                if y < image.height - 2:
                    #third row
                    for subX in range(startReducer,len(row2Mults) - endReducer):
                        upPix = image.getpixel((startX+x-2,y+2))
                        image.putpixel((startX+x-2,y+2),ApplyError(upPix,err,row2Mults[subX]))

def BurckesDithering(image):
    row0Mults = (8/32, 4/32)
    row1Mults = (2/32, 4/32, 8/32, 4/32, 2/32)
    for y in range(0,image.height):
        for x in range(0,image.width):
            pixel = image.getpixel((x,y))
            newPixel = findNearest_distance3D(pixel,colors)
            image.putpixel((x,y),newPixel)
            err = GetError(pixel, newPixel)
            # _ _ x 8 4
            # 2 4 8 4 2
            # diviser : 32
            startX = 0
            startReducer = 0
            endReducer = 0
            if(x == image.width - 2):
                endReducer = 2
            elif(x == image.width - 1):
                endReducer = 1
            
            if(x == 0):
                startReducer = 2
                startX = 2
            elif(x == 1):
                startReducer = 1
                startX = 1

            for subX in range(0,len(row0Mults) - endReducer):
                upPix = image.getpixel((startX+x,y))
                image.putpixel((startX+x,y),ApplyError(upPix,err,row0Mults[subX]))
            #second row
            #go from x-2->x+2, or image.width-1, whichever is smaller
            if y < image.height - 1:
                for subX in range(startReducer,len(row1Mults) - endReducer):
                    upPix = image.getpixel((startX+x-2,y+1))
                    image.putpixel((startX+x-2,y+1),ApplyError(upPix,err,row1Mults[subX]))

def SierraDithering(image):
    row0Mults = (5/32, 3/32)
    row1Mults = (2/32, 4/32, 5/32, 4/32, 2/32)
    row2Mults = (2/32, 3/32, 2/32)
    for y in range(0,image.height):
        for x in range(0,image.width):
            pixel = image.getpixel((x,y))
            newPixel = findNearest_distance3D(pixel,colors)
            image.putpixel((x,y),newPixel)
            err = GetError(pixel, newPixel)
            # _ _ x 5 3
            # 2 4 5 4 2
            # _ 2 3 2 _
            # diviser : 32

def ApplyDither(image):
    #ApplyFloydSteinberg(image)
    #ApplyJarvisJudiceNinke(image) #<-Pretty bad actually
    #ApplyStucki(image)
    BurckesDithering(image)