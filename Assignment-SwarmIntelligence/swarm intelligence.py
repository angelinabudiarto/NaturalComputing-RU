# -*- coding: utf-8 -*-
"""
Created on Sun Feb 14 15:26:25 2021

@author: guusv
"""
import numpy as np
from sklearn import datasets
from matplotlib import pyplot as plt
#%%

def CreateDataset1(n):
    #initialize dataset with n rows and z1,z2,class
    X = np.zeros((n,2))
    Y = np.zeros(n)
    for i in range(n):
        #Z1
        X[i,0]=np.random.uniform(-1,1)
        #Z2
        X[i,1]=np.random.uniform(-1,1)
        #assign classes
        if (X[i,0] >= 0.7) or (X[i,0]<=0.3 and X[i,1]>=-0.2 - X[i,0]):
            Y[i]=1
        else:
            Y[i]=0
    return X , Y

def CreateDataset2():
    iris = datasets.load_iris()
    X = iris.data
    Y = iris.target
    return X, Y

def kmeans(Nc,X, T):
    No,Nd = X.shape
    #initialize clusters 
    M = np.zeros((Nc,Nd))
    for i in range(Nc):
        for j in range(Nd):
            # set centroid of cluster i in dimension j as random between min and max of that dimension
            M[i,j] = np.random.uniform(np.min(X[:,j]),np.max(X[:,j]))
    #iterate kmeans
    for t in range(T):
        #calculate distances to centroids
        d = np.zeros((No,Nc))
        for m in range(Nc):
            d[:,m] = np.sqrt(np.sum((X-M[m,:] )**2,axis=1))
        #assign data to closest centroid
        Ypred=np.argmin(d,axis=1)
        #print(q_error(X,Ypred))
        #recompute cluster centroids
        for i in range(Nc):
            C=X[np.argwhere(Ypred==i)]
            M[i,:]=np.mean(C,axis=0)
    return Ypred, M


def update_velocity(position, velocity, localbest, globalbest):
    Nc,Nd = position.shape
    #inertia weight
    w=0.72
    #acceleration
    c1=1.49
    c2=1.49
    #random weights
    r1=np.random.uniform(0,1,(Nc,Nd))
    r2=np.random.uniform(0,1,(Nc,Nd))
    #compute new velocity
    newvelocity=w*velocity + c1*r1*(localbest-position) + c2*r2*(globalbest-position)
    #print(newvelocity)
    return newvelocity

def initialize_particles(Nd,Nc,Np,X):
    Particles=[]
    for p in range(Np):
        #initialize cluster centroids
        M = np.zeros((Nc,Nd))
        for i in range(Nc):
            for j in range(Nd):
                # set centroid of cluster i in dimension j as random between min and max of that dimension
                M[i,j] = np.random.uniform(np.min(X[:,j]),np.max(X[:,j]))
        Particles.append(M)
    return Particles

def distance(z,m):
    return np.sqrt(np.sum((z-m)**2))

def fitness(X,c,centroids):
    Nc,Nd = centroids.shape
    f=0
    for m in range(Nc):
        C=X[np.argwhere(c==m)]
        d=0
        if(len(C)==0):
            Nc=Nc-1
        else:
            for z in C:
                d+=distance(z,centroids[m]) 
            d=d/len(C)
        f+=d
        
    f=f/Nc
    return f

def q_error(X,Ypred,centroids):
    Nc,Nd = centroids.shape
    ClusteredData=[]
    for c in range(Nc):
        C=X[np.argwhere(Ypred==c)]
        C=np.reshape(C,(len(C),Nd))
        ClusteredData.append(C)
    J=0
    for c in range(Nc):
        d=0
        for z in ClusteredData[c]:
            d += distance(z,centroids[c])/len(C)
        #print(d)
        J+=d
    q=J/Nc
    return q

def PSO(X,Nc,Np,maxiter):
    No,Nd = X.shape
    Particles=initialize_particles(Nd,Nc,Np,X)
    Local_best_f=np.ones(Np)*999
    Local_best = np.copy(Particles)
    Global_best_f = 999
    Global_best = np.copy(Particles[0])
    v=0
    v_init=np.ones((Nc,Nd))*v
    Particle_velocities = []
    for p in range(Np):
        Particle_velocities.append(v_init)
    #for each iteration
    for t in range(maxiter):
        #for each particle
        
        for p in range(Np):
            #for each datapoint
            C=np.zeros(No)
            for i in range(No):
                z=X[i]
                d=np.zeros(Nc)
                #for each centroid in particle
                for c in range(Nc):
                    m=Particles[p][c]
                    #calculate distance between datapoint and centroid
                    d[c]=distance(z,m)
                #assign datapoint to cluster with minimal distance
                C[i]=np.argmin(d)
            #compute fitness of particle using average weighted distance from data to centroids(slides)
            f=fitness(X,C,Particles[p])
            #f=q_error(X,C,Particles[p])
            #update local fitness for particle
            if f<Local_best_f[p]:
                Local_best[p]=np.copy(Particles[p])
                Local_best_f[p]=f
        #update global fitness
        if np.min(Local_best_f) < Global_best_f:
            Global_best= np.copy(Local_best[np.argmin(Local_best_f)])
            Global_best_f = np.min(Local_best_f)
        
        #update each particle
        for p in range(Np):
            Particle_velocities[p]=update_velocity(Particles[p],Particle_velocities[p],Local_best[p],Global_best)
        #print('pos: '+ str(Particles[0][0]) +' v: '+ str(Particle_velocities[0][0]))
        #print(Local_best_f[0])
        for p in range(Np):
            Particles[p]=Particles[p]+Particle_velocities[p]
        
    
    Ypred=np.ones(No)*999
    for i in range(No):
        z=X[i]
        d=np.zeros(Nc)
        #for each centroid in particle
        for c in range(Nc):
            m=Global_best[c]
            #calculate distance between datapoint and centroid
            d[c]=distance(z,m)
        #assign datapoint to cluster with minimal distance
        Ypred[i]=np.argmin(d)
    return Ypred, Global_best


# =============================================================================
# #%%
# #T=[1,2,3,5,10,15,20,30,50,70,100,130,150,200,250]
# #T=np.arange(1,10)
# T=[1,2,3,6,12,18,24,48,96,144,192]
# 
# #T=[1,2,3,5,7,10,50]
# 
# X,Y=CreateDataset2()
# plt.close('all')
# fig = plt.figure()
# fig.subplots_adjust(hspace=0.4, wspace=0.4)
# ax = fig.add_subplot(3, 4, 1)
# ax.scatter(X[:,0], X[:,1], c=Y)
# ax.set_title('Original classes')
# #delete 'magenta' for dataset1
# colordict=['red','blue','magenta']
# for t in range(len(T)):
#     print('iterations: ' + str(t))
#     np.random.seed(10)
#     #Nc=Nclusters,X,T=nriterations
#     #Ypred,centroids kmeans(3,X,t)
#     #                       X,Nc,Np,T
#     Ypred, centroids = PSO(X,3 ,5 ,T[t])
#     ax = fig.add_subplot(3, 4, t+2)
#     ax.scatter(X[:,0], X[:,1], c=Ypred)
#     ax.scatter(centroids[:,0],centroids[:,1], color=colordict)
#     ax.set_title('Iteration ' + str(T[t]))
#     print('fitness: '+str(fitness(X,Ypred,centroids)))
#     print('q error: '+str(q_error(X,Ypred,centroids)))
# =============================================================================

#%%
plt.close('all')
np.random.seed(10)
iterations=150
nrparticles=5
fig = plt.figure()
fig.subplots_adjust(hspace=0.4, wspace=0.4)
ax = fig.add_subplot(2, 3, 1)
colordict1=['red','blue']
colordict2=['red','blue', 'magenta']
#plot dataset 1
X1,Y1=CreateDataset1(400)
ax.scatter(X1[:,0], X1[:,1], c=Y1)
ax.set_title('Original classes, Dataset 1')
#apply kmeans
Ypred1_k,centroids1_k=kmeans(2,X1,iterations)
ax = fig.add_subplot(2, 3, 2)
ax.set_title('K-means after 150 iterations, Dataset 1')
ax.scatter(X1[:,0], X1[:,1], c=Ypred1_k)
ax.scatter(centroids1_k[:,0],centroids1_k[:,1], color=colordict1)
ax.set_xlabel('Quantization error: ' +str(q_error(X1,Ypred1_k,centroids1_k)))
print('fitness kmeans 1: '+str(fitness(X1,Ypred1_k,centroids1_k)))
print('q error kmeans 1: '+str(q_error(X1,Ypred1_k,centroids1_k)))

#apply PSO
Ypred1_pso, centroids1_pso = PSO(X1,2 ,nrparticles ,iterations)
ax = fig.add_subplot(2, 3, 3)
ax.set_title('PSO after 150 iterations, Dataset 1')
ax.scatter(X1[:,0], X1[:,1], c=Ypred1_pso)
ax.scatter(centroids1_pso[:,0],centroids1_pso[:,1], color=colordict1)
ax.set_xlabel('Quantization error: ' +str(q_error(X1,Ypred1_pso,centroids1_pso)))
print('fitness pso 1: '+str(fitness(X1,Ypred1_pso,centroids1_pso)))
print('q error pso 1: '+str(q_error(X1,Ypred1_pso,centroids1_pso)))

#plot dataset 2
X2,Y2=CreateDataset2()
ax = fig.add_subplot(2, 3, 4)
ax.scatter(X2[:,0], X2[:,1], c=Y2)
ax.set_title('Original classes, Dataset 2')
#apply kmeans
Ypred2_k,centroids2_k=kmeans(3,X2,iterations)
ax = fig.add_subplot(2, 3, 5)
ax.set_title('K-means after 150 iterations, Dataset 2')
ax.scatter(X2[:,0], X2[:,1], c=Ypred2_k)
ax.scatter(centroids2_k[:,0],centroids2_k[:,1], color=colordict2)
ax.set_xlabel('Quantization error: ' +str(q_error(X2,Ypred2_k,centroids2_k)))
print('fitness kmeans 2: '+str(fitness(X2,Ypred2_k,centroids2_k)))
print('q error kmeans 2: '+str(q_error(X2,Ypred2_k,centroids2_k)))

#apply PSO
Ypred2_pso, centroids2_pso = PSO(X2,3 ,nrparticles ,iterations)
ax = fig.add_subplot(2, 3, 6)
ax.set_title('PSO after 150 iterations, Dataset 2')
ax.scatter(X2[:,0], X2[:,1], c=Ypred2_pso)
ax.scatter(centroids2_pso[:,0],centroids2_pso[:,1], color=colordict2)
ax.set_xlabel('Quantization error: ' +str(q_error(X2,Ypred2_pso,centroids2_pso)))
print('fitness pso2: '+str(fitness(X2,Ypred2_pso,centroids2_pso)))
print('q error pso2: '+str(q_error(X2,Ypred2_pso,centroids2_pso)))





    
