#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
June 2018

@author: Sylvia, Xiaohan

"""

import csv
import math
import os
import numpy as np
import matplotlib.pyplot as pyplot
import scipy.misc
import scipy.ndimage
from scipy import interpolate

def loadData(input_file):
    points = open(input_file).readlines()

    point_list = []
    for point in points:
        p_tmp = point.strip().split(" ")
        p_tmp_tofloat = list(map(float, p_tmp))
        point_list.append(p_tmp_tofloat)

    return point_list   

def retriveSatellite():
    organized = np.array(point_list).T
    x = organized[0]
    y = organized[1]

    #print x

    minX = min(x)
    minY = min(y)
    maxX = max(x)
    maxY = max(y)

def pixelGPSet():
    ver_pix_num = 70 # change
    delta_coor = (maxX-minX) / ver_pix_num
    hor_pix_num = int((maxY-minY) / delta_coor)
    # print hor_pix_num

    GPset = []

    for i in range(0, ver_pix_num):
        tmp = []
        for j in range(0, hor_pix_num):
            tmp.append([])

        GPset.append(tmp)


    for point in point_list:
        x = point[0]
        y = point[1]
        alt = point[2]
        i = point[3]

        #print x,y

        pix_x = int((x-minX) / delta_coor) - 1
        pix_y = int((y-minY) / delta_coor) - 1

        #print pix_x, pix_y

        GPset[pix_x][pix_y].append((x,y,alt,i))

        GPset = eliminateNul
        return GPset

if __name__ == "__main__":
    #loading the cloud data points into point_list
    input_file = 'final_project_point_cloud.fuse'
    point_list = loadData(input_file)
    GPset = pixelGPSet()

#S(x,y) = STD(GP(x,y))
DTM_std = []
DTM_med = []
DTM_min = []
DTM_exist = []
for i in range(0, ver_pix_num):
    std_row = []
    med_row = []
    min_row = []
    exist_row = []
    for j in range(0, hor_pix_num):
        if GPset[i][j]:
            std_val = np.std([GPset[i][j][k][2] for k in range(0, len(GPset[i][j]))])
            md_val = np.median([GPset[i][j][k][2] for k in range(0, len(GPset[i][j]))])
            min_val = np.min([GPset[i][j][k][2] for k in range(0, len(GPset[i][j]))])
            exist_val = 100
            #print md_val
        else:
            std_val = 0
            md_val = 222
            min_val = 222
            exist_val = 0

        std_row.append(std_val)
        med_row.append(md_val*1000)
        min_row.append(min_val)
        exist_row.append(exist_val)

    DTM_std.append(std_row)
    DTM_med.append(med_row)
    DTM_min.append(min_row)
    DTM_exist.append(exist_row)

# STD = np.array(DTM_std)
STD = np.fliplr(np.array(DTM_std).T).T
# MED = np.array(DTM_med)
MED = np.fliplr(np.array(DTM_med).T).T
# MIN = np.array(DTM_min)
MIN = np.fliplr(np.array(DTM_min).T).T
# EXIST = np.array(DTM_exist)
EXIST = np.fliplr(np.array(DTM_exist).T).T

# standard deviation
index = np.argmax(STD)
row = int(index) / hor_pix_num
col = int(index) % hor_pix_num
#max_pix = STD[row][col]

# hist_can = []
# for p in GPset[row][col]:
#     hist_can.append(p[2])

# the histogram of max std
# num_bins = 20
# n, bins, patches = pyplot.hist(hist_can, num_bins)
# pyplot.show()


'''
csvfile = "pixelmodel_output.csv"
with open(csvfile, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    writer.writerows(whole_col)
'''
# resized_MIN = scipy.misc.imresize(STD,200,interp='bilinear')
# resized_MIN = scipy.ndimage.interpolation.zoom(input=MIN, zoom=(5./3), order = 2)
x,y = np.mgrid[45.90487933:45.90329572:70j, 11.02701384:11.02965733:116j]
xnew,ynew = np.mgrid[45.90487933:45.90329572:210j, 11.02701384:11.02965733:348j]
tck = interpolate.bisplrep(x, y, MIN, s=0)
resized_MIN = interpolate.bisplev(xnew[:,0], ynew[0,:], tck)

# pyplot.imshow(STD)
# pyplot.colorbar()
# pyplot.show()
#
# pyplot.imshow(MED)
# pyplot.colorbar()
# pyplot.show()

pyplot.imshow(MIN)
pyplot.colorbar()
pyplot.title("DTM - minimum")
pyplot.show()

pyplot.imshow(resized_MIN)
pyplot.colorbar()
pyplot.title("DTM - interpolation")
pyplot.show()
#
# pyplot.imshow(EXIST)
# pyplot.colorbar()
# pyplot.show()
