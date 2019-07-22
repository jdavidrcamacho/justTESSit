#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
from tess_stars2px import tess_stars2px_function_entry
from astropy.coordinates import SkyCoord


def checkCoordinates(star_file, header=0):
    """
        Returns the RA and DEC for a given list of stars
        Parameters:
            star_file = file with the list of stars
            header = number of lines used as header
    """
    star = np.loadtxt(star_file, skiprows=header, unpack=True, dtype='str')
    #astropy RA and DEC for our stars
    star.reshape(star.size)
    ra, dec = [], []
    for i,j in enumerate(star):
        ra.append(np.array(SkyCoord.from_name(j).ra))
        dec.append(np.array(SkyCoord.from_name(j).dec))
    ra = np.array(ra)
    ra.reshape(ra.size)
    dec = np.array(dec)
    dec.reshape(dec.size)
    data = np.stack((ra, dec))
    return data


def checkTESS(coord_file, header=0):
    """
        Returns the TESS website file with sector observations for a given set 
    of star coordinates
        Parameters:
            coord_file = file with the stars coordinates
    """
    #our coordinates
    ra, dec = np.loadtxt(coord_file, skiprows=0, unpack=True, 
                         usecols=(0,1), delimiter=',')
    star_id = np.linspace(1, len(ra), len(ra))
    
    #Lets see if TESS will look at it
    outID, outEclipLong, outEclipLat, outSec, outCam, outCcd, \
            outColPix, outRowPix, scinfo = tess_stars2px_function_entry(star_id, ra, dec)
    
    print(outID)
    print(outSec)
    
#    sectors = []
#    for i, j in enumerate(star_id):
#        stars = [int(i+1)]
#        sectors.append(outSec[i])
#        observations = np.array([stars, sectors])
#        print(observations)
#        if i == 0:
#            final_list = observations
#        else:
#            final_list = np.vstack((final_list, observations))
    return 0


##our initial list of start
#star = np.loadtxt("utils/list_of_stars_LP.txt", skiprows=0, unpack=True, dtype='str')
#
##astropy RA and DEC for our stars
#star.reshape(star.size)
#ra, dec = [], []
#for i,j in enumerate(star):
#    ra.append(np.array(SkyCoord.from_name(j).ra))
#    dec.append(np.array(SkyCoord.from_name(j).dec))
#ra = np.array(ra)
#ra.reshape(ra.size)
#dec = np.array(dec)
#dec.reshape(dec.size)
#data = np.stack((ra, dec))
#data = data.T
#
#
##observations taken from TESS website
#observations = np.loadtxt("utils/wtv-star_coordinates.txt", skiprows=31, 
#                          delimiter=',', unpack=True, dtype='float')
#observations = observations.T
#
##date of observation for each sector
#sectors = np.loadtxt("utils/sectors.txt", skiprows=0, unpack=True, dtype='str')
#sectors = sectors.T
#
##because I prefer the name of the start instead of RA and DEC
#data = star
#for i in range(sectors[:,0].size):
#    data = np.vstack((data, observations[:,i+2]))
#data = data.T
#
##all stars and the times they we observed if that was the case
#allStarList = [[i] for i in star]
#for i in range(data[:,0].size):
#    for j in range(1, data[0].size):
#            print(data[i,0], np.float(data[i,j]))
#            if int(np.float(data[i,j])) != 0:
#                result = ["from ", sectors[j-1,1], " to ", sectors[j-1,2] ]
#                result = "".join(result)
#                allStarList[i].append(result)
#
###only stars that were observed
##observedStarList = []
##for i,j in enumerate(allStarList):
##    if len(j) > 1:
##        observedStarList.append(j)
#
##now a final list with start and end observations
#final_list = []
#for i,j in enumerate(allStarList):
#    final_list.append([j[0]])
#    if len(j) == 1:
#        final_list[i].append('Not observed')
#    else:
#        observationSpan = [allStarList[i][-1][0:16], ' ', allStarList[i][-1][-14:]]
#        observationSpan = "".join(observationSpan)
#        final_list[i].append(observationSpan)
#
#data = np.array(final_list)
#np.savetxt('star_observations.txt', data, 
#           delimiter='\t', comments='', fmt='%s')
