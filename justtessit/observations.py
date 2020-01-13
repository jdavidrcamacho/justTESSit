#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
from tess_stars2px import tess_stars2px_function_entry
from astropy.coordinates import SkyCoord

#date of observation for each sector
sectors = [['1', '2018-Jul-25', '2018-Aug-22'], 
            ['2', '2018-Aug-22', '2018-Sep-20'], 
            ['3', '2018-Sep-20', '2018-Oct-18'], 
            ['4', '2018-Oct-18', '2018-Nov-15'], 
            ['5', '2018-Nov-15', '2018-Dec-11'], 
            ['6', '2018-Dec-11', '2019-Jan-07'], 
            ['7', '2019-Jan-07', '2019-Feb-02'], 
            ['8', '2019-Feb-02', '2019-Feb-28'], 
            ['9', '2019-Feb-28', '2019-Mar-26'], 
            ['10', '2019-Mar-26', '2019-Apr-22'], 
            ['11', '2019-Apr-22', '2019-May-21'], 
            ['12', '2019-May-21', '2019-Jun-19'], 
            ['13', '2019-Jun-19', '2019-Jul-18'], 
            ['14', '2019-Jul-18', '2019-Aug-15'], 
            ['15', '2019-Aug-15', '2019-Sep-11'], 
            ['16', '2019-Sep-11', '2019-Oct-07'], 
            ['17', '2019-Oct-07', '2019-Nov-02'], 
            ['18', '2019-Nov-02', '2019-Nov-27'], 
            ['19', '2019-Nov-27', '2019-Dec-24'], 
            ['20', '2019-Dec-24', '2020-Jan-21'], 
            ['21', '2020-Jan-21', '2020-Feb-18'], 
            ['22', '2020-Feb-18', '2020-Mar-18'], 
            ['23', '2020-Mar-18', '2020-Apr-16'], 
            ['24', '2020-Apr-16', '2020-May-13'], 
            ['25', '2020-May-13', '2020-Jun-08'], 
            ['26', '2020-Jun-08', '2020-Jul-04'],
            ['27', '2020-Jul-04', '2020-Jul-30'], 
            ['28', '2020-Jul-30', '2020-Aug-26'], 
            ['29', '2020-Aug-26', '2020-Sep-22'], 
            ['30', '2020-Sep-22', '2020-Oct-21'], 
            ['31', '2020-Oct-21', '2020-Nov-19'], 
            ['32', '2020-Nov-19', '2020-Dec-17'], 
            ['33', '2020-Dec-17', '2021-Jan-13'], 
            ['34', '2021-Jan-13', '2021-Feb-09'], 
            ['35', '2021-Feb-09', '2021-Mar-07'], 
            ['36', '2021-Mar-07', '2021-Apr-02'], 
            ['37', '2021-Apr-02', '2021-Apr-28'], 
            ['38', '2021-Apr-28', '2021-May-26'], 
            ['39', '2021-May-26', '2021-Jun-24']]


def checkStar(star, savefile = True):
    """
    Returns the a file with TESS observations for a given star
    
    Parameters
    ----------
    star: str
        Name of the star
    savefile: bool
        True if we want a txt file with the schedule
        
    Returns
    -------
    data: array
        Observation schedule of the given stars
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
    #because I prefer the name of the start instead of RA and DEC
    allStarList = [[i] for i in [star]]
    for i, j in enumerate([star]):
        if len(observed_sectors[i]) == 0:
            allStarList[i].append(" Star not observed")
        else:
            for ii, jj in enumerate(observed_sectors[0]):
                result = [" Observed in sector {0}: ".format(jj), 
                          sectors[int(observed_sectors[0][ii])-1][1], " to ",
                          sectors[int(observed_sectors[0][ii])-1][2]]
                result = "".join(result)
                allStarList[i].append(result)
    #now a final list with start and end observations
    data = np.squeeze(np.array(allStarList))
    if savefile:
        np.savetxt('star_observations.txt', data, delimiter='\t', newline='\r\n',
                   comments='', fmt='%s')
    return data


def checkList(star_file, header = 0, savefile = True):
    """
    Returns the TESS observations for a given list of stars
    
    Parameters
    ----------
    star_file: str
        File with the list of stars
    header: int
        Number of lines used as header
    savefile: bool
        True if we want a txt file with the schedule
        
    Returns
    -------
    data: array
        Observation schedule of the given stars
    """
    #our stars
    stars = np.loadtxt(star_file, skiprows = header, 
                       unpack = True, dtype='str')
    #lets check them one by one
    results = []
    for i,j in enumerate(stars):
        result = "\n".join(checkStar(j))
        results.append(result)
    data = np.squeeze(np.array(results))
    if savefile:
        np.savetxt('star_observations.txt', data, delimiter='\t', newline='\r\n',
                   comments='', fmt='%s')
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

