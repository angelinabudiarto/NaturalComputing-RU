#Exercise 3 (ensemble learning)
#Group 8: Bono, Guus, Charlotte

import math
import matplotlib.pyplot as plt
import numpy as np

def majority_vote_prob(c_strong, c_weak, p_strong, p_weak):
    # equal weight majority vote

    maj_weak = math.floor((c_strong+c_weak)/2 + 1) #majority of only weak classifiers (ensemble), amount strong classifier = w (weight)
    maj_strong = max(maj_weak - c_strong, 0) #majority of only tje strong classifiers

    prob = 0

    # strong classifier is correct
    for i in range(maj_strong, c_weak+1):
        prob += p_strong * math.comb(c_weak, i) * math.pow(p_weak, i) * math.pow(1-p_weak, c_weak-i)

    # strong classifier is incorrect
    for j in range(maj_weak, c_weak+1):
        prob += (1- p_strong) * math.comb(c_weak, j) * math.pow(p_weak, j) * math.pow(1-p_weak, c_weak-j)

    return prob

def plot_majority_vote_prob(max_range, c_weak, p_strong, p_weak):
    # weighted majority vote (strong classifier has larger weight)

    weights_w = [i for i in range(0, max_range)]
    result_w = [majority_vote_prob(w, c_weak, p_strong, p_weak) for w in weights_w]
    print("Majority vote probabilities (weighted) for different weights: ", result_w)

    plt.figure()
    plt.plot(weights_w, result_w)
    plt.xlabel("Weights of strong classifier")
    plt.ylabel("Probability correct decision")
    plt.title("Weighted majority vote given different weights of the strong classifier")
    plt.show()

def adaboost_m1(error):
    # weight according to the adaboost.m1 algorithm (updated weight)

    w = 1 #w_old
    alpha = np.log((1 - error) / error)
    w *= np.exp(alpha) #w_new

    return w

def weights_adaboost_m1(error_weak, error_strong):
    # expected errors of the strong and weak classifiers are used to compute respective weights

    w_strong = adaboost_m1(error_strong)
    print("Weight strong classifier = ", w_strong)
    w_weak = adaboost_m1(error_weak)
    print("Weight weak classifier = ", w_weak)

def plot_w_baselearner(max_range):
    weights_w = x = [i/max_range for i in range(1,max_range)]
    result_w = [adaboost_m1(w) for w in weights_w]
    alpha_w = [math.log(i) for i in result_w]

    print("Probabilities for different the weights by adaboost: ", result_w)

    plt.figure()
    plt.plot(weights_w, result_w)
    plt.xlabel("Error of the learner")
    plt.ylabel("Probability correct decision")
    plt.axvline(x=0.5, color='g', linestyle='--')
    plt.title("Weights of adaboost.m1 given different errors")
    plt.show()

    plt.figure()
    plt.plot(weights_w, alpha_w)
    plt.xlabel("Error of the learner")
    plt.ylabel("Alpha")
    plt.axvline(x=0.5, color='g', linestyle='--')
    plt.title("Weights of adaboost.m1 given different errors")
    plt.show()


print("----- Exercise 3 (group 8) -----")

## Question 3a
print("-- Question 3a")
c_weak = 10
p_weak = 0.6
c_strong = 1
p_strong = 0.75
print("Probability of majority vote (with c_weak = ",
      c_weak, ", c_strong = ", c_strong, ", p_weak = ", p_weak, ", p_strong = ", p_strong,
      ") = ", majority_vote_prob(c_strong, c_weak, p_strong, p_weak))

## Question 3b
print("-- Question 3b")
#plot_majority_vote_prob(20+1, c_weak, p_strong, p_weak)
plot_majority_vote_prob(15+1, c_weak, p_strong, p_weak)

## Question 3c
print("-- Question 3c")
error_weak = 1-p_weak
error_strong = 1-p_strong
weights_adaboost_m1 (error_weak, error_strong)

## Question 3d
print("-- Question 3d")
plot_w_baselearner(1500)

