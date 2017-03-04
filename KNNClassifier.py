import random
import math
import operator


# Method to read data from a file
def readDataset(file):
    with open(file, "r") as ins:
        array = []
        for line in ins:
            array.append(line)

    dataset = []
    for i in range(1,len(array)):
        splitLine = array[i].split('\t')
        floatLine = [ float(x) for x in splitLine ]
        dataset.append(floatLine)

    return dataset;

# Method to split data randomly into training and testing subsets
def splitDataset(dataSet,split):
    trainingSet = []
    testSet = []
    for data in dataSet:
        if random.random() < split:
	        trainingSet.append(data)
        else:
            testSet.append(data)
    return trainingSet, testSet

# method to calculate euclidian distance
def euclideanDistance(item1, item2, length):
	distance = 0
	for x in range(1,length+1):
		distance += pow((item1[x] - item2[x]), 2)
	return math.sqrt(distance)

# method to calculate neighbours
def getNeighbors(trainingSet, testInstance, k, numFeatures):
	distances = []
	for x in range(len(trainingSet)):
		dist = euclideanDistance(testInstance, trainingSet[x], numFeatures)
		distances.append((trainingSet[x], dist))
	distances.sort(key=operator.itemgetter(1))
	neighbors = []
	for x in range(k):
		neighbors.append(distances[x][0])
	return neighbors

# method to get response
def getResponse(neighbors):
	classVotes = {}
	for x in range(len(neighbors)):
		response = neighbors[x][0] # type of classification
		if response in classVotes:
			classVotes[response] += 1
		else:
			classVotes[response] = 1
	sortedVotes = sorted(classVotes.iteritems(), key=operator.itemgetter(1), reverse=True)
	return sortedVotes[0][0]

# method to get accuracy
def getAccuracy(testSet, predictions):
	correct = 0
	for x in range(len(testSet)):
		if int(testSet[x][0]) is int(predictions[x]):
			correct += 1
	return (correct/float(len(testSet))) * 100.0

dataset = readDataset("epi_stroma_data.tsv");
print "dataset", len(dataset)
print "----------------------------------------------"
trainingSet, testSet = splitDataset(dataset, 0.66)
print "trainingSet", len(trainingSet)
print "testSet", len(testSet)
print "----------------------------------------------"
numFeatures = len(dataset[0])-1
print "Number of Features: ", numFeatures
print "----------------------------------------------"
k = 25
print "k: ", k
predictions=[]
for x in range(len(testSet)):
	neighbors = getNeighbors(trainingSet, testSet[x], k,numFeatures)
	result = getResponse(neighbors)
	predictions.append(result)
	print('> predicted=' + repr(result) + ', actual=' + repr(testSet[x][0]))
accuracy = getAccuracy(testSet, predictions)
print('Accuracy: ' + repr(accuracy) + '%')
