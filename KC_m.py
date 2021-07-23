''' -*- coding: utf-8 -*-
This is the on python3 code for the KC model, main implementation, in
"Apparently similar neuronal dynamics may lead to different collective repertoire"

run using python3 KC_m.py on a terminal

programed by Margarita M. Sanchez Díaz and Eyisto J. Aguilar Trejo
'''

# ///--- KC_m ----///

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import datetime

a1 = datetime.datetime.now()

#Parameters
N = 5000   # Neurons
Avg_degree = 10   #Connectivity <k>. Here k_in=k_out so no distinction is done.
pi = 0.6   # rewiring probability
r1 = 0.001 # the spontaneous neuron activation frequency

# ///---- States ----///
#Q: quiescent, E: excited, R:refractory
Q = 0
E = 1
R = 2 or 3 or 4
S = np.random.randint(0, 4, size=N)
stepnum = 1000   #time steps at each value of sigma

# ///---- Network + weightsMatrix ----///
conectivityMatrix = nx.watts_strogatz_graph(N, Avg_degree, pi, seed=None)
NeighborMat = np.zeros((N, 5*Avg_degree), dtype=int)-(int(1))
count = np.zeros(N,dtype=int)
c=0
for i in list(conectivityMatrix.nodes): #For the list of nodes i
        pos=0
        
        for j in list(conectivityMatrix.neighbors(i)): #For each neighbors j of i
            NeighborMat[i,pos]=int(j)
            pos=pos+1
            count[c]=count[c]+1
        c=c+1

weightsMatrix = np.zeros((N, 5*Avg_degree))+-1 #Memory
for i in range(N):
    for j in range(count[i]):
        if weightsMatrix[i,j]==-1:
            weightsMatrix[i,j]=np.random.uniform(0,1)
            for h in range(count[NeighborMat[i,j]]):
                if i==NeighborMat[NeighborMat[i,j],h]:
                    weightsMatrix[NeighborMat[i,j],h]=weightsMatrix[i,j]

del conectivityMatrix
activity = np.zeros(stepnum)
Time=np.zeros(stepnum)
f_s = []

# ///---- Dynamics ----///

sigma_0 = 0
sigma_f = 2
n_sigma = 21  # number of sigma values used beteen sigma_0 and sigma_F, including sigma_0 and sigma_f (i.e., Delta sigma= (sigma_f-sigma_0)/(n_sigma-1) 

sigma_values = np.linspace(sigma_0, sigma_f, n_sigma)

for sigma in sigma_values:
    S = np.random.randint(0, 5, size=N)
    p_max = (2*sigma)/(Avg_degree-1)
    print(sigma)
    for t in range(stepnum):
        activity[t] = np.sum(S == E)
        Time[t]=t
        S_prev = S.copy()
        for i in range(N):
            if S_prev[i] == Q:
                if np.random.rand() <= r1:
                    S[i] = E
                else:
                    for j in range(count[i]): #for all j active neighbors
                        if (S_prev[NeighborMat[i,j]]==E):
                          if(np.random.uniform(0,1)<weightsMatrix[i][j]*p_max):
                                S[i]=E
                                break
            else:
                S[i] = (S_prev[i] + 1) % 5
    f_s.append(np.mean(activity)/N)      
    
# ///---- Data file ----///
    filename = 'act%sK%sPI%sSigma%s.txt' % (N,Avg_degree,int(pi*100),int(sigma*1000))
    file=open(filename,"w")
    np.savetxt(filename , np.column_stack([Time, activity]), fmt=['%d','%d'])
    file.close() 
filename2 = 'f_svsSigmaN%sK%sPI%s.txt' % (N,Avg_degree,int(pi*100))
file1=open(filename2,"w")
np.savetxt(filename2 , np.column_stack([sigma_values, f_s]), fmt=['%f','%f'])
file1.close()
plt.xlabel("$\sigma$")
plt.ylabel("$f_s$")
plt.plot(sigma_values,f_s,linestyle='solid',marker='o',color='blue')
plt.show()
a2 = datetime.datetime.now()
b=a2-a1
print("time",a2-a1)
