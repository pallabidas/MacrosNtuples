#! /usr/bin/env python
#Based off of https://github.com/aloeliger/L1MenuTools/blob/8b4eStudies/L1NtuplesAnalyser/bunchPositionAnalysis.py

import json
  
f = open('data.json')
  
data = json.load(f)

timingInformation = data['IP1_5']['collisionTimePhase']['phaseshift'] 

for i in range(0, len(timingInformation)):
    #if (timingInformation[i] - timingInformation[i-1] > 0. and timingInformation[i-2] - timingInformation[i-1] > 0.):  #gives last filled bunch in a train
    if ((timingInformation[i-1] - timingInformation[i] > 0.) and (timingInformation[i-1] - timingInformation[i-2] > 0.)): #gives last empty bunch
        print(i+1)
