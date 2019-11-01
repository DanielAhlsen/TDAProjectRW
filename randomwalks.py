import numpy as np
from random import randint
import networkx as nx

class UniformRandomWalk:
    
    def __init__(self, init = (0,0)):
        self.current = init
        self.graph = nx.Graph()
        self.graph.add_node(init)
        
        self.trajectory = np.array([init], dtype='int64')
        
    def step(self, n=1):
        for i in range(n):
            sample = randint(0, 3)
            
            if sample == 0:
                self.graph.add_edge(self.current, (self.current[0]+1,self.current[1]))
                self.current = (self.current[0]+1,self.current[1])
                self.trajectory = np.append(self.trajectory, [self.current],axis=0)
            elif sample == 1:
                self.graph.add_edge(self.current, (self.current[0],self.current[1]+1))
                self.current = (self.current[0],self.current[1]+1)
                self.trajectory = np.append(self.trajectory, [self.current],axis=0)
            elif sample == 2:
                self.graph.add_edge(self.current, (self.current[0]-1,self.current[1]))
                self.current = (self.current[0]-1,self.current[1])
                self.trajectory = np.append(self.trajectory, [self.current],axis=0)
            else:
                self.graph.add_edge(self.current, (self.current[0],self.current[1]-1))
                self.current = (self.current[0],self.current[1]-1)
                self.trajectory = np.append(self.trajectory, [self.current],axis=0)

    def clear(self, init=(0,0)):
        self.__init__(init)

class GreedyRandomWalk:
    """
    GreedyRandomWalk
    
    A Greedy Random Walk in 2D, which uses uniform distribution.
    """
    def __init__(self, init = (0,0)):
        self.current = init
        self.graph = nx.Graph()
        self.graph.add_node(init)
        self.trajectory = np.array([init], dtype='int64')
        
    def step(self, n=1):
        for i in range(n):
            t = self.current
            possible_moves = [ ((t[0],t[1]), (t[0]+1,t[1])), ((t[0],t[1]), (t[0]-1,t[1])), 
                                ((t[0],t[1]), (t[0],t[1]+1)), ((t[0],t[1]), (t[0],t[1]-1)) ]
            available_moves = []
            for i in range(4):
                temp = [possible_moves[i], (possible_moves[i][1], possible_moves[i][0])]
                if all( [ tempi not in self.graph.edges() for tempi in temp ]):
                    available_moves = available_moves + [possible_moves[i]]
            
            if len(available_moves) in [1,2,3]:
                i = randint(0, len(available_moves)-1)
                self.graph.add_edge(available_moves[i][0], available_moves[i][1])
                self.current = available_moves[i][1]
                self.trajectory = np.append(self.trajectory, [self.current],axis=0)
            else:
                i = randint(0, 3)
                self.graph.add_edge(possible_moves[i][0], possible_moves[i][1])
                self.current = possible_moves[i][1]
                self.trajectory = np.append(self.trajectory, [self.current],axis=0)

    def clear(self, init=(0,0)):
        self.__init__(init)

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
        RandomWalk.step(length)
        list[i,:,:] = RandomWalk.trajectory
        RandomWalk.clear()

    return list