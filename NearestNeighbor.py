from math import sqrt

def findNearest_distance3D(pixel,colorList):
    #https://en.wikipedia.org/wiki/Nearest_neighbor_search
    minDistanceIndex = 0
    minDistance = sqrt(255*255*255)
    for x in range(0,len(colorList)):
        d = (pixel[0] - colorList[x][0]) * (pixel[0] - colorList[x][0])
        d += (pixel[1] - colorList[x][1]) * (pixel[1] - colorList[x][1])
        d += (pixel[2] - colorList[x][2]) * (pixel[2] - colorList[x][2])
        d = sqrt(d)
        if d <= minDistance:
            minDistance = d
            minDistanceIndex = x
    return colorList[minDistanceIndex]