import numpy as np

def interpolation(array):
    shape = array.shape

    for i in range(1,shape[0]-1):
        for j in range (1, shape[1]-1):
            # pixel = array[i][j]
            pixel_left = array[i-1][j]
            pixel_right = array[i+1][j]
            pixel_lower = array[i][j-1]
            pixel_upper = array[i][j+1]

            #all the neighbour pixels are missing
            if pixel_left+pixel_right+pixel_lower+pixel_upper == 888:
                continue
            else
