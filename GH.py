''' -*- coding: utf-8 -*-
programed by Margarita M. Sanchez Díaz and Eyisto J. Aguilar Trejo
This is the on python3 code for the GH model in
"Apparently similar neuronal dynamics may lead to different collective repertoire"

run using python3 GH.py on a terminal
'''

# ///--- Greenberg Hastings Model ----///
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import datetime
import random

a1 = datetime.datetime.now()

#Parameters
N = 5000  #Neurons
Avg_degree = 10    #Connectivity <k>. Here k_in=k_out so no distinction is done.
pi = 0.6  #Rewiring probability 
scale = 1/12.5 #Lambda=12.5
r1 = 1e-3  # Spontaneous neuron activation
r2 = 0.3 #Probability of quiescent state
stepnum = 1000 #time steps at each value of T

# ///---- States and Control Parameter ----///
# Q = quiescent, E = excited, R = refractory, T = threshold
Q = 0
E = 1
R = 2
T_0 = 0
T_F= 0.4
n_t= 41 # number of T values used beteen T_0 and T_F, including T_0 and T_f (i.e., Delta T= (T_f-T_0)/(n_t-1) 
T_list = np.linspace(T_0, T_F, n_t)
next_state = np.random.randint(0, 3, size=N)
activity = np.zeros(stepnum)
Time=np.zeros(stepnum)
mean_series = []

# ///---- Network + weightsMatrix ----///
conectivityMatrix = nx.watts_strogatz_graph(N, Avg_degree, pi, seed=None)

neighb = np.zeros((N, 5*Avg_degree), dtype=int)-(int(1))
count = np.zeros(N,dtype=int)
c=0
for i in list(conectivityMatrix.nodes): #For the list of nodes i
        pos=0
        
        
        for j in list(conectivityMatrix.neighbors(i)): #For each neighbors j of i
            neighb[i,pos]=int(j)
            pos=pos+1
            count[c]=count[c]+1
        c=c+1


weightsMatrix = np.zeros((N, 5*Avg_degree))+-1 #Memory
for i in range(N):
    for j in range(count[i]):
        if weightsMatrix[i,j]==-1:
            weightsMatrix[i,j]=np.random.exponential(scale)
            for h in range(count[neighb[i,j]]):
                if i==neighb[neighb[i,j],h]:
                    weightsMatrix[neighb[i,j],h]=weightsMatrix[i,j]

del conectivityMatrix
# ///---- Dynamics ----///
for T in T_list:
    print(float("{0:.2f}".format(T)))
    next_state = np.random.randint(0, 3, size=N)
    for t in range(stepnum):
        activity[t] = np.sum(next_state == E)
        Time[t]=t
        previous_state = next_state.copy()
        for i in range(N):
            if previous_state[i] == Q:
                if np.random.uniform(0,1) <= r1:
                    next_state[i] = E
                else:
                    activity_neighbors=0
                    for j in range(count[i]): #for all j active neighbors
                        if (previous_state[neighb[i,j]]==E):
                            activity_neighbors=activity_neighbors+weightsMatrix[i,j]
                    if activity_neighbors >= T:
                        next_state[i] = E
            elif previous_state[i] == E:
                next_state[i] = R
            else:
                if np.random.uniform(0,1) <= r2:
                    next_state[i] = Q
    mean_series.append(np.mean(activity))   
    
# ///---- Data file ----///
    filename = 'actN%sK%sPI%sT%s.txt' % (N,Avg_degree,int(pi*100),int(T*1000))
    file=open(filename,"w")
    np.savetxt(filename , np.column_stack([Time, activity]), fmt=['%d','%d'])
    file.close()
plt.plot(T_list,mean_series,linestyle='solid',marker='o',color='blue')
a2 = datetime.datetime.now()
b=a2-a1
print("time",a2-a1)
