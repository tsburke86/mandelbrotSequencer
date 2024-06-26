from mandelbrotConfig import *


# Image size (pixels)
'''
        '1':(600,400),
        '2':(800,600),
        '3':(1200,800),
        '4':(1800,1200)
'''
WIDTH = 600
HEIGHT = 450
MAX_ITER = 750
# Give the Zooms as whole numbers ~ 32 is 32x
startZoom = 1024
endZoom =  8192
# What percent of current zoom to increase by
mag = .99025
times = 0
maxIncrement = .025
crossHairs = True
display = True

xStart = -0.7692847770693966
yStart = -0.1070103894443514


#times = setTimes(startZoom, endZoom, mag)
# coords = setCoords(xStart, yStart, xEnd, yEnd, times)

zoomList = getZooms(startZoom, endZoom, mag)
times = len(zoomList)
print('times:', times)
end = input('ctl+c to end or enter to continue')


totalTimer = StopWatch()
totalTimer.start()

printZooms(xStart, yStart, zoomList,WIDTH, HEIGHT, MAX_ITER, crossHairs, display, directory = 'Plots')
#printZoomsMovement(coords, startZoom, times, MAX_ITER, WIDTH, HEIGHT, mag, crossHairs, display, directory = 'Plots')

totalTimer.stop()
print(totalTimer.lapsedTime() / 60, "minutes")
print()
print("#######################################################")
print("######################## Done #########################")
print("#######################################################")
