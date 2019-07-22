#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
from astropy.coordinates import SkyCoord

star = np.loadtxt("list_of_stars_LP.txt", skiprows=0, unpack=True, dtype='str')
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
data = data.T
np.savetxt('star_coordinates.txt', data, 
           delimiter=',', comments='')
