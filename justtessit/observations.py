#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
from tess_stars2px import tess_stars2px_function_entry
from astropy.coordinates import SkyCoord


def checkList(star_file, header = 0, savefile = True):
    """
        Returns the TESS observations for a given list of stars
        Parameters:
            star_file = file with the list of stars
            header = number of lines used as header
            savefile = True if we want a txt file with the schedule
    """
    #our stars
    stars = np.loadtxt(star_file, skiprows=0, unpack=True, dtype='str')
    #our coordinates
    ra, dec = _checkListCoordinates(star_file, header=header)
    #giving ids to the stars
    star_id = np.linspace(1, len(stars), len(stars))
    
    #Lets see if TESS will look at it
    outID, outEclipLong, outEclipLat, \
    outSec, outCam, outCcd, \
    outColPix, outRowPix, scinfo = tess_stars2px_function_entry(star_id,ra,dec)
    
    observed_sectors = []
    for i, j in enumerate(star_id):
        sector = []
        for ii, jj in enumerate(outID):
            if j==jj:
                sector.append(outSec[ii])
        observed_sectors.append(sector)
    
    #date of observation for each sector
    sectors = np.loadtxt("utils/sectors.txt", skiprows=0, unpack=True, dtype='str')
    sectors = sectors.T
    
    #because I prefer the name of the start instead of RA and DEC
    allStarList = [[i] for i in stars]
    for i, j in enumerate(stars):
        if len(observed_sectors[i]) == 0:
            allStarList[i].append("Star not observed")
        else:
            result = ["Observed from ", sectors[int(observed_sectors[i][0])-1,1], 
                      " to ", sectors[int(observed_sectors[i][-1])-1, 2]]
            result = "".join(result)
            allStarList[i].append(result)
    
    #now a final list with start and end observations
    data = np.array(allStarList)
    if savefile:
        np.savetxt('star_observations.txt', data, 
                   delimiter='\t', comments='', fmt='%s')
    return data

def checkStar(star, savefile = True):
    """
        Returns the a file with TESS observations for a given star
        Parameters:
            star = name of the star
            savefile = True if we want a txt file with the schedule
    """
    #our coordinates
    ra, dec = _checkStarCoordinates(star)
    #giving ids to the stars
    star_id = [1]
    
    #Lets see if TESS will look at it
    outID, outEclipLong, outEclipLat, \
    outSec, outCam, outCcd, \
    outColPix, outRowPix, scinfo = tess_stars2px_function_entry(star_id,ra,dec)
    
    observed_sectors = []
    for i, j in enumerate(star_id):
        sector = []
        for ii, jj in enumerate(outID):
            if j==jj:
                sector.append(outSec[ii])
        observed_sectors.append(sector)
    
    #date of observation for each sector
    sectors = np.loadtxt("utils/sectors.txt", skiprows=0, unpack=True, dtype='str')
    sectors = sectors.T
    
    #because I prefer the name of the start instead of RA and DEC
    allStarList = [[i] for i in [star]]
    for i, j in enumerate([star]):
        if len(observed_sectors[i]) == 0:
            allStarList[i].append("Star not observed")
        else:
            result = ["Observed from ", sectors[int(observed_sectors[i][0])-1,1], 
                      " to ", sectors[int(observed_sectors[i][-1])-1, 2]]
            result = "".join(result)
            allStarList[i].append(result)
            
    #now a final list with start and end observations
    data = np.array(allStarList)
    np.savetxt('star_observations.txt', data, 
               delimiter='\t', comments='', fmt='%s')
    return data


def _checkListCoordinates(star_file, header = 0):
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
    return ra, dec

def _checkStarCoordinates(star):
    """
        Returns the RA and DEC for a given list of stars
        Parameters:
            star = name of the star
    """
    #astropy RA and DEC for our stars
    ra, dec = [], []
    for i,j in enumerate([star]):
        ra.append(np.array(SkyCoord.from_name(j).ra))
        dec.append(np.array(SkyCoord.from_name(j).dec))
    ra = np.array(ra)
    ra.reshape(ra.size)
    dec = np.array(dec)
    dec.reshape(dec.size)
    return ra, dec

