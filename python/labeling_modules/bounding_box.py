#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2017 Francisco Paisana.
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#

import numpy as np
import matplotlib.pyplot as plt

class BoundingBox:
    def __init__(self,time_bounds,freq_bounds):
        if len(time_bounds)!=2 or type(time_bounds[0]) is not int:
            raise ValueError('ERROR: The time interval {} does not have integer bounds'.format(time_bounds))
        self.time_bounds = time_bounds
        if len(freq_bounds)!=2 or np.max(freq_bounds)>0.5 or np.min(freq_bounds)<-0.5:
            raise ValueError('ERROR: The frequency bounds have to be normalized')
        self.freq_bounds = freq_bounds

    def is_equal(self,box):
        return box.time_bounds==self.time_bounds and box.freq_bounds==self.freq_bounds

    def time_intersection(self,tinterv):
        tstart = max(tinterv[0],self.time_bounds[0])
        tend = min(tinterv[1],self.time_bounds[1])
        if tend<=tstart:
            return None
        return (tstart,tend)

    def freq_intersection(self,finterv):
        fstart = max(finterv[0],self.freq_bounds[0])
        fend = min(finterv[1],self.freq_bounds[1])
        if fend<=fstart:
            return None
        return (fstart,fend)

    def box_intersection(self,box):
        tintersect = self.time_intersection(box.time_bounds)
        if tintersect is None:
            return None
        fintersect = self.freq_intersection(box.freq_bounds)
        if fintersect is None:
            return None
        return BoundingBox(tintersect,fintersect)

def find_tx_intervals(x):
    thres = 1e-5
    stepups=[i+1 for i in range(len(x)-1) if x[i]<thres and x[i+1]>=thres]
    stepdowns=[i+1 for i in range(len(x)-1) if x[i]>=thres and x[i+1]<thres]
    n_intervs = max(len(stepups),len(stepdowns))
    if x[0]>=thres and x[-1]>=thres:
        n_intervs += 1
    prev = 0
    l = [None]*n_intervs
    for j in range(len(l)):
        i2 = stepdowns[j] if j<len(stepdowns) else len(x)
        i = stepups[j] if j<len(stepups) and stepups[j]<i2 else prev
        l[j] = (i,i2)
        if i2==len(x):
            break
        prev = stepups[j]
        # i = stepups[j+jinc]
    return l

def find_tx_intervals_old(x): # NOTE: For some reason this version although simpler is super slow
    thres = 1e-5
    i=0
    l=[]
    while i < len(x):
        try:
            i = next(j for j in range(i,len(x)) if x[j]>=thres)
        except StopIteration:
            break
        try:
            i2 = next(j for j in range(i+1,len(x)) if x[j]<thres)
        except StopIteration:
            i2=len(x)
        l.append((i,i2))
        i = i2+1
    return l

def find_frequency_bounds(x,fftsize,thres=0.05):
    X=np.fft.fftshift(np.abs(np.fft.fft(x,fftsize))**2)
    Xcentre = np.sum(np.arange(X.size)*X)/np.sum(X)

    # find left bound
    Xstart = int(np.round(Xcentre-X.size/2))
    Xleftrange = np.mod(range(Xstart,int(Xcentre)+1),X.size)
    # left_bound = next(i for i in Xleftrange if X[i] > X[Xcentre]*thres)
    csum_left = np.cumsum(X[Xleftrange])
    left_bound = next(j+Xstart for j in range(csum_left.size) if csum_left[j]>thres*csum_left[-1])

    # find right bound
    Xend = int(np.round(Xcentre+X.size/2))
    Xrightrange = np.mod(range(int(Xcentre),Xend),X.size)
    # right_bound = next(i for i in Xrightrange if XdB[i] < XdB[Xcentre]*thres)
    csum_right = np.cumsum(X[Xrightrange])
    right_bound = next(j+Xcentre for j in range(csum_right.size) if csum_right[j]>=(1-thres)*csum_right[-1])

    interv = ((left_bound-0.5)/float(X.size)-0.5,(right_bound+0.5)/float(X.size)-0.5)

    # Y=X
    # zeroidxs = np.flatnonzero(X==0)
    # Y[zeroidxs] = np.min(X[np.flatnonzero(X)])
    # XdB = 10*np.log10(Y)
    # XdB = XdB-np.mean(XdB)#)/(np.max(XdB)-np.min(XdB)) # do i need to scale?
    # print 'centre:',Xcentre,'left bound:',left_bound,'right bound:',right_bound
    # plt.plot(XdB)
    # plt.plot(range(int(left_bound),int(right_bound)+1),np.ones(int(right_bound-left_bound+1))*np.max(XdB),'x')
    # plt.show()

    return interv

# def find_interv_freq_bounds(x,intervs=None):
#     if intervs is None:
#         intervs = [(0,x.size)]
#     l = []
#     for i in intervs:
#         y=x[i[0]:i[1]]
#         l.append(find_frequency_bounds(y,y.size))
#     return l

import time

def compute_bounding_box(x):
    print 'ola tudo bem. Isto e o tamanho:',x.size
    start_time = time.time()
    tinterv_list = find_tx_intervals(x)
    print 'number of boxes:',len(tinterv_list),'elapsed time(time intervals):',time.time()-start_time
    start_time = time.time()
    finterv = find_frequency_bounds(x,x.size) # FIXME: Make a smarter frequency estimator that partitions the signal
    print 'elapsed time(freq intervals):',time.time()-start_time
    # into smaller intervals and computes the average frequency bounds of each
    boxes = [BoundingBox(i,finterv) for i in tinterv_list]
    return boxes