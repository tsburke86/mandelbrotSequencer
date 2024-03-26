
maxIncrements = {

	"standard":
		{
			"x": .025,
			"y": .025,
			"zoom": .025,
			"frames": 0,
		},

	"fastZoom":
		{
			"x": .025,
			"y": .025,
			"zoom": .125,
			"frames": 0,
		},

}


# see how many frames this item will take.
# Later we change them all to the highest one
def generateFrameIntervals(startValue, endValue, maxIncrement=.025):

	frameIntervals = {
	    'frames': 0,
	    "maxIncrement": maxIncrement,
		'startValue': startValue,
		'endValue': endValue,
        'values': [],
    }

	valueDelta = endValue - startValue
	valueIncrement = maxIncrement * valueDelta
	frameIntervals['maxIncrement'] = valueIncrement
	frames = int(valueDelta / valueIncrement)

	while startValue < endValue:

		frameIntervals['values'].append(startValue)

		if abs(startValue + (startValue * valueIncrement)) < abs(endValue):
			startValue += valueIncrement

	frameIntervals['values'].append(endValue)
	frameIntervals['frames'] = len(frameIntervals['values'])

	return frameIntervals



# Change the increment to match the new frames
def setFrameIntervals(frameIntervals, frames):
	valueDelta = frameIntervals["endValue"] - frameIntervals["startValue"]
	valueIncrement = valueDelta / frames
 
	frameIntervals['maxIncrement'] = valueIncrement # Set maxIncrement
	startValue = frameIntervals["startValue"]
	endValue = frameIntervals["endValue"]

	while startValue < endValue:

		frameIntervals['values'].append(startValue)
		startValue += valueIncrement

	frameIntervals['values'].append(endValue)
	frameIntervals['frames'] = len(frameIntervals['values'])

	return frameIntervals






if __name__ == '__main__':
	x1 = 2
	x2 = 40
	y1 = 5
	y2 = 70


	x1 = -0.34515734750000004
	x2 = -0.3452412708398438

	y1 = -0.6422024474999997
	y2 = -0.6425610290429684

	maxIncrement = .025

	frames = False
	printList = []


	xIntervals = generateFrameIntervals(x1, x2, maxIncrement)
	yIntervals = generateFrameIntervals(y1, y2, maxIncrement)

	printList.append(yIntervals)
	printList.append(xIntervals)

	printList.sort(key=lambda x: x['frames'])

	frames = printList[0]['frames']

	for i in printList:
		i = setFrameIntervals(i, frames)
		print(i)
		print()






