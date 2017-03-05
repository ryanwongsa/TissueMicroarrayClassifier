import numpy as np
import random
import warnings
warnings.filterwarnings("ignore")

# print float("6.5e+07");


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

dataset = readDataset("redv1_epi_stroma_data.tsv");
print "dataset", len(dataset)
print "----------------------------------------------"
numFeatures = len(dataset[0])-1
print "Number of Features: ", numFeatures

# Calculate maximums
# maxList=[]
# minList=[]
# for i in range(1,numFeatures+1):
#     maxItem = -1000000000
#     minItem = 10000000000
#     for data in dataset:
#         if maxItem <= data[i]:
#             maxItem = data[i];
#         if minItem >= data[i]:
#             minItem = data[i];
#     maxList.append(maxItem);
#     minList.append(minItem);
# # print "List of Maximums:", maxList;
#
# for data in dataset:
#     for i in range(1,numFeatures+1):
#         try:
#             data[i]=(data[i]-minList[i-1])/(float)(maxList[i-1]-minList[i-1]);
#         except Exception:
#             data[i]=data[i]


# print dataset


# SPLIT DATA INTO SUBSETS FOR C-FOLD
random.shuffle(dataset);
print "random dataset", len(dataset)
fold = 10;
foldedDataset = splitFoldDataset(dataset,fold)

totalAccuracy=0
for i in range(fold):
    # combine for training set
    trainingSet = []
    for j in range(fold):
        if i!=j:
            trainingSet += foldedDataset[j]
    # left over for test set
    testSet = foldedDataset[i]

    parameters = {}

    for cl in range(1,3):
        data_pos=[]
        for r in range(len(trainingSet)):
            if int(trainingSet[r][0])==cl:
                data_pos.append(trainingSet[r]);
        # print len(data_pos)

        class_pars = {}
        class_pars['mean'] = np.array(data_pos).mean(axis=0)[1:]
        class_pars['vars'] = np.array(data_pos).var(axis=0)[1:]
        class_pars['prior'] = 1.0*len(data_pos)/len(trainingSet)
        # print class_pars
        parameters[cl] = class_pars


    predictions = []
    for j,dataItem in enumerate(testSet):
        total_like1 = 1.0
        for a,feature in enumerate(dataItem[1:]):
            # print i,feature
            total_like1 *= 1.0/(np.sqrt(2.0*np.pi))
            total_like1 *= 1.0/np.sqrt(parameters[1]['vars'][a])
            total_like1 *= np.exp((-1.0/(2.0*parameters[1]['vars'][a]))*(feature - parameters[1]['mean'][a])**2)

        total_like1 *= parameters[1]['prior']

        total_like2 = 1.0
        for a,feature in enumerate(dataItem[1:]):
            # print i,feature
            total_like2 *= 1.0/(np.sqrt(2.0*np.pi))
            total_like2 *= 1.0/np.sqrt(parameters[2]['vars'][a])
            total_like2 *= np.exp((-1.0/(2.0*parameters[2]['vars'][a]))*(feature - parameters[2]['mean'][a])**2)
            # print total_like2
        total_like2 *= parameters[2]['prior']
        # print total_like1,total_like2
        try:
            prob1 = 1.0*total_like1/(float)(total_like1 + total_like2)
        except Exception:
            prob1=0.5

        if prob1>0.5:
            predictions.append(1)
        else:
            predictions.append(2)

    accuracy = getAccuracy(testSet, predictions)
    totalAccuracy+=accuracy
    print "Accuracy (",i,"):", accuracy
    # break;
print "Average Accuracy:",totalAccuracy/(float)(fold);
