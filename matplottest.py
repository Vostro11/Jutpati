import numpy
import sys

inputF = input("Enter address:")
outputF = print()


def activationFunction(output):
    if output > 0:
        return 1
    else:
        return -1


data = numpy.genfromtxt(inputF, delimiter=',')
label = data[:, 2]
features = data[:, 0:2]
bias = numpy.ones((data.shape[0], 1))
features = numpy.hstack((bias, features))
weights = numpy.array([0, 0, 0])
outputFile = numpy.zeros((1, 3))
while True:

    prevWeights = weights
    for i in range(0, data.shape[0]):
        output = numpy.matmul(features[i], weights.T)
        output = activationFunction(output)
        if label[i] * output <= 0:
            update = label[i] * features[i]
            prevWeights = weights + update

    if (prevWeights == weights).all():
        break
    else:
        weights = prevWeights
        print(weights[0], weights[1], weights[2])
        outputFile = numpy.vstack((outputFile, [weights[1], weights[2], weights[0]]))

print(outputFile)
numpy.savetxt('hellyeah', outputFile[1:], fmt="%.3f", delimiter=',')