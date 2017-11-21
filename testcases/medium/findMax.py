def findMax(arr):
	largestNum = -1
	for next in arr:
		if next > largestNum:
			largestNum = next
	return largestNum