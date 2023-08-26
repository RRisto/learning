# SISO program convertPartitionToPacking.py

# Convert an instance of Partition into an equivalent instance of
# Packing.

# inString: an instance of Partition, represented as integer weights
# separated by whitespace.

# returns: an instance of Packing, represented as integer weights
# separated by whitespace followed by the low and high thresholds,
# separated by semicolons.

# Example:
# >>> convertPartitionToPacking('6 6 7 7')
# '6 6 7 7;13;13'
import utils; from utils import rf
def convertPartitionToPacking(inString):  
    weights = [int(x) for x in inString.split()]
    totalWeight = sum(weights)
    if totalWeight % 2 == 1:
        # if the total weight is odd, no partition is possible,
        # so return any negative instance of Packing
        return '0;1;1' 
    else:
        # use thresholds that are half the total weight
        targetWeight = str(int(totalWeight / 2))
        return inString+';'+targetWeight+';'+targetWeight  

def testConvertPartitionToPacking():
    from packing import packing
    from partition import partition
    instances = ['5', '5 6', '5 6 7', '5 6 7 8',
                 '',
                 '5 7',
                 '6 6',
                 '6 6 7 7',
                 '10 20 30 40 11 21 31 41',]
    for instance in instances:
        convertedInstance = convertPartitionToPacking(instance)
        instanceSolution = partition(instance)
        convertedInstanceSolution = packing(convertedInstance)
        revertedSolution = convertedInstanceSolution
        utils.tprint(instance, 'maps to', convertedInstance,\
              ' solutions were: ', instanceSolution, ';', convertedInstanceSolution)

        if revertedSolution=='no':
            assert instanceSolution=='no'
        else:
            total = sum([int(x) for x in instance.split()])
            solutionTotal = sum([int(x) for x in revertedSolution.split()])
            assert solutionTotal * 2 == total


