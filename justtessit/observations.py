#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np

def checkit(star_file, tess_file):
    """
        Checks if a given list of stars is observed with TESS
        Parameters:
            star_file = file with the list of stars
            tess_file = file given by TESS website
    """

#our initial list of start
star = np.loadtxt("list_of_stars_LP.txt", skiprows=0, unpack=True, dtype='str')
#observations taken from TESS website
observations = np.loadtxt("wtv-star_coordinates.txt", skiprows=31, 
                          delimiter=',', unpack=True, dtype='float')
observations = observations.T
#date of observation for each sector
sectors = np.loadtxt("sectors.txt", skiprows=0, unpack=True, dtype='str')
sectors = sectors.T

#because I prefer the name of the start instead of RA and DEC
data = star
for i in range(sectors[:,0].size):
    data = np.vstack((data, observations[:,i+2]))
data = data.T

#all stars and the times they we observed if that was the case
allStarList = [[i] for i in star]
for i in range(data[:,0].size):
    for j in range(1, data[0].size):
            print(data[i,0], np.float(data[i,j]))
            if int(np.float(data[i,j])) != 0:
                result = ["from ", sectors[j-1,1], " to ", sectors[j-1,2] ]
                result = "".join(result)
                allStarList[i].append(result)

##only stars that were observed
#observedStarList = []
#for i,j in enumerate(allStarList):
#    if len(j) > 1:
#        observedStarList.append(j)

#now a final list with start and end observations
final_list = []
for i,j in enumerate(allStarList):
    final_list.append([j[0]])
    if len(j) == 1:
        final_list[i].append('Not observed')
    else:
        observationSpan = [allStarList[i][-1][0:16], ' ', allStarList[i][-1][-14:]]
        observationSpan = "".join(observationSpan)
        final_list[i].append(observationSpan)

data = np.array(final_list)
np.savetxt('star_observations.txt', data, 
           delimiter='\t', comments='', fmt='%s')
