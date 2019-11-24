# GrayMatter
Deriving rules for the quick learning Neural Network self-organization.

## To do

* create sensors (environment)
* create neuron class
* create gray matter box
* connect actions
* create counters/graphs

## Elasticsearch server
* monitoring training.

## Description
    Main program is universe.py. 
    It determines play size, population size, 
    It has population, keeps amount of food at each point.
    It makes time tick. It creates individuals (brains).
    On each tick it check individuals and updates positions and states. 

    brain.py
    has neurons. creates/removes them. it has synapses. 
    has quality that it exposes to other individuals.  
    parameter: interconnectedness. 
    ticks neurons.
    
    neuron.py
    has synapses. can remove synapses.
    parameters: treshold, leakage, random signal prob. 

    synapse
    parameters: destination neuron, distance, weight, sensitivity, sensitivity decay

## technical org.
    one node runs one population
    populations coordinated externaly - from time to time a couple of individuals exchanged between randomly selected populations
    each individual is a thread
    each brain loops through neurons once per tick and puts them into new state. Each synapse has a fixed list of events comming its way. it is as long as the distance between the neurons (in ticks).
    
