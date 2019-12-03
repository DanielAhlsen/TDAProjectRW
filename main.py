from randomwalks import UniformRandomWalk as URW
from randomwalks import GreedyRandomWalk as GRW
from randomwalks import GraphDistanceMatrix as GraphDist
from randomwalks import GenerateSample as Sample
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

URW = URW()
#GRW = GRW()
number_of_samples = 1
sample_length = 1000

list_URW = Sample(URW,sample_length,number_of_samples)
#list_GRW = Sample(GRW,sample_length,number_of_samples)

distances_URW = [ np.array(GraphDist(RW)) for RW in list_URW ]
#distances_GRW = [ np.array(GraphDist(RW)) for RW in list_GRW ]
