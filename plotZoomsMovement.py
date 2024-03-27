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
startZoom = 1/ 1024
endZoom = 1 / 100000
mag = .99025
times = 0
maxIncrement = .025
crossHairs = True
display = True



xStart = -0.34515734750000004
yStart = -0.6422024474999997
xEnd = -0.3452412708398438
yEnd = -0.6425610290429684

# xStart = -0.11640740000000008
# yStart = -0.6497024999999994
# xEnd = -0.11640740000000008
# yEnd = -0.6497024999999994

#times = setTimes(startZoom, endZoom, mag)
# coords = setCoords(xStart, yStart, xEnd, yEnd, times)

coords1 = (xStart, yStart)
coords2 = (xEnd, yEnd)
coords = generateCoordsList(coords1, coords2, maxIncrement)

times = coords['frames']
print('times:', times)
end = input('ctl+c to end or enter to continue')


totalTimer = StopWatch()
totalTimer.start()

printZoomsMovement(coords, startZoom, times, MAX_ITER, WIDTH, HEIGHT, mag, crossHairs, display, directory = 'Plots')

totalTimer.stop()
print(totalTimer.lapsedTime() / 60, "minutes")
print()
print("#######################################################")
print("######################## Done #########################")
print("#######################################################")
