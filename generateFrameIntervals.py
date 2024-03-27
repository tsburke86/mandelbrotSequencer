
maxIncrements = {

	"standard":
		{
			"x": .025,
			"y": .025,
			"zoom": .0125,
			"frames": 0,
			"MAX_ITER": .2,
		},

	"fastZoom":
		{
			"x": .025,
			"y": .025,
			"zoom": .125,
			"frames": 0,
			"MAX_ITER": .2,
		},

}


# see how many frames this item will take.
# Later we change them all to the highest one
def generateFrameIntervals(startValue, endValue, name, maxIncrement, integer):

	frameIntervals = {
		"name": name,
	    'frames': 0,
	    "maxIncrement": maxIncrement,
		'startValue': startValue,
		'endValue': endValue,
        'values': [],
        'integerValues': integer # bool
    }

	valueDelta = endValue - startValue # 252
	valueIncrement = maxIncrement * valueDelta #1.625
	frameIntervals['maxIncrement'] = valueIncrement
	frameIntervals['frames'] = int(valueDelta / maxIncrement)

	while startValue < endValue:

		if frameIntervals['integerValues'] == True:
			frameIntervals['values'].append(int(startValue))
		else:
			frameIntervals['values'].append(startValue)
		startValue += valueIncrement

	frameIntervals['values'].pop()
	frameIntervals['values'].append(endValue)
	frameIntervals['frames'] = len(frameIntervals['values'])

	return frameIntervals



# Change the increment to match the new frames
def setFrameIntervals(frameIntervals, frames):
	frameIntervals["values"] = []
	valueDelta = frameIntervals["endValue"] - frameIntervals["startValue"]
	valueIncrement = valueDelta / frames
 
	frameIntervals['maxIncrement'] = valueIncrement # Set maxIncrement
	startValue = frameIntervals["startValue"]
	endValue = frameIntervals["endValue"]

	while startValue < endValue:

		if frameIntervals['integerValues'] == True:
			frameIntervals['values'].append(int(startValue))
		else:
			frameIntervals['values'].append(startValue)
		startValue += valueIncrement

	frameIntervals['values'].pop()
	frameIntervals['values'].append(endValue)
	frameIntervals['frames'] = len(frameIntervals['values'])

	return frameIntervals






if __name__ == '__main__':
	x1 = 2
	x2 = 40

	y1 = 5
	y2 = 70

	zoom1 = 4
	zoom2 = 256

	iter1 = 200
	iter2 = 750


	# x1 = -0.34515734750000004
	# x2 = -0.3452412708398438

	# y1 = -0.6422024474999997
	# y2 = -0.6425610290429684

	maxIncrement = .0125

	frames = False
	printList = []


	xIntervals = generateFrameIntervals(x1, x2, 'x', maxIncrements['standard']['x'], integer=False)
	yIntervals = generateFrameIntervals(y1, y2, 'y', maxIncrements['standard']['y'], integer=False)

	zoomIntervals = generateFrameIntervals(zoom1, zoom2, 'zoom', maxIncrements['standard']['zoom'], integer=False)
	iterIntervals = generateFrameIntervals(iter1, iter2, 'MAX_ITER', maxIncrements['standard']['MAX_ITER'], integer=True)


	printList.append(zoomIntervals)
	printList.append(yIntervals)
	printList.append(xIntervals)
	printList.append(iterIntervals)



	for i in printList:
		print()
		print(i['name'],i['frames'])

	printList.sort(key=lambda x: x['frames'], reverse = True)
	print(printList[0]['name'],printList[0]['frames'])

	frames = printList[0]['frames']

	for i in printList:
		print()
		#print(i['name'],i['frames'])

		if i['frames'] < frames:
			i = setFrameIntervals(i, frames)

			print(i['name'],i['frames'])
			print(i['values'])
			print()
		# print()
		# print()






