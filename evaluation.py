# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 16:41:29 2020

@author: Dell
"""

# -*- coding: utf-8 -*-
"""

"""

#!/usr/bin/env python
import math
import numpy
import os
import sys
import glob
import matplotlib.pyplot as plt


numpy.set_printoptions(threshold=numpy.inf)


def readFlo(file):
    with open(file, 'br') as f:
        tag = f.read(4)
        if tag != b'PIEH':
            print("File '{}' has wrong input type.".format(file))
            return None
        width = numpy.fromfile(f, dtype=numpy.int32, count=1)[0]
        height = numpy.fromfile(f, dtype=numpy.int32, count=1)[0]
        data = numpy.fromfile(f, dtype=numpy.float32)
    # data.shape = (height, 2*width)
    data.shape = (-1, 2)  # two columns
    return data


def calculateAngleError(data1, data2):
    m12 = numpy.multiply(data1, data2)
    m11 = numpy.square(data1)
    m22 = numpy.square(data2)
    num = 1 + numpy.sum(m12, axis=1)
    den11 = 1 + numpy.sum(m11, axis=1)
    den22 = 1 + numpy.sum(m22, axis=1)
    denom = numpy.sqrt(den11 * den22)
    q = num / denom
    q[q > 1] = 1.
    return numpy.arccos(q)


# calculateAngleError(flow1,flow2)


def calculateEndpointError(data1, data2):
    return numpy.sqrt(numpy.sum(numpy.square(data1 - data2), axis=1))


# calculateEndpointError(flow1,flow2)
def compareFiles(file1, file2):
    data1 = readFlo(file1)
    if data1 is None:
        return
    data2 = readFlo(file2)
    if data2 is None:
        return

    ae = numpy.average(calculateAngleError(data1, data2))
    ee = numpy.average(calculateEndpointError(data1, data2))

    return ae, ee



    
mag=numpy.empty([0,0],dtype=float)
ee_plot  = numpy.empty([0,0],dtype=float)
avg_ee_array = numpy.empty([0,0],dtype=float)
avg_ae_array = numpy.empty([0,0],dtype=float)
counter=1

for files in range(len(glob.glob("(abs path of folder with estimated .flo files)"))): # ground truth and estimated files have the same quantity
    path1="path of first .flo file" + str(counter+1) + ".flo"
    
    #exit(0)
    ee_plot=numpy.append(ee_plot,files)
    #empty_list.append(path1)
    flow1 = readFlo(os.path.abspath(path1))
    print(path1)
    
    #H:\ground_truths_picking_stuff\ground_truth_picking_stuff\flo
    path2="path of first ground truth.flo file" + str(counter+1) + ".flo"
    counter=counter+1
        
    
    flow2 = readFlo(os.path.abspath(path2))
    
    # to be used for future work when one has to guage the average movement in the scene whithout the 0 values
    
    '''u=flow2[:,0]
    v=flow2[:,1]
    non_zero_u=u[u!=0]
    non_zero_v=v[v!=0]
    
        
    
        
    usquared=numpy.square(non_zero_u)
    vsquared=numpy.square(non_zero_v)
    difference_vu=abs(numpy.count_nonzero(vsquared)-numpy.count_nonzero(usquared))
    difference_uv=abs(numpy.count_nonzero(usquared)-numpy.count_nonzero(vsquared))
    
    if numpy.count_nonzero(usquared)>numpy.count_nonzero(vsquared):
       vsquared=numpy.append(vsquared,numpy.zeros((difference_uv)))
    if numpy.count_nonzero(vsquared)>numpy.count_nonzero(usquared):
       usquared=numpy.append(usquared,numpy.zeros(difference_vu)) 
    
    
    
    magnitude=numpy.sqrt(usquared+vsquared)
    mean_mag=numpy.average(magnitude)
    mag=numpy.append(mag,mean_mag)'''
    
    
    
        
    
    ee=calculateEndpointError(flow1,flow2)
    avg_ee=numpy.average(ee)
    avg_ee_array=numpy.append(avg_ee_array,avg_ee)
    
    
    ae=calculateAngleError(flow1,flow2)
    ae=ae*57.296
    avg_ae=numpy.average(ae)
    avg_ae_array=numpy.append(avg_ae_array,avg_ae)
    
    #flow2_array=numpy.append(flow2_array,flow2,axis=0'''
   
# to be used for future work when one has to guage the average movement in the scene whithout the 0 values
    
'''import array as arr    
u1=numpy.empty([0,0],dtype=float)    
u=flow2[:,0]
v=flow2[:,1]
non_zero_u=u[u!=0]

average=numpy.average(non_zero_u)
u1=numpy.append(u1,average)
    
    
        

usquared=numpy.square(u)
vsquared=numpy.square(v)

magnitude=numpy.sqrt(usquared+vsquared)
mean_mag=numpy.average(magnitude)    
  #mag=numpy.append(mag,magnitude)
    #mag=numpy.square(u)'''
    
new_avg_ee_array=numpy.delete(avg_ee_array,[12])
new_avg_ae_array=numpy.delete(avg_ae_array,[12])
new_ee_plot=numpy.delete(ee_plot,[12])    

    
plt.plot(new_ee_plot,new_avg_ae_array)
plt.title("cartwheel")
plt.xlabel("Frames")
plt.ylabel("Angular Error ")
plt.show()

#print(flow1)

print(numpy.average(avg_ee_array))
print(numpy.average(avg_ae_array))



