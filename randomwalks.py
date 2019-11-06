import numpy as np
from numpy.random import randint
import networkx as nx

class RandomWalk:
    """
    RandomWalk
    
    A RandomWalk in 2D.
    """
    def __init__(self, init = (0,0)):
        self.current = init
        self.graph = nx.Graph()
        self.graph.add_node(self.current)
        self.trajectory = np.array([self.current], dtype='int16')
        
    def takeStep(self,next_step):
        self.graph.add_edge(self.current, next_step)
        self.current = next_step
        self.trajectory = np.append(self.trajectory, [self.current],axis=0)

    def clear(self, init=(0,0)):
        self.__init__(init)
        
    def getStep(self,x=(0,0)):
        i, j = randint(2, size=2)
        return (x[0] + (-1)**j * ((i+1) % 2) , x[1] + (-1)**j * (i % 2))
        
class UniformRandomWalk(RandomWalk):
    """
    UniformRandomWalk
    
    A Random Walk in 2D, 
    """  
    def takeStep(self):
        next_step = self.getStep(self.current)
        super().takeStep(next_step)

class GreedyRandomWalk(RandomWalk):
    """
    GreedyRandomWalk
    
    A Greedy Random Walk in 2D.
    """  
    def takeStep(self):
        graph_edges = self.graph.edges()
        while True:
            next_step = self.getStep(self.current)
            edge = (self.current, next_step)
            edge_rev = (next_step, self.current)
            if not (edge in graph_edges or edge_rev in graph_edges):
                super().takeStep(next_step)
                break

def DistanceMatrix(RandomWalk):     
    G = RandomWalk.graph
    nodes = list(G.nodes())
    distances = dict(nx.all_pairs_shortest_path_length(G))
    matrix = np.zeros((len(G),len(G))) 

    for i in range(len(G)):
        for j in range(len(G)):
            matrix[i][j] = distances[nodes[i]][nodes[j]]

    return matrix
    
def GenerateSample(RandomWalk, length, num):
    list = np.zeros((num,length+1,2))

    for i in range(num):
        for n in range(length):
            RandomWalk.takeStep()
        list[i,:,:] = RandomWalk.trajectory
        RandomWalk.clear()

    return list