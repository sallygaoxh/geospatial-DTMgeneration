import csv
import math
import os
import numpy as np
import matplotlib.pyplot as pyplot
# import cv2

# input_file = 'final_project_point_cloud.csv'
input_file = 'coord_outputs.csv'
points = open(input_file).readlines()

point_list = []
for point in points:
    p_tmp = point.strip().split(",")
    # print repr(p_tmp)
    p_tmp_tofloat = list(map(float, p_tmp))
    point_list.append(p_tmp_tofloat)
    # point_list.append(p_tmp)

#print len(point_list)

organized = np.array(point_list).T
x = organized[0]
y = organized[1]

#print x

minX = min(x)
minY = min(y)
maxX = max(x)
maxY = max(y)
# print minX
# print minY
# print maxX
# print maxY

ver_pix_num = 150 # change
delta_coor = (maxX-minX) / ver_pix_num;
hor_pix_num = int((maxY-minY) / delta_coor);

GPset = []

for i in range(0, ver_pix_num):
    tmp = []
    for j in range(0, hor_pix_num):
        tmp.append([])

    GPset.append(tmp)

#print 'GPset size', np.shape(GPset)

for point in point_list:
#for c in range(0, 100):
#    point = point_list[c]
    x = point[0]
    y = point[1]
    alt = point[2]
    i = point[3]

    #print x,y

    pix_x = int((x-minX) / delta_coor) - 1
    pix_y = int((y-minY) / delta_coor) - 1

    #print pix_x, pix_y

    #if x==4363910.64554 and y==850489.133023:
#        print pix_x, pix_y

    GPset[pix_x][pix_y].append((x,y,alt,i))




#S(x,y) = STD(GP(x,y))
whole_col = []
DTM_col = []
for i in range(0, ver_pix_num):
    each_row = []
    DTM_row = []
    for j in range(0, hor_pix_num):
        if GPset[i][j]:
            std_val = np.std([GPset[i][j][k][2] for k in range(0, len(GPset[i][j]))])
            md_val = np.median([GPset[i][j][k][2] for k in range(0, len(GPset[i][j]))])
            #print md_val
        else:
            std_val = 0
            md_val = 220
        each_row.append(std_val)
        DTM_row.append(md_val*1000)

    whole_col.append(each_row)
    DTM_col.append(DTM_row)


S = np.array(whole_col)
# print S
DTM = np.array(DTM_col)


index = np.argmax(S)
# print index
row = int(index) / hor_pix_num
col = int(index) % hor_pix_num
#print row, col
max_pix = S[row][col]
#print max_pix

hist_can = []
for p in GPset[row][col]:
    hist_can.append(p[2])

# the histogram of the data
num_bins = 100
n, bins, patches = pyplot.hist(hist_can, num_bins)
#pyplot.plot(bins, y, 'r--')
pyplot.show()






#print np.shape(S)
#print S


'''
csvfile = "pixelmodel_output.csv"
with open(csvfile, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    writer.writerows(whole_col)
'''



pyplot.imshow(S)
pyplot.colorbar()
pyplot.show()


pyplot.imshow(DTM)
pyplot.colorbar()
pyplot.show()
