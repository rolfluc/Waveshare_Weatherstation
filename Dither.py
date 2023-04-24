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
    for y in range(0,image.height):
        for x in range(0,image.width):
            pixel = image.getpixel((x,y))
            newPixel = findNearest_distance3D(pixel,colors)
            image.putpixel((x,y),newPixel)
            err = GetError(pixel, newPixel)
            # _ _ x 7 5
            # 3 5 7 5 3
            # 1 3 5 3 1
            # diviser : 48

def ApplyStucki(image):
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

def BurckesDithering(image):
    for y in range(0,image.height):
        for x in range(0,image.width):
            pixel = image.getpixel((x,y))
            newPixel = findNearest_distance3D(pixel,colors)
            image.putpixel((x,y),newPixel)
            err = GetError(pixel, newPixel)
            # _ _ x 8 4
            # 2 4 8 4 2
            # diviser : 32

def SierraDithering(image):
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
    ApplyFloydSteinberg(image)