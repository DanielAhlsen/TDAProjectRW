import numpy as np
from numpy.random import randint
from numpy.random import choice
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
        
class UniformRandomWalk(RandomWalk):
    """
    UniformRandomWalk
    
    A Random Walk in 2D, 
    """  
    def takeStep(self):
        next_step = self.getStep(self.current)
        super().takeStep(next_step)
        
    def getStep(self,x):
        i, j = randint(2, size=2)
        return (x[0] + (-1)**j * ((i+1) % 2) , x[1] + (-1)**j * (i % 2))

class GreedyRandomWalk(RandomWalk):
    """
    GreedyRandomWalk
    
    A Greedy Random Walk in 2D.
    """  
    def takeStep(self):
        next_step = self.getStep(self.current)
        super().takeStep(next_step)

    def getStep(self,x):
        available = [ (x[0]+1,x[1]),(x[0]-1,x[1]),(x[0],x[1]+1),(x[0],x[1]-1)]
        possible = []
        
        graph_edges = self.graph.edges()
        for move in available:
            if not ((move,x) in graph_edges or (x,move) in graph_edges):
                possible.append(move)
        if len(possible) > 0:
            return possible[choice(len(possible))]
        else:
            return available[choice(4)]

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