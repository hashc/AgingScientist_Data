#%load_ext autoreload
#%autoreload 2
import zipfile
import time
#import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter,defaultdict
import pickle
import numpy as np
import matplotlib.colors as mcolors
import matplotlib.cm as cm
import sys
import statsmodels.api as sm
import random
import json
import psutil
import os
import pandas as pd
import seaborn as sns
import tqdm

def star(i):
    res=''
    for a in [0.01,0.05,0.1]:
        if i<a:
            res+='*'
    return res
def print_memory():
    pid = os.getpid()
    p = psutil.Process(pid)
    info = p.memory_full_info()
    memory = info.uss / 1024. / 1024./1024.
    print('Memory used: {:.2f} GB'.format(memory)) 

def get_memory():
    pid = os.getpid()
    p = psutil.Process(pid)
    info = p.memory_full_info()
    memory = info.uss / 1024. / 1024./1024.
    return memory

def timelogger(func):
    def inner(*args, **kwargs): #1
        start = time.perf_counter()
        sm = get_memory()
        res = func(*args, **kwargs) 
        cm = get_memory()
        print("==Time: %.2f, Memory used: %.2f GB, Current Memory: %2f GB=="%(time.perf_counter()-start,cm-sm,cm)) 
        return res #2
    return inner

def fun_sortedbydate(plist,DateDict):
    if len(plist)>1:
        tmp = [(p,DateDict[p]) for p in plist]
        Sort = sorted(tmp,key = lambda item:item[1])
        res = [a for a,b in Sort]
    else:
        res = plist
    return res

    
@timelogger
def fun_save_pickle(data,fname):
    with open(fname,'wb')as f:
        pickle.dump(data,f)
    print("[ok] Saving %s"%fname)
    
@timelogger
def fun_load_pickle(fname):
    with open(fname,'rb')as f:
        res = pickle.load(f)
    print("[ok] Loading %s"%fname)
    return res


def fun_load_pickle_no_timer(fname):
    with open(fname,'rb')as f:
        res = pickle.load(f)
    return res


def OLSRegressFit(x,y):
    xx = sm.add_constant(x, prepend=True)
    res = sm.OLS(y,xx).fit()
    constant, beta = res.params
    r2 = res.rsquared
    return [constant,beta] 
def fun_get_csm(d):
    careerAgeRef,meanRefAge,sdRefAge=np.array([[k,np.nanmean(v),np.nanstd(v)] for k,v in sorted(d.items(), key = lambda x:x[0])]).T
    return careerAgeRef,meanRefAge,sdRefAge
def bootstrap_resample(X, n=None):
    """ Bootstrap resample an array_like
    Parameters
    ----------
    X : array_like
      data to resample
    n : int, optional
      length of resampled array, equal to len(X) if n==None
    Results
    -------
    returns X_resamples
    """
    if n == None:
        n = len(X)     
    resample_i = np.floor(np.random.rand(n)*len(X)).astype(int)
    X_resample = [X[i] for i in resample_i]
    return X_resample
def fun_get_csm_bootstrap_v1(tmp,n1=10,n2=1000,f=np.mean):
    bs = {}
    for k in tmp:
        v = np.array(tmp[k])
        new_v = []
        for _ in range(n1):
            new_v.append(f(bootstrap_resample(v, n=min(n2,len(v)))))
        bs[k] = new_v
    return bs
def fun_get_csm_bootstrap_v2(res,n1=10,n2=1000,f=np.mean):
    bs = defaultdict(lambda:[])
    for ni in range(n1):
        print(ni,n1,end='\r')
        resi = bootstrap_resample(res, n=min(n2,len(res)))
        tmpi = defaultdict(lambda:[])
        for ri in resi:
            for y in ri:
                tmpi[y].append(ri[y])
        tmpi = {y:tmpi[y] for y in tmpi}
        careerAgeRef,meanRefAge,sdRefAge = fun_get_csm(tmpi)
        for i,j in zip(careerAgeRef,meanRefAge):
            bs[i].append(j)
    return {i:bs[i] for i in bs}


def fun_window(Series,indexs=None,window_size=5):
    n = len(Series)
    if indexs is None:
        indexs = range(n)
    S1 = defaultdict(lambda:defaultdict(lambda:0))
    for i in range(n-window_size+1):
        for j in range(i,i+window_size):
            for wid in Series[indexs[j]]:
                S1[indexs[i]][wid]+=1
    return S1
def fun_distance(function=None,indexs=None,Series=None):
    return [function(Series[indexs[i]],Series[indexs[i+1]]) for i in range(len(indexs)-1)]

import scipy

def fun_kl_similarity(d1,d2):
    s1 = sum([d1[i] for i in d1])*1.0
    px = {i:d1[i]/s1 for i in d1 }
    s2 = sum([d2[i] for i in d2])*1.0
    py = {i:d2[i]/s2 for i in d2 }
    klist = list(set(list(d1.keys())+list(d2.keys())))
    return scipy.stats.entropy([px[i]+1e-5 if i in px else 1e-5 for i in klist],[py[i]+1e-5 if i in py else 1e-5 for i in klist])
def fun_ws_distance(d1,d2):
    s1 = sum([d1[i] for i in d1])*1.0
    px = {i:d1[i]/s1 for i in d1 }
    s2 = sum([d2[i] for i in d2])*1.0
    py = {i:d2[i]/s2 for i in d2 }
    klist = list(set(list(d1.keys())+list(d2.keys())))
    return scipy.stats.wasserstein_distance([px[i] if i in px else 0. for i in klist],[py[i] if i in py else 0. for i in klist])

def fun_jc_distance(d1,d2):
    s1 = sum([d1[i] for i in d1])*1.0
    px = {i:1 for i in d1 }
    s2 = sum([d2[i] for i in d2])*1.0
    py = {i:1 for i in d2 }
    klist = list(set(list(d1.keys())+list(d2.keys())))
    return scipy.spatial.distance.jaccard([px[i] if i in px else 0. for i in klist],[py[i] if i in py else 0. for i in klist])

