# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 23:40:18 2017

@author: Family
"""

#!/usr/bin/python
# -*- coding: utf-8 -*-


import numpy as np
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

for i in range(100): print(' ')

SAMPLE_PER_CLASS=100
samples_class_pos=np.random.multivariate_normal([4, 0],[[2, 0],[0, 2]],SAMPLE_PER_CLASS)
samples_class_neg=np.random.multivariate_normal([0, 4],[[2, 0],[0, 2]],SAMPLE_PER_CLASS)

#plt.figure(1)
#plt.plot(samples_class_pos[:, 0], samples_class_pos[:, 1], 'ro')
#plt.plot(samples_class_neg[:, 0], samples_class_neg[:, 1], 'bo')

#define Macros
TEST_PERCENT=0.1  #  0<TEST_PERCENT<1
TRAIN_PERCENT=1-TEST_PERCENT
CLASS_NUM=2
ITERR_NUM=10        # cross validation

samples_all = np.concatenate((samples_class_pos, samples_class_neg))
targets_all = np.concatenate((np.zeros([SAMPLE_PER_CLASS,1]), np.ones([SAMPLE_PER_CLASS,1])))
sample_number=SAMPLE_PER_CLASS*CLASS_NUM

h0=np.linspace(2.5,15,20)
performance=np.zeros(len(h0))
H=np.power(h0,2)
print(H)
number=0
for h in H:
    iteration_error=np.zeros(ITERR_NUM, dtype=int)
    iteration=0
    for iteration in range(ITERR_NUM):    
        samples, test_samples, target_samples, target_test_samples = train_test_split(samples_all, targets_all, test_size=TEST_PERCENT, random_state=iteration)
        
        feature_dist=np.zeros(samples.shape)
        
        for sample in range((test_samples.shape)[0]): 
            #distance from all features (axis)
            feature_dist[:,:]=samples-test_samples[sample,:]   
            
            feature_dist_pow2=np.power(feature_dist, 2)
            sample_dist=np.sum(feature_dist_pow2, axis=1)
            
            sample_dist_sorted=np.sort(sample_dist)
            sample_dist_argsort=np.argsort(sample_dist)
            
            dist_of_samples_in_ball  = sample_dist_sorted[sample_dist_sorted<h]
            
            if (len(dist_of_samples_in_ball)==0):
                print('There is no sample in this ball.')
                
            samples_in_ball          = sample_dist_argsort[0:len(dist_of_samples_in_ball)]
            target_of_samples_in_ball= target_samples[samples_in_ball]
            hist_class=np.histogram(target_of_samples_in_ball, bins=np.arange(CLASS_NUM+1))[0]
            parzen_window_class_assign=np.argmax(hist_class)
            
            #print(dist_of_samples_in_ball)
            #print(samples_in_ball)
            #print(target_of_samples_in_ball)
            #print(hist_class)
            #print(parzen_window_class_assign)
            #print('parzen assigned class={} real class={}'.format(parzen_window_class_assign,target_test_samples[sample]))
            if (target_test_samples[sample]!=parzen_window_class_assign): iteration_error[iteration]=iteration_error[iteration]+1
        
    error=np.sum(iteration_error)
    number_of_tests=ITERR_NUM*len(test_samples);
    performance[number]=(1-(error/(number_of_tests)))*100
    print('h={}   error ={}   number_of_tests={}  performancce={}'.format(h0[number], error, number_of_tests, performance[number]))
    number=number+1

plt.figure(2)
plt.plot(h0,performance,c='b')
plt.xlabel('h')
plt.ylabel('Performance')
plt.title('Performane of Parzen window classifier')
plt.grid()
plt.show()


