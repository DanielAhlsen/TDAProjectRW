# Code based upon what's shamelessly stolen from Daniel :P
import numpy as np
from numpy.random import randint
from numpy.random import choice
import networkx as nx

class RandomWalk:
    """
    RandomWalk

    A RandomWalk in 2D.
    """
    def __init__(self, topology, radius, init = (0,0)):
        self.current = init
        self.graph = nx.Graph()
        self.topology = topology
        self.radius = radius
        self.graph.add_node(self.current)
        self.trajectory = np.array([self.current], dtype='int16')


    def takeStep(self,next_step):
        if self.current != next_step: #This prevents loops
            self.graph.add_edge(self.current, next_step)
        self.current = next_step
        self.trajectory = np.append(self.trajectory, [self.current],axis=0)

    def clear(self, init=(0,0)):
        self.__init__(self.topology, self.radius, init)

class UniformRandomWalk(RandomWalk):
    """
    UniformRandomWalk

    A Random Walk in 2D,
    """
    def takeStep(self):
        next_step = self.getStep(self.current)
        super().takeStep(next_step)

    #generate next step:
    def getStep(self,x):
        i, j = randint(2, size=2)
        xnew,ynew = (x[0] + (-1)**j * ((i+1) % 2) , x[1] + (-1)**j * (i % 2))
        #distinguish topology
        if self.topology == 'plane':
            return (xnew,ynew)
        elif self.topology == 'box':
            if max(abs(x[0]),abs(x[1])) <= self.radius-1:
                return (xnew, ynew)
            else:
                return (x[0],x[1])
            #Note: This means, the random walk just stays in this position for all remaining steps.
            #This needs to be considered when going for the distance space!
        elif self.topology == 'torus':
            if abs(xnew) > self.radius:
                return (-x[0], x[1])
            elif abs(ynew) > self.radius:
                return (x[0], -x[1])
            else:
                return (xnew, ynew)



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
            xnew, ynew = possible[choice(len(possible))]
        else:
            xnew, ynew = available[choice(4)]
        #... now pretend this is a transition from a simple random walk - and recycle the code
        #distinguish topology
        if self.topology == 'plane':
            return (xnew,ynew)
        elif self.topology == 'box':
            if max(abs(x[0]),abs(x[1])) <= self.radius-1:
                return (xnew, ynew)
            else:
                return (x[0],x[1])
        elif self.topology == 'torus':
            if abs(xnew) > self.radius:
                return (-x[0], x[1])
            elif abs(ynew) > self.radius:
                return (x[0], -x[1])
            else:
                return (xnew, ynew)



#Generates one trajectory of RandomWalk, up to time t=time (Does not reset afterwards, though!)
def Run(RandomWalk, time):
    traj = np.zeros((time+1,2))
    for n in range(time):
        RandomWalk.takeStep()
    traj = RandomWalk.trajectory
    G = RandomWalk.graph

    return (traj, G)


#Generates num trajectories of RandomWalk
def RepRun(RandomWalk, time, num):
    collection = list()
    for n in range(num):
        A = Run(RandomWalk, time)
        collection.append(A)
        RandomWalk.clear()

    return collection


#Returns the distance matrix according to the graph distance -- requires as input the result of Run(RW,time)
def GraphDistance(run):
    G = run[1]
    nodes = list(G.nodes())
    distances = dict(nx.all_pairs_shortest_path_length(G))
    matrix = np.zeros((len(nodes),len(nodes)))

    for i in range(len(nodes)):
        for j in range(len(nodes)):
            matrix[i][j] = distances[nodes[i]][nodes[j]]

    return matrix


#Returns the distance matrix according to maximum distance between vertices and edge midpoints
def MaxDistance(run, topology, radius):
    G = run[1]
    nodes = list(G.nodes())
    edges = list(G.edges())
    l = len(nodes)+len(edges)
    matrix = np.zeros((l,l))

    #easy cases first
    if topology != 'torus':
        #introduce midpoints
        for e in edges:
            mp = ((e[0][0]+e[1][0])/2, (e[0][1]+e[1][1])/2)
            nodes.append(mp)
        for i in range(len(nodes)):
            for j in range(len(nodes)):
                matrix[i][j] = max(abs(nodes[i][0]-nodes[j][0]),abs(nodes[i][1]-nodes[j][1]))
        return matrix
    #now some technicialities (topology =='torus')
    else:
        diam = 2*radius + 1
        for e in edges:
            if (abs(e[0][0])==radius and e[0][0]== -e[1][0]):
                mp = ((2*e[0][0]+1)/2, e[0][1])
            elif (abs(e[0][1])==radius and e[0][1]== -e[1][1]):
                mp = (e[0][0], (2*e[0][1]+1/2))
            else:
                mp = ((e[0][0]+e[1][0])/2, (e[0][1]+e[1][1])/2)
            nodes.append(mp)
        for i in range(len(nodes)):
            for j in range(len(nodes)):
                dist0 = min(abs(nodes[i][0]-nodes[j][0]), diam-abs(nodes[i][0]-nodes[j][0]))
                dist1 = min(abs(nodes[i][1]-nodes[j][1]), diam-abs(nodes[i][1]-nodes[j][1]))
                matrix[i][j] = max(dist0,dist1)
        return matrix


#rescale all distances s.t. the diameter of the space is 1
def Scaling(matrix):
    A = matrix/np.amax(matrix)
    return A


#Generating num many trajectories of length <= time,
#and giving both distance matrices for each of them
def Sample(RandomWalk, time, num):
    collection1 = RepRun(RandomWalk, time, num)
    collection2 = collection1.copy()
    gdists = []
    mdists = []
    for i in collection1:
        g = Scaling(GraphDistance(i))
        gdists.append(g)
    for i in collection2:
        m = Scaling(MaxDistance(i, RandomWalk.topology, RandomWalk.radius))
        mdists.append(m)
    return (gdists, mdists)
