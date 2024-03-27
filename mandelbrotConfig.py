from tkinter import *
import time as t
from PIL import Image, ImageDraw, ImageFont, ImageTk
from collections import defaultdict
from math import floor, ceil, log, log2
import csv
import os
from movement import *




##########################################################
##########################################################
# Config Functions

def mandelbrot(c,m):
    MAX_ITER = m
    z = 0
    n = 0
    while abs(z) <= 2 and n < MAX_ITER:
        z = z*z + c
        n += 1

    if n == MAX_ITER:
        return MAX_ITER
    
    return n + 1 - log(log2(abs(z)))

def linear_interpolation(color1, color2, t):
    return color1 * (1 - t) + color2 * t

def setMaxIter(oldValue):
    while True:
        print("Enter new Interation Value between 5-1000 (currently: "+str(oldValue)+"): ",end='')
        entry = input()
        if entry == '':continue
        try: eval(entry)
        except NameError:print("Invald input");continue
        entry = eval(entry)
        if 5 <= entry <= 1000:
            return entry
        
def setResolution(oldValue):
    res = {
        '1':(600,400),
        '2':(800,600),
        '3':(1200,800),
        '4':(1800,1200)
        }
    for key,value in res.items():print(key,value)
    
    while True:
        print("Enter the number for the new resolution (currently: "+\
              str(oldValue)+"x"+str(oldValue*.75)+"): ",end='')
        entry = str(input())
        if entry == '':continue
        
        if entry in res:
            WIDTH = res[entry][0]
            HEIGHT = res[entry][1]
            return WIDTH, HEIGHT
        else:print("Invalid input")
    
# Get coordinates, process and return list of coords to to print from
# uses the times variable for amont of coords to generate
def setCoords(xStart, yStart, xEnd, yEnd, times):

    # coords = {
    # 'x': [],
    # 'y': []
    # }


    xDelta = (xEnd - xStart) / times
    yDelta = (yEnd - yStart) / times
    x = xStart
    y = yStart
    coords = {}
    coords['x'] = []
    coords['y'] = []

    for i in range(times):
        coords['x'].append(x)
        coords['y'].append(y)
        x += xDelta
        y += yDelta

    return coords

# Set the x,y start end points based on the center pixel
def getPoints(x, y, xSpread):
    x1 = x - xSpread / 2
    x2 = x + xSpread / 2
    
    ySpread = xSpread * .75
    y1 = y - ySpread / 2
    y2 = y + ySpread / 2

    points = (x1,y1,x2,y2)
    return points, xSpread, ySpread


# Set the amount of images and their zoom ratio
# default zoom increase is mag=2

def getZooms(start, endZoom, mag):
    zoomList = [1 / start]
    while start < endZoom:
        start = start / mag
        zoomList.append(1 / start)
    zoomList.pop()
    zoomList.append(1 / endZoom)
    return zoomList

def getZoomsMovement(coords, start, times, mag):
    zoomList = [start]
    for i in range(times - 1 ):
        start = start / mag
        zoomList.append(start)
    return zoomList


def getIters(start, times, interval):
    iterList = [start]
    for i in range(times -1 ):
        start += interval
        iterList.append(start)
    return iterList


##########################################################
##########################################################
# Print Functions

def printDetails(name, X, Y, xSpread, res, printZoom,
                 iterations, precision, numbersCounted):
    p = '.'+precision+'f'
    fov = str(format(X - xSpread/2,p))+" to "+ str(format(X + xSpread/2,p))
    print("#######################################################")
    print()
    print("File Name: "+name+\
              "\n  Resolution: "+res+\
              "\n  Zoom: "+printZoom+"x"+\
              "\n  Iterations: "+iterations)
    print()
    print("Center Coordinates: X:"+str(X)+" Y:"+str(Y))
    print("X Spread: "+str(xSpread)+" | FOV = "+fov)
    print()
    print('Calculating...')
    

def printIters(X, Y, zoom, WIDTH, HEIGHT, Istart, Itimes, Iinterval, crossHairs, display):    # Change default mag interval
    iterList = getIters(Istart, Itimes, Iinterval)
    counter = 1
    for i in iterList:
        printChart(X, Y, zoom, WIDTH, HEIGHT, i, crossHairs, display, counter)
        counter +=1

# Print as many images as Ztimes.
# mag is the amount (times) to magnify each time.
#      - So mag = 2 means is gets twice as big each time
def printZooms(X, Y, zoomList, WIDTH, HEIGHT, MAX_ITER, crossHairs, display, directory = ''):    # Change default mag interval
    counter = 1
    for zoom in zoomList:
        printChart(X, Y, zoom, WIDTH, HEIGHT, MAX_ITER, crossHairs, display, counter, directory)
        counter +=1

def printZoomsMovement(coords, Zstart, times, MAX_ITER, WIDTH, HEIGHT, mag, crossHairs, display, directory = ''):
    times = coords["frames"]
    zoomList = getZoomsMovement(coords, Zstart, times, mag)
    stopWatch = StopWatch()
    counter = 1
    for i in range(times):
        stopWatch.start()
        print('printing image', i, 'of', len(zoomList))
        print()
        printChart(
            coords['x'][i],
            coords['y'][i], 
            zoomList[i],
            WIDTH,
            HEIGHT,
            MAX_ITER,
            crossHairs,
            display,
            counter,
            directory
            )
        counter +=1
        stopWatch.stop()
        print('Done in {} seconds'.format(stopWatch.lapsedTime()))
    
 
def printTime(t):
    minutes = 0
    seconds = t
    if t > 60:
        minutes = t // 60
    seconds = format(t % 60, '.4f')
    return str(minutes)+' minutes and '+seconds+' seconds.'


#              1  2  3        4     5       6          7         8          9
def printChart(X, Y, zoom, WIDTH, HEIGHT, MAX_ITER, crossHairs, display, counter=1, directory = ''):

    pathToFile = os.getcwd() + '/' + directory 
    if directory: pathToFile += '/'

    tStart = t.time() 
    points, xSpread, ySpread = getPoints(X, Y, zoom)
    printZoom = str(1 / zoom)
    start = (points[0], points[1] )
    end =   (points[2], points[3] )
    RE_START = start[0]
    IM_START = start[1]
    RE_END = end[0]
    IM_END = end[1]

    # stuff for printing        
    #font1 = ImageFont.truetype("/usr/share/fonts/gnu-free/FreeMono.ttf", 48)
    #font2 = ImageFont.truetype("/usr/share/fonts/dejavu/DejaVuSansMono.ttf", 12)
    res = str(WIDTH)+"x"+str(HEIGHT)
    numbersCounted = str(WIDTH * HEIGHT)
    iterations = str(MAX_ITER)
    if xSpread < 1:
        precision = str(len(str(xSpread))-2)
    else: precision = str(1)

    # Naming
    
    #name = 'zoom-'+printZoom+'x-'+str(counter)+'.png'
    ##name = 'iter-'+printZoom+'x-'+str(counter)+'.png'
    
    name = 'navi-'+str(counter)+'.png'
    #name = 'main-'+printZoom+'x'+res+'.png'
    printDetails(name, X, Y, xSpread, res, printZoom,
                 iterations, precision, numbersCounted)
    # Print Data on Image
    details = "File Name: "+name+\
              " | Resolution: "+res+\
              " | Zoom: "+printZoom+"x"+\
              " | Iterations: "+iterations
    coordinates = "X: "+str(X)+"  Y: "+str(Y)+\
              "    Precision: "+precision
    spreads = "X Spread: "+str(xSpread)+"   Y Spread: "+str(ySpread)
    
    histogram = defaultdict(lambda: 0)
    values = {}
    for x in range(0, WIDTH):
        for y in range(0, HEIGHT):
            # Convert pixel coordinate to complex number
            c = complex(RE_START + (x / WIDTH) * (RE_END - RE_START),
                        IM_START + (y / HEIGHT) * (IM_END - IM_START))
            # Compute the number of iterations
            m = mandelbrot(c, MAX_ITER)
            
            values[(x, y)] = m
            if m < MAX_ITER: # Test
            #if m < MAX_ITER - (MAX_ITER * .1): # Test
                histogram[floor(m)] += 1

    total = sum(histogram.values())
    hues = []
    h = 0
    for i in range(MAX_ITER):
        h += histogram[i] / total
        hues.append(h)
    hues.append(h)
     
    im = Image.new('HSV', (WIDTH, HEIGHT), (0, 0, 0))
    draw = ImageDraw.Draw(im)

    for x in range(0, WIDTH):
        for y in range(0, HEIGHT):
            m = values[(x, y)]
            # The color depends on the number of iterations    
            hue = 255 - int(255 * linear_interpolation(hues[floor(m)], hues[ceil(m)], m % 1))
            saturation = 255
            value = 255 if m < MAX_ITER else 0
            # Plot the point
            draw.point([x, y], (hue, saturation, value))
            
    #Cross Hairs
    if crossHairs:
        mag1 = .125
        X1 = (WIDTH/2-WIDTH*mag1)
        X2 = (WIDTH/2+WIDTH*mag1)
        Ycenter = HEIGHT/2
        Y1 = HEIGHT/2-HEIGHT *mag1
        Y2 = HEIGHT/2+HEIGHT*mag1
        Xcenter = WIDTH /2
        draw.line((X1, Ycenter, X2, Ycenter), fill=(0,0,255), width = 1)
        draw.rectangle((X1, Y1, X2, Y2), outline = (0,0,255))
        draw.line((Xcenter, Y1, Xcenter, Y2), fill=(0,0,255), width = 1)
      
    # Add Details
    if display:
        draw.rectangle((0, 0, WIDTH, 28), outline='black', fill='black')
        draw.text((4,0),details, (0,0,255))
        draw.text((4,14),"Coordinates: "+coordinates, (0,0,255))
    
    # save file
    im.convert('RGB').save(pathToFile+name, 'PNG')

    # print Time
    tEnd = t.time()
    tDif = tEnd - tStart
    print()
    print("Elapsed Time: "+printTime(tDif))
    print()
    print("#######################################################")
  

##########################################################
##########################################################
# CSV Functions

def saveStatsCsv(X, Y, zoom, WIDTH, HEIGHT, MAX_ITER, crossHairs, display, zoomFile):
    file_exists = os.path.isfile(zoomFile)
    with open(zoomFile, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['X', 'Y', 'Zoom', 'Width', 'Height', 'Max Iter', 'Cross Hairs', 'Display'])
        writer.writerow([X, Y, zoom, WIDTH, HEIGHT, MAX_ITER, crossHairs, display])


def loadStatsCsv(file):
    data = []
    with open(file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(dict(row))
    return data



##########################################################
##########################################################
# Windows

def displayImage(filePath, WIDTH, HEIGHT):
    window = Tk()
    window.title("Mandelbrot Navigator v4.20")
    # Left Side
    frame1 = Frame(window)
    frame1.pack(side = LEFT)

    # Right Side
    frame2 = Frame(window)
    frame2.pack(side = RIGHT)
    # Image 1
    canvas1 = Canvas(frame2, width = WIDTH, height = HEIGHT)  
    canvas1.pack()  
    img1 = ImageTk.PhotoImage(Image.open(filePath+"navi-1.png"))  
    canvas1.create_image(10, 10, anchor=NW, image=img1)
    # Image 2
    canvas2 = Canvas(frame2, width = WIDTH, height = HEIGHT)  
    canvas2.pack(side = BOTTOM)  
    img2 = ImageTk.PhotoImage(Image.open(filePath+"navi-2.png"))  
    canvas2.create_image(10, 10, anchor=NW, image=img2)

    window.mainloop()


##########################################################
##########################################################
# Misc

class StopWatch():

    def __init__(self):
        self.startTime = str()
        self.stopTime = str()

    def start(self):
        import time
        self.startTime = time.time()

    def stop(self):
        import time
        self.stopTime = time.time()

    def lapsedTime(self):
        sec = self.stopTime - self.startTime
        return sec


