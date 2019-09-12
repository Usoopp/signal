# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 10:44:03 2019

@author: xiaozhang
"""

##　estimation_background from falcon2d estimation_background.m
from pywt import wavedec,waverec
import numpy as np
import matplotlib.pyplot as plt
t = np.linspace(-100,100,50)
bg = 5
y = 50*np.exp(-t**2/(2*2^2)) + bg
plt.plot(t,y)

iter = 5
x_filt = y
th = 1
for i in range(iter):
     #wavelet transform

    coeffs = wavedec(x_filt,'db3',level=3)
    cA = coeffs[0]
    cD =  []
    # 令高频信息为0，也就是令cDn全部设置为0
    for j in range(1,len(coeffs)):     
         a = np.squeeze( np.array([np.zeros([np.size(coeffs[j]),1 ])]) )
         cD.append(a)  
    cD.insert(0,cA)

    # inverse wavelet transform by only using low-freq components  
    x_new = waverec(cD, 'db3')
    if th > 0:
    # cut off values over current estimated background level.
        eps = np.sqrt(abs(x_filt))/2
        ind = y > (x_new + eps)
        x_filt[ind] = x_new[ind]+eps[ind]
        
        # re-estimate background 
        coeffs = wavedec(x_filt,'db3',level=3)
        cA = coeffs[0]
        cD =  []
        for j in range(1,len(coeffs)):     #排除cA5,cDn全部设置为0
             a = np.squeeze( np.array([np.zeros([np.size(coeffs[j]),1 ])]) )
             cD.append(a)  
        cD.insert(0,cA)

        x_new = waverec(cD, 'db3')
        
def est_bg(y, iter):
    x_filt = y
    th = 1
    for i in range(iter):
     #wavelet transform
        coeffs = wavedec(x_filt,'db6',level=5)
        cA = coeffs[0]
        cD =  []
        # 令高频信息为0，也就是令cDn全部设置为0
        for j in range(1,len(coeffs)):     
             a = np.squeeze( np.array([np.zeros([np.size(coeffs[j]),1 ])]) )
             cD.append(a)  
        cD.insert(0,cA)
        
        # inverse wavelet transform by only using low-freq components  
        x_new = waverec(cD, 'db6')
        if th>0:
         #cut off values over current estimated background level.
            eps = np.sqrt(abs(x_filt))/2
            ind = y > (x_new + eps)
            x_filt[ind] = x_new[ind]+eps[ind]
            
            # re-estimate background 
            coeffs = wavedec(x_filt,'db6',level=5)
            cA = coeffs[0]
            cD =  []
            # 令高频信息为0，也就是令cDn全部设置为0
            for j in range(1,len(coeffs)):     
                 a = np.squeeze( np.array([np.zeros([np.size(coeffs[j]),1 ])]) )
                 cD.append(a)  
            cD.insert(0,cA)
          
            x_new = waverec(cD, 'db6')
    return x_new
    


#est_bg(y,5)
    
    
    
