import random
import math
import sys
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

# method to calculate euclidian distance
def euclideanDistance(item1, item2, length):
	distance = 0
	for x in range(1,length+1):
		distance += pow((item1[x] - item2[x]), 2)
	return math.sqrt(distance)

# method to get neighbours for test object
def getNeighbours(trainingSet, testItem, k, numFeatures):
	distances = []
	for x in range(len(trainingSet)):
		dist = euclideanDistance(testItem, trainingSet[x], numFeatures)
		distances.append((trainingSet[x], dist))
	distances.sort(key=operator.itemgetter(1))
	neighbours = []
	for x in range(k):
		neighbours.append(distances[x][0])
	return neighbours

# method to get classification based on neighbours
def getClassification(neighbours):
	vote = {}
	for x in range(len(neighbours)):
		response = neighbours[x][0] # type of classification
		if response in vote:
			vote[response] += 1
		else:
			vote[response] = 1
	sortVotes = sorted(vote.iteritems(), key=operator.itemgetter(1), reverse=True)
	return sortVotes[0][0]

# method to get accuracy
def getAccuracy(testSet, predictions):
	correct = 0
	for x in range(len(testSet)):
		if int(testSet[x][0]) is int(predictions[x]):
			correct += 1
	return (correct/float(len(testSet))) * 100.0

# Method to split data randomly into number of folds
def splitFoldDataset(dataSet,fold):
    foldsDataset = [];
    lengthDS =  len(dataSet)
    divDS = lengthDS / fold;
    for i in range(fold):
        foldsDataset.append(dataSet[i*divDS:(i*divDS)+divDS])
    return foldsDataset

def normalise(dataset,numFeatures):
    # Normalise dataset
    maxList=[]
    minList=[]
    for i in range(1,numFeatures+1):
        maxItem = -sys.float_info.min
        minItem = sys.float_info.max
        for data in dataset:
            if maxItem <= data[i]:
                maxItem = data[i];
            if minItem >= data[i]:
                minItem = data[i];
        maxList.append(maxItem);
        minList.append(minItem);


    for data in dataset:
        for i in range(1,numFeatures+1):
            try:
                data[i]=(data[i]-minList[i-1])/(float)(maxList[i-1]-minList[i-1]);
            except Exception: # if max - min is equal to 0
                data[i]=data[i]

    return dataset

def main():
    dataset = readDataset("epi_stroma_data.tsv"); # data for full set
    # dataset = readDataset("redv1_epi_stroma_data.tsv"); # data for subset
    numFeatures = len(dataset[0])-1
    kMax=25
    fold = 10;

    # Loop for K
    dataset = normalise(dataset,numFeatures); # 'normalise' of dataset
    for k in range(1,kMax+1,2):
        random.shuffle(dataset); # shuffle dataset after each K change
        foldedDataset = splitFoldDataset(dataset,fold)

        totalMisclassification=0
        print "K = ", k
        # Loop for fold
        for i in range(fold):
            # combine (fold-1) pieces for training set
            trainingSet = []
            for j in range(fold):
                if i!=j:
                    trainingSet += foldedDataset[j]


            # left over for test set (1 piece)
            testSet = foldedDataset[i]

            predictions=[]
            for x in range(len(testSet)):
            	neighbours = getNeighbours(trainingSet, testSet[x], k,numFeatures)
            	result = getClassification(neighbours)
            	predictions.append(result)

            misclassification = 100 - getAccuracy(testSet, predictions)
            print('Misclassifcation (Fold: ' +str(i+1)+ ' ): ' + str(misclassification) + '%')
            totalMisclassification+=misclassification

        print "----------------------------------------------"
        print 'Average Misclassifcation ( K= '+str(k)+' ) :'  + str(totalMisclassification/(float)(fold))+'%'
        print "=============================================="

main();
