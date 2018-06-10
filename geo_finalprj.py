#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
June 2018

@author: Sylvia, Xiaohan

"""

import numpy as np
import matplotlib.pyplot as pyplot
from scipy import interpolate

input_file = 'final_project_point_cloud.fuse'
points = open(input_file).readlines()

point_list = []
for point in points:
    p_tmp = point.strip().split(" ")
    p_tmp_tofloat = list(map(float, p_tmp))
    point_list.append(p_tmp_tofloat)


organized = np.array(point_list).T
x = organized[0]
y = organized[1]


minX = min(x)
minY = min(y)
maxX = max(x)
maxY = max(y)

ver_pix_num = 80 #Zoom in -> one pixel => more coord
delta_coor = (maxX-minX) / ver_pix_num
hor_pix_num = int((maxY-minY) / delta_coor)

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

    pix_x = int((x-minX) / delta_coor) - 1
    pix_y = int((y-minY) / delta_coor) - 1

    GPset[pix_x][pix_y].append((x,y,alt,i))

#delete boundary rows with less than 8% non-empty pixels
while True:
    if len(filter(None, GPset[0])) < 0.08*len(GPset[0]):
         GPset = GPset[1:]
    else:
        break
while True:
    if len(filter(None, GPset[-1])) < 0.08*len(GPset[0]):
         GPset = GPset[:-1]
    else:
        break

#delete boundary columns with less than 8% non-empty pixels
GPset = np.asarray(GPset).T
while True:
    if len(filter(None, GPset[0])) < 0.08*len(GPset[0]):
         GPset = GPset[1:]
    else:
        break
while True:
    if len(filter(None, GPset[-1])) < 0.08*len(GPset[0]):
         GPset = GPset[:-1]
    else:
        break
GPset = GPset.T

ver_pix_num = GPset.shape[0]
hor_pix_num = GPset.shape[1]
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
        else:
            std_val = 0
            md_val = 220 # assume
            min_val = 220 # assume
            exist_val = 0
        std_row.append(std_val)
        med_row.append(md_val)
        min_row.append(min_val)
        exist_row.append(exist_val)

    DTM_std.append(std_row)
    DTM_med.append(med_row)
    DTM_min.append(min_row)
    DTM_exist.append(exist_row)

inter2 = DTM_min

for k in range(0, 2):
    inter = inter2
    inter2 = []
    for i in range(0, ver_pix_num):
        inter_row = []
        for j in range(0, hor_pix_num):
            if inter[i][j] == 220:
                count = 0
                if i>0 and j>0 and i<ver_pix_num-2 and j<hor_pix_num-2:
                    if inter[i][j+1] == 220:
                        r = 0
                        count+=1
                    else:
                        r = inter[i][j+1]
                    if inter[i][j-1] == 220:
                        l = 0
                        count+=1
                    else:
                        l = inter[i][j-1]
                    if inter[i-1][j] == 220:
                        u = 0
                        count+=1
                    else:
                        u = inter[i-1][j]
                    if inter[i+1][j] == 220:
                        d = 0
                        count+=1
                    else:
                        d = inter[i+1][j]

                    if count == 4 or count == 3:
                        new_val = 220
                    else:
                        new_val = (r+l+u+d) / (4-count)

                else:
                    if j+1 >= hor_pix_num:
                        r = 0.0
                        count+=1
                    else:
                        if inter[i][j+1] == 220:
                            r = 0.0
                            count+=1
                        else:
                            r = inter[i][j+1]
                    if j-1 <= 0:
                        l = 0.0
                        count+=1
                    else:
                        if inter[i][j-1] == 220:
                            l = 0.0
                            count+=1
                        else:
                            l = inter[i][j-1]
                    if i-1 <=0:
                        u = 0.0
                        count+=1
                    else:
                        if inter[i-1][j] == 220:
                            u = 0.0
                            count+=1
                        else:
                            u = inter[i-1][j]
                    if i+1 >= ver_pix_num:
                        d = 0.0
                        count+=1
                    else:
                        if inter[i+1][j] == 220:
                            d = 0.0
                            count+=1
                        else:
                            d = inter[i+1][j]
                    #print r,l,u,d,count

                    if count == 4 or count == 3:
                        new_val = 220
                    else:
                        new_val = (r+l+u+d) / (4-count)

            else:
                new_val = inter[i][j]

            inter_row.append(new_val)

        inter2.append(inter_row)

# STD = np.array(DTM_std)
STD = np.fliplr(np.array(DTM_std).T).T
# MED = np.array(DTM_med)
MED = np.fliplr(np.array(DTM_med).T).T
# MIN = np.array(DTM_min)
MIN = np.fliplr(np.array(DTM_min).T).T
# EXIST = np.array(DTM_exist)
EXIST = np.fliplr(np.array(DTM_exist).T).T
#INT = np.array(inter2)
INT2 = np.fliplr(np.array(inter2).T).T




'''
# standard deviation
index = np.argmax(STD)
row = int(index) / hor_pix_num
col = int(index) % hor_pix_num
#max_pix = STD[row][col]

hist_can = []
for p in GPset[row][col]:
    hist_can.append(p[2])

# the histogram of max std
num_bins = 20
n, bins, patches = pyplot.hist(hist_can, num_bins)
pyplot.show()
'''

'''
csvfile = "pixelmodel_output.csv"
with open(csvfile, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    writer.writerows(whole_col)
'''

pyplot.figure(1)
pyplot.imshow(STD)
pyplot.title('Standard Deviation')
pyplot.colorbar()
#pyplot.show()

pyplot.figure(2)
pyplot.imshow(MED)
pyplot.title('Median')
pyplot.colorbar()
#pyplot.show()

pyplot.figure(3)
pyplot.imshow(MIN)
pyplot.title('Maximum')
pyplot.colorbar()
#pyplot.show()

pyplot.figure(4)
pyplot.imshow(EXIST)
pyplot.title('pixel with value')
#pyplot.colorbar()
#pyplot.show()

pyplot.figure(5)
pyplot.imshow(INT2)
pyplot.title('interpolation')
pyplot.colorbar()
#pyplot.show()

vals = np.reshape(INT2, (ver_pix_num * hor_pix_num))
pts = np.array([[i,j] for i in np.linspace(0,1,ver_pix_num) for j in np.linspace(0,1,hor_pix_num)] )

grid_x, grid_y = np.mgrid[0:1:ver_pix_num*2j, 0:1:hor_pix_num*2j]
grid_z = interpolate.griddata(pts, vals, (grid_x, grid_y), method='linear')

pyplot.matshow(INT2)
pyplot.colorbar()
pyplot.title('Adding prediction of missing values')
pyplot.matshow(grid_z)
pyplot.colorbar()
pyplot.title('Interpolation')
pyplot.show()
