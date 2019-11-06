from randomwalks import UniformRandomWalk as URW
from randomwalks import GreedyRandomWalk as GRW
from randomwalks import DistanceMatrix as Dist
from randomwalks import GenerateSample as Sample
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

URW = URW()
GRW = GRW()
num = 1
length = 100
#list_URW = Sample(URW,length,num)
list_GRW = Sample(GRW,length,num)

#plt.plot(list_URW[0,:,0], list_URW[0,:,1])
plt.plot(list_GRW[0,:,0], list_GRW[0,:,1], color='red')
plt.show()
"""
dist = np.zeros((num,num))
for i in range(num):
    for j in range(num):
        dist[i,j] = np.sum(abs(list_URW[i,:,:] - list_URW[j,:,:]))/length

dist = np.zeros((num,num))
for i in range(num):
    for j in range(num):
        dist[i,j] = np.sum(abs(list_GRW[i,:,:] - list_GRW[j,:,:]))/length

"""