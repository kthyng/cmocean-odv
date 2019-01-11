'''
Make ODV .pal colormap files from cmocean rgb files.
This reads in the colormap rgb from github directly, and it is stored
locally by np.genfromtxt.
'''

import numpy as np
import os
import cmocean


# number of levels for colormap, set by ODV
N = 113

# location of local rgb files
loc = 'https://raw.githubusercontent.com/matplotlib/cmocean/master/cmocean/rgb/'

# file list
Files = [loc + name + '-rgb.txt' for name in cmocean.cm.cmapnames]

if not os.path.exists('pal'):
    os.makedirs('pal')

# Loop through rgb files and make pal file
for File in Files:

    # read in rgb values
    rgb = np.genfromtxt(File)

    # convert to colormap
    cmap = cmocean.tools.cmap(rgb, N=N)

    # back to rgb, now correct number of levels
    rgb = cmocean.tools.print_colormaps([cmap], N=N)[0]

    # file name
    fname = File.split('/')[-1].split('-')[0]
    f = open('pal/' + fname + '.pal', 'w')

    # fill in lines 0-31 from ODV default palette
    odv = np.loadtxt('pal/Odv-save.pal')
    for j in range(32):
        f.write('%3i  %.3f  %.3f  %.3f\n' % (odv[j, 0], odv[j, 1], odv[j, 2], odv[j, 3]))

    # loop through rgb to write to file
    for j in range(rgb.shape[0]):
        f.write('%3i  %.3f  %.3f  %.3f\n' % (j+32, rgb[j, 0], rgb[j, 1], rgb[j, 2]))

    # fill in lines 145-176
    for j in range(145, 177):
        f.write('%3i  %.3f  %.3f  %.3f\n' % (odv[j, 0], odv[j, 1], odv[j, 2], odv[j, 3]))

    f.close()
