def findMostCommonNum(arr):
	highestNumCount = arr[0]
	for next in arr:
		if findNumCount(arr, next) > highestNumCount:
			highestNumCount = findNumCount
	return highestNumCount