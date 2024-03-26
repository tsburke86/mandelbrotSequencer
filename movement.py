
def generateCoordsList(coords1, coords2, maxIncrement=.025):
	'''(x1, y1), (x2, y2)'''

	# coords1 = (600, 400)
	# coords2 = (700, 700)

	coords = {
        'x': [],
        'y': [],
        'frames': 0
    }


	x1 = coords1[0]
	y1 = coords1[1]

	x2 = coords2[0]
	y2 = coords2[1]

	xDelta = x2 - x1
	yDelta = y2 - y1


	xIncrement = maxIncrement * xDelta
	yIncrement = maxIncrement * yDelta
	coordsList = [] # save the coords for each frame
	frames = 0 # Max number of frames for the movement


	xImages = int(xDelta / xIncrement)
	yImages = int(yDelta / yIncrement) 


	# Set spreads and frames
	if yImages < xImages:
		yIncrement -= (yImages / xImages) * yIncrement
		frames = xImages

	elif xImages < yImages:
		xIncrement -= (xImages / yImages) * xIncrement
		frames = yImages

	else:
		frames = yImages
	coords['frames'] = frames

	for i in range(frames + 1):


		coords['x'].append(x1)
		coords['y'].append(y1)


		if abs(x1 + (x1 * xIncrement)) < abs(x2):
			x1 += xIncrement
		if abs(y1 + (y1 * yIncrement)) < abs(y2):
			y1 += yIncrement


	coords['x'].append(x2)
	coords['y'].append(y2)
	coords['frames'] = len(coords['x'])

	return coords

if __name__ == '__main__':

	x1 = -0.34515734750000004
	x2 = -0.3452412708398438

	y1 = -0.6422024474999997
	y2 = -0.6425610290429684
	coords1 = (x1, y1)
	coords2 = (x2, y2)
	d = generateCoordsList(coords1, coords2)
	print(d)



