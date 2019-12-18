import pandas as pd
import stableRANK_I as sr
import numpy as np
inf=float("inf")
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import _pickle as pickle
from ripser import ripser
import math
import randomwalks as rw

## Note: stableRANK_I is a module written by and copyrighted to Wojciech
## Chachólski, wojtek[at]@kth.se, and is not included in the GitHub repo.

def barcode(matrix,maxdim=1, coeff=2, thresh=inf):
    distance_matrix=True
    do_cocycles=False
    dgms=ripser(matrix, maxdim, thresh, coeff, distance_matrix, do_cocycles)["dgms"]
    i=0
    dic={}
    while i<=maxdim:
        dic["H"+str(i)]=dgms[i]
        i=i+1
    return sr.bc(dic)

def compute_stable_rank(matrix,homology,maxdim=2):

    maxdim=2
    thresh=inf
    coeff=3
    distance_matrix=True
    do_cocycles=False

    contours={"H0": [  [[0],[1]], ("area", inf, inf)] }
    bc_object = barcode(matrix,maxdim=maxdim)
    stable_rank=bc_object.stable_rank_max(contours)

    return stable_rank[homology]

def mean_stdv(D):

    sum_signature=D[0]
    for i in range(1,number_samples):
        sum_signature=sum_signature+D[i]

    common_domain=sum_signature.content[0]

    extended_signatures=[]
    for i in range(number_samples):
        extended_signatures_values=((D[i].extension(common_domain)).content[1])
        extended_signatures.append(list(extended_signatures_values))
    mean=np.mean(extended_signatures,axis=0)
    std_dev=np.std(extended_signatures,axis=0)
    return list([common_domain,mean,mean-std_dev,mean+std_dev])

def plot_stats_summaries(l,labels,c):
    reduct="no"
    plt.figure(figsize=(20, 20))
    for i,x in enumerate(l):
        common_domain=x[0]
        mean=x[1]
        mean_min_std=x[2]
        mean_plus_std=x[3]
        plt.subplot(2,math.ceil(len(l)/2),i+1)

        plt.plot(common_domain,mean,linewidth=2,label="{0}".format(labels[i]),color=c)
        plt.fill_between(common_domain, mean_min_std, mean_plus_std,alpha=0.2,color=c)
        plt.legend()

def plot_stats_summaries_alltogether(l,labels):
    reduct="no"
    plt.figure(figsize=(20, 20))
    for i,x in enumerate(l):
        common_domain=x[0]
        mean=x[1]
        mean_min_std=x[2]
        mean_plus_std=x[3]
        plt.plot(common_domain,mean,linewidth=2,label="{0}".format(labels[i]))
        plt.fill_between(common_domain, mean_min_std, mean_plus_std,alpha=0.2)
        plt.legend()


if __name__ == '__main__':
    number_samples=200
    time=100
    homology="H1"
    stable_rank_samples_greedy=[]
    RW = rw.GreedyRandomWalk('box',10)
    distance_list = rw.Sample(RW, time, number_samples)
    distance_matrices = distance_list[0] # 0 or 1 for choosing distance function.

    for i in range(number_samples):
        matrix = distance_matrices[i]
        stable_rank_samples_Greedy.append(compute_stable_rank(matrix,homology,maxdim=1)) # This is just a dict with above objects
    stable_rank_samples_greedy=pd.Series(stable_rank_samples_greedy)

    stable_rank_samples_uniform=[]
    RW = rw.UniformRandomWalk('box',10)
    distance_list = rw.Sample(RW, time, number_samples)
    distance_matrices = distance_list[0] # 0 or 1 for choosing distance function.


    for i in range(number_samples):
        matrix = distance_matrices[i]
        stable_rank_samples_uniform.append(compute_stable_rank(matrix,homology,maxdim=1)) # This is just a dict with above objects
    stable_rank_samples_uniform=pd.Series(stable_rank_samples_uniform)

    # This things plots the mean pcf and the stdv around it
    shapes_stats_summaries=[]
    shapes_stats_summaries.append(mean_stdv(stable_rank_samples_greedy))
    shapes_stats_summaries.append(mean_stdv(stable_rank_samples_uniform))

    number_samples=100
    time=100
    homology="H0"
    stable_rank_samples=[]
    RW = rw.UniformRandomWalk('box',10)
    distance_list = rw.Sample(RW, time, number_samples)
    distance_matrices = distance_list[0] # 0 or 1 for choosing distance function.


    for i in range(number_samples):
        matrix = distance_matrices[i]
        stable_rank_samples.append(compute_stable_rank(matrix,homology,maxdim=1)) # This is just a dict with above objects
    stable_rank_samples=pd.Series(stable_rank_samples)
