from randomwalks import UniformRandomWalk as URW
from randomwalks import GreedyRandomWalk as GRW
import numpy as np
import pylab

UniRanWalk = URW()
GreRanWalk = GRW()
N = 10000
for i in range(N):
    UniRanWalk.step()
    GreRanWalk.step()

pylab.title("Random Walks ($N = " + str(N) + "$ steps)") 
pylab.plot(UniRanWalk.trajectory[:,0], UniRanWalk.trajectory[:,1], color='red', label='Uniform RW')
pylab.plot(GreRanWalk.trajectory[:,0], GreRanWalk.trajectory[:,1], color='blue', label='Greedy RW') 
pylab.show()