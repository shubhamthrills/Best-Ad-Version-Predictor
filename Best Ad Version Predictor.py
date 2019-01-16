# -*- coding: utf-8 -*-
"""
Created on Mon Jan 14 20:23:21 2019

@author: Shubham Sagar
@Title: Best Ad Version Predictor
"""
import numpy as np													#Importing libraries
import matplotlib.pyplot as plt
import pandas as pd
dataset = pd.read_csv('Ads.csv')									#Importing the dataset
import random
import math
N=10000																#Number of Rows(Different Customers)
d=10																	#Number of column(Different Ads)

ads_selected_random=[]                                        #Implementing random Method
total_reward_r = 0
for n in range(0, N):
    ad_r=random.randrange(d)
    ads_selected_random.append(ad_r)
    reward_r=dataset.values[n, ad_r]
    total_reward_r=total_reward_r + reward_r
    
ad_ucbs_selected_ucb=[]                                     #Implementing Upper Confidence Bond
numbers_of_selections=[0]*d
sums_of_reward_ucbs=[0]*d
total_reward_ucb_ucb=0
for n in range(0, N):
    ad_ucb=0
    max_upper_bound_ucb=0
    for i in range(0, d):
        if (numbers_of_selections[i] > 0):
            average_reward_ucb = sums_of_reward_ucbs[i] / numbers_of_selections[i]
            delta_i = math.sqrt(3/2 * math.log(n + 1) / numbers_of_selections[i])
            upper_bound = average_reward_ucb + delta_i
        else:
            upper_bound = 1e400
        if upper_bound > max_upper_bound_ucb:
            max_upper_bound_ucb = upper_bound
            ad_ucb = i
    ad_ucbs_selected_ucb.append(ad_ucb)
    numbers_of_selections[ad_ucb] = numbers_of_selections[ad_ucb] + 1
    reward_ucb = dataset.values[n, ad_ucb]
    sums_of_reward_ucbs[ad_ucb] = sums_of_reward_ucbs[ad_ucb] + reward_ucb
    total_reward_ucb_ucb = total_reward_ucb_ucb + reward_ucb    

ads_selected=[]                                             #Implementing Thompson Sampling
numbers_of_rewards_1=[0]*d										  #Writting Program According to algo
numbers_of_rewards_0=[0]*d
total_reward=0

for n in range(0,N):
    ad=0
    max_random=0
    for i in range(0,d):
        random_beta=random.betavariate(numbers_of_rewards_1[i]+1,numbers_of_rewards_0[i]+1)
        if random_beta > max_random:
            max_random=random_beta
            ad=i
    ads_selected.append(ad)
    reward=dataset.values[n, ad]
    if reward==1:
        numbers_of_rewards_1[ad]=numbers_of_rewards_1[ad]+1
    else:
        numbers_of_rewards_0[ad]=numbers_of_rewards_0[ad]+1
    total_reward = total_reward+reward

plt.hist(ads_selected_random)                               #Visualising the results for random
plt.title('Graph for ads selections By Random')
plt.xlabel('Ad Number')
plt.ylabel('Number of times each ad was selected')
plt.show()

plt.hist(ad_ucbs_selected_ucb)                #Visualising the results for Upper Confidence bound
plt.title('Graph for ads selections By Upper Confidence bound')
plt.xlabel('Ad Number')
plt.ylabel('Number of times each ad was selected')
plt.show()

plt.hist(ads_selected)										#Visualising the results Thompson Sampling
plt.title('Graph for ads selections By Thompson Sampling')
plt.xlabel('Ad Number')
plt.ylabel('Number of times each ad was selected')
plt.show()