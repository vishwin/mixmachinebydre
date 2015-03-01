import json
import os.path

from pybrain.tools.shortcuts import buildNetwork
from pybrain.tools.xml.networkwriter import NetworkWriter
from pybrain.tools.xml.networkreader import NetworkReader
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
from random import random

labels = ["ginger ale", "cranberry juice", "coke", "mello yello"]

# Load existing data
ds = SupervisedDataSet(4, 1)
training_set = []
if os.path.isfile('neural_net_data.json'):
    with open('neural_net_data.json', 'r') as infile:
        existing_data = json.load(infile)
        training_set = [ (x[0], x[1]) for x in existing_data ]
    for x in training_set:
        ds.addSample(tuple(x[0]), (x[1], ))
else:
    training_set = []

# Load existing NN weights
if os.path.isfile('neural_net_weights.xml'):
    net = NetworkReader.readFrom('neural_net_weights.xml')
else:
    net = buildNetwork(4, 8, 8, 1)

trainer = BackpropTrainer(net, ds)

def train(rounds=300):
    print(('Training on dataset with {0} rounds...'.format(rounds)))
    for _ in range(rounds):
        print((trainer.train()))
    print('Done training with 300 rounds and (8,8) hidden layers.')
    # Save the learned weights
    NetworkWriter.writeToFile(net, 'neural_net_weights.xml')

def generate_suggestion(threshold=6):
    while True:
        values = [random(), random(), random(), random()]
        values = [ v / (values[0] + values[1] + values[2] + values[3]) for v in values ]
        # Ignore bad suggestions
        if net.activate(values)[0] < 6:
            continue
        return values

def learn(values, rank, rounds=5):
    ds.addSample(tuple(values), (rank, ))
    training_set.append((values, rank))
    for _ in range(rounds):
        print((trainer.train()))
    NetworkWriter.writeToFile(net, 'neural_net_weights.xml')
    with open('neural_net_data.json', 'w') as outfile:
        json.dump(training_set, outfile)
