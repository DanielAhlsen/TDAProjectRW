from randomwalks import UniformRandomWalk as URW
from randomwalks import GreedyRandomWalk as GRW
from randomwalks import DistanceMatrix as Dist
from randomwalks import GenerateSample as Sample
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

RW = GRW()
num = 3
length = 5000
list = Sample(RW,length,num)

dist = np.zeros((num,num))
for i in range(num):
    for j in range(num):
        dist[i,j] = np.sum(abs(list[i,:,:] - list[j,:,:]))/length

plt.plot(list[0,:,0], list[0,:,1])
plt.plot(list[1,:,0], list[1,:,1])
plt.plot(list[2,:,0], list[2,:,1])
plt.show()