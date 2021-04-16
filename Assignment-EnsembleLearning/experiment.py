# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 13:13:30 2021

@author: guusv
"""
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors
from matplotlib.ticker import PercentFormatter
from numpy import genfromtxt
from sklearn.ensemble import IsolationForest
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
#%% load the data
data = genfromtxt('winequality-white.csv', delimiter=';')
y=data[1:len(data),11]
X=data[1:len(data),0:11]
#%% make a histogram
scores=[]
counts=[]
for i in range(1,11):
    scores.append(i)
    c=0
    for j in y:
        if i==j:
            c+=1
    counts.append(c)
plt.bar(scores,counts)
plt.xlabel('Quality scores(1-10)')
plt.ylabel('Counts')
plt.title('Distribution of quality scores')
plt.show()
#%% bin the scores into poor, mediocre and excellent 
labels = np.empty(len(y), dtype=str)
for i in range(len(y)):
    if y[i]<5:
        labels[i]='poor'
    elif y[i]>7:
        labels[i]='excellent'
    else:
        labels[i]='mediocre'
unique, counts = np.unique(labels, return_counts=True)
print(dict(zip(unique, counts)))
y=labels
#%% create train and test set
np.random.seed(1)
indices = np.random.permutation(X.shape[0])

idx_train, idx_test = indices[:int(len(X)*0.80)],  indices[int(len(X)*0.80):]
X_train, X_test = X[idx_train,:], X[idx_test,:]
y_train, y_test = y[idx_train], y[idx_test]
#%% make a new train set with proportion p mediocre samples
p=4
[idx_e] = np.where(y_train=='e')
[idx_m] = np.where(y_train=='m')
[idx_p] = np.where(y_train=='p')
m = int((len(idx_e)+len(idx_p))/2)
idx_m=idx_m[0:int(p*m)]
idx_train=np.concatenate((idx_e,idx_m,idx_p))
X_train, y_train = X_train[idx_train,:], y_train[idx_train]


#%%
n=500
d=10

#%% train an isolation forest and random forest on top
iso_forest = IsolationForest(random_state=0, n_estimators=n).fit(X_train)
outliers = iso_forest.predict(X_train)
[idx_out]=(outliers<0).nonzero()
X_out, y_out= X_train[idx_out], y_train[idx_out]
p,e = y_out =='p', y_out=='e'
print('nr detected outliers', len(y_out))
print('percentage outstanding wines', sum(p+e)/len(y_out))
print('undetected outstanding wines', 363-sum(p+e))
out_forest = RandomForestClassifier(max_depth=d, random_state=0, n_estimators=n)
out_forest.fit(X_out,y_out)
pred_out_train = out_forest.predict(X_out)
print('training score', sum(pred_out_train==y_out)/len(y_out))

#test the model
outliers = iso_forest.predict(X_test)
[idx_out]=(outliers<0).nonzero()
X_out, y_out= X_test[idx_out], y_test[idx_out]
pred_out_test = out_forest.predict(X_out)
print('test score', sum(pred_out_test==y_out)/len(y_out))
print(classification_report(y_out, pred_out_test))

#%% train regular random forest
n=500
d=10
print(n,d)
reg_forest = RandomForestClassifier(max_depth=d, random_state=0, n_estimators=n)
reg_forest.fit(X_train,y_train)
pred_reg_train = reg_forest.predict(X_train)
print('training score', sum(pred_reg_train==y_train)/len(y_train))

#test the model
pred_reg_test = reg_forest.predict(X_test)
print('test score', sum(pred_reg_test==y_test)/len(y_test))
print(classification_report(y_test, pred_reg_test))

#%% results for the three experiments
#nr of trees
n=[10,50,100,500,1000,5000]
x=range(len(n))
e_p=np.array([16,16,16,17,17,16])/100
e_r=np.array([83,88,85,88,85,85])/100
m_p=np.array([98,98,98,98,98,98])/100
m_r=np.array([51,53,55,54,55,53])/100
p_p=np.array([11,12,13,12,12,12])/100
p_r=np.array([89,89,89,89,89,89])/100

plt.plot(x,e_p, label='precision excellent wines', color='red')
plt.plot(x,m_p, label='precision mediocre wines', color ='purple')
plt.plot(x,p_p, label='precision poor wines', color = 'blue' )
plt.plot(x,e_r, label='recall excellent wines', color='red', linestyle='dashed')
plt.plot(x,m_r, label='recall mediocre wines', color ='purple', linestyle='dashed')
plt.plot(x,p_r, label='recall poor wines', color = 'blue',linestyle='dashed')
plt.xticks(range(len(n)),n)
plt.xlabel('number of trees')
plt.ylabel('classification score')
plt.title('Classification results for different numbers of trees')
plt.show()

#%% depth of trees
d=[2,5,10,20,50,100]
x=range(len(d))
e_p=np.array([11,13,17,17,17,17])/100
e_r=np.array([63,73,88,88,88,88])/100
m_p=np.array([95,97,98,98,98,98])/100
m_r=np.array([47,52,54,54,54,54])/100
p_p=np.array([10,12,12,12,12,12])/100
p_r=np.array([81,86,89,86,86,86])/100

plt.plot(x,e_p, label='precision excellent wines', color='red')
plt.plot(x,m_p, label='precision mediocre wines', color ='purple')
plt.plot(x,p_p, label='precision poor wines', color = 'blue' )
plt.plot(x,e_r, label='recall excellent wines', color='red', linestyle='dashed')
plt.plot(x,m_r, label='recall mediocre wines', color ='purple', linestyle='dashed')
plt.plot(x,p_r, label='recall poor wines', color = 'blue',linestyle='dashed')
plt.xticks(range(len(d)),d)
plt.xlabel('depth of trees')
plt.ylabel('classification score')
plt.title('Classification results for different depths of trees')
plt.show()

#%% class imbalance

i=['4:1', '2:1', '1:1', '1:2', '1:4', '1:26(original)']
x=range(len(i))
e_p=np.array([10,11,17,23,40,100])/100
e_r=np.array([100,100,88,61,41,5])/100
m_p=np.array([100,99,98,97,95,93])/100
m_r=np.array([4,18,54,81,94,100])/100
p_p=np.array([7,8,12,25,39,100])/100
p_r=np.array([95,89,89,76,49,11])/100

plt.plot(x,e_p, label='precision excellent wines', color='red')
plt.plot(x,m_p, label='precision mediocre wines', color ='purple')
plt.plot(x,p_p, label='precision poor wines', color = 'blue' )
plt.plot(x,e_r, label='recall excellent wines', color='red', linestyle='dashed')
plt.plot(x,m_r, label='recall mediocre wines', color ='purple', linestyle='dashed')
plt.plot(x,p_r, label='recall poor wines', color = 'blue',linestyle='dashed')
plt.xticks(range(len(i)),i)
plt.xlabel('proportion samples excellent/poor : mediocre')
plt.ylabel('classification score')
plt.title('Effect of class imbalance w.r.t. mediocre wines')
plt.show()