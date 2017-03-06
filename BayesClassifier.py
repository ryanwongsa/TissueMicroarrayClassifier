import numpy as np
import random

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

# Method to split data randomly into number of folds
def splitFoldDataset(dataSet,fold):
    foldsDataset = [];
    lengthDS =  len(dataSet)
    divDS = lengthDS / fold;
    for i in range(fold):
        foldsDataset.append(dataSet[i*divDS:(i*divDS)+divDS])
    return foldsDataset

# method to get accuracy
def getAccuracy(testSet, predictions):
	correct = 0
	for x in range(len(testSet)):
		if int(testSet[x][0]) is int(predictions[x]):
			correct += 1
	return (correct/float(len(testSet))) * 100.0


def main():
    dataset = readDataset("epi_stroma_data.tsv"); # data for full set
    # dataset = readDataset("redv1_epi_stroma_data.tsv"); # data for subset
    numFeatures = len(dataset[0])-1


    random.shuffle(dataset); # shuffle dataset after each K change
    fold = 10;
    foldedDataset = splitFoldDataset(dataset,fold)

    totalMisclassification=0
    for i in range(fold):

        # SPLIT DATA INTO SUBSETS FOR C-FOLD
        # combine (fold-1) pieces for training set
        trainingSet = []
        for j in range(fold):
            if i!=j:
                trainingSet += foldedDataset[j]
        # left over for test set (1 piece)
        testSet = foldedDataset[i]

        parameters = {}

        # Learning stage
        for classType in range(1,3):
            data_pos=[]
            for r in range(len(trainingSet)):
                if int(trainingSet[r][0])==classType:
                    data_pos.append(trainingSet[r]);

            class_pars = {}
            class_pars['mean'] = np.array(data_pos).mean(axis=0)[1:]
            class_pars['vars'] = np.array(data_pos).var(axis=0)[1:]
            class_pars['prior'] = 1.0*len(data_pos)/len(trainingSet)
            parameters[classType] = class_pars

        # Testing stage
        predictions = [] # Predicted which class item belongs to
        for j,dataItem in enumerate(testSet):

            # Determining Likelihood for being 1
            total_like1 = 1.0
            for a,feature in enumerate(dataItem[1:]):
                total_like1 *= 1.0/(np.sqrt(2.0*np.pi))
                total_like1 *= 1.0/np.sqrt(parameters[1]['vars'][a])
                total_like1 *= np.exp((-1.0/(2.0*parameters[1]['vars'][a]))*(feature - parameters[1]['mean'][a])**2)

            total_like1 *= parameters[1]['prior']

            # Determining Likelihood for being 2
            total_like2 = 1.0
            for a,feature in enumerate(dataItem[1:]):

                total_like2 *= 1.0/(np.sqrt(2.0*np.pi))
                total_like2 *= 1.0/np.sqrt(parameters[2]['vars'][a])
                total_like2 *= np.exp((-1.0/(2.0*parameters[2]['vars'][a]))*(feature - parameters[2]['mean'][a])**2)

            total_like2 *= parameters[2]['prior']


            prob1 = 1.0*total_like1/(float)(total_like1 + total_like2)

            if prob1>0.5:
                predictions.append(1)
            else:
                predictions.append(2)

        misclassification = 100- getAccuracy(testSet, predictions)
        totalMisclassification+=misclassification
        print "Misclassification ( fold =",i,"):", misclassification,'%'

    print "========================================================================="
    print "Average Misclassification:",totalMisclassification/(float)(fold),'%'

main();
