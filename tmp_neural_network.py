#!/usr/bin/env python3

import numpy as np
import pandas as pd

# X = (hours sleeping, hours studying), y = score on test
# X = np.array(([2, 9], [1, 5], [3, 6]), dtype=float)
# y = np.array(([92], [86], [89]), dtype=float)
data = pd.read_csv("random_v_zeros.txt", sep = "\t", names = ["Jump score", \
                   "Death score", "Avoid Death score", "Provide Defense score",\
                   "Distance to King score", "Distance to King factor", "aggression_threshhold",\
                   "Aggression factor", "Coward factor", "Result", "Turn score", "Size of result"])

X = np.array(([5,  5,  -8, -10,  -10,  -2, -10, -7, 1], [-1, 6,  -10,  -8, -9, -2, 0.7,  1,  4], [-5, -9, -2, -3, 3,  9,  -6, 5,  0]), dtype = float)
y = np.array(([1], [-1], [0]), dtype = float)
xPredicted = np.array(([4,8]), dtype=float)

scores = data.iloc[0:100:,0:9]
# scores.iloc[:,0:5] /= 10
scores = np.array(scores, dtype = float)
results = data.iloc[0:100:,9:12]
results[results == "R"] = 1
results[results == 0] = 0.5
results[results == -1] = 0
results = np.array(results, dtype = float)
to_predict = data.iloc[101:102:,0:9]
should_predict = data.iloc[101:102:,9:12]
# results = results[np.newaxis]
# results = results.T


X = scores
y = results
# scale units
# X = np.divide(X, 10)
# print(X)
# y = y/100 # max test score is 100
xPredicted = xPredicted/np.amax(xPredicted, axis=0)

class NeuralNetwork(object):

    def __init__(self):
        #parameters
        self.inputSize = 9
        self.outputSize = 3
        self.hiddenSize = 8

        #weights
        self.W1 = np.random.randn(self.inputSize, self.hiddenSize) # (3x2) weight matrix from input to hidden layer
        self.W2 = np.random.randn(self.hiddenSize, self.outputSize) # (3x1) weight matrix from hidden to output layer

    def forward(self, X):
    #forward propagation through our network
        self.z = np.dot(X, self.W1) # dot product of X (input) and first set of 3x2 weights
        self.z2 = self.sigmoid(self.z) # activation function
        # self.z2 = self.tanh(self.z) # activation function
        self.z3 = np.dot(self.z2, self.W2) # dot product of hidden layer (z2) and second set of 3x1 weights
        o = self.sigmoid(self.z3) # final activation function
        # o = self.tanh(self.z3) # final activation function
        return o

    def sigmoid(self, s):
        # activation function
        return 1/(1+np.exp(-s))

    def sigmoidPrime(self, s):
        #derivative of sigmoid
        return s * (1 - s)

    def tanh(self, s):
        # activation function
        return (2 / (1 + np.exp(-2 * s))) - 1

    def tanh_prime(self, s):
        # derivative of tanh
        return 1 - (s ** 2)
    def backward(self, X, y, o):
        # backward propagate through the network
        self.o_error = y - o # error in output
        self.o_delta = self.o_error*self.sigmoidPrime(o) # applying derivative of sigmoid to error
        # self.o_delta = self.o_error*self.tanh_prime(o) * 0.1# applying derivative of sigmoid to error

        self.z2_error = self.o_delta.dot(self.W2.T) # z2 error: how much our hidden layer weights contributed to output error
        self.z2_delta = self.z2_error*self.sigmoidPrime(self.z2) # applying derivative of sigmoid to z2 error
        # self.z2_delta = self.z2_error*self.tanh_prime(self.z2) * 0.1 # applying derivative of sigmoid to z2 error

        self.W1 += X.T.dot(self.z2_delta) # adjusting first set (input --> hidden) weights
        self.W2 += self.z2.T.dot(self.o_delta) # adjusting second set (hidden --> output) weights

    def train (self, X, y):
        o = self.forward(X)
        self.backward(X, y, o)

    def predict(self):
        print ("Predicted data based on trained weights: ")
        print ("Input (scaled): \n" + str(to_predict))
        print ("Output: \n" + str(self.forward(to_predict)))

NN = NeuralNetwork()
for i in range(10000): # trains the NN 1,000 times
    print ("Input: \n" + str(X))
    print ("Actual Output: \n" + str(y))
    print ("Predicted Output: \n" + str(NN.forward(X)))
    print ("Loss: \n" + str(np.mean(np.square(y - NN.forward(X))))) # mean sum squared loss
    print ("\n")
    NN.train(X, y)

# defining our output
# o = NN.forward(to_predict)
NN.predict()
# print("Predicted Output: {}".format(o))
print("Actual Output: {}".format(should_predict))
