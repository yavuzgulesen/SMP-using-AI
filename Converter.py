# -*- coding: utf-8 -*-
"""
Created on Fri Nov 6 19:19:06 2020

@author: YavuzGulesen
"""

import random

def rank_finder(list_, ind, n):
  i=0
  while i < len(list_):
    #print(list_[i])
    if ind in list_[i]:
      return i
    i += 1
  return n


def changeStructure(mpref, wpref, n1, n2):
    men_rank_list = []
    for i in mpref:
      #every men's list one by one in i
      rank_li = []
      for j in range(0, n2):
        rank_li.append(rank_finder(i, j, n2))
      men_rank_list.append(rank_li)
      
    women_rank_list = [] 
    for k in wpref:
      #every men's list one by one in i
      rank_lis = []
      for l in range(0, n1):
        rank_lis.append(rank_finder(k, l, n1))
      women_rank_list.append(rank_lis)
      
    return men_rank_list, women_rank_list

def randomMatch(m, w): #m = len(M) w = len(W)
  randommatching = []
  poolmen = [i for i in range(m)]
  poolwomen = [j for j in range(w)]

  min = m
  max = w
  if w < m:
    min = w
    max = m
  
  l = 0
  while l<min:
    i = random.randint(0, min-1)
    i = poolmen[i%len(poolmen)]
    j = random.randint(0, m-1)
    j = poolwomen[i%len(poolwomen)]
    poolmen.remove(i)
    poolwomen.remove(j)
    randommatching.append([i, j])
    l= l+1
  k = 0
  while k < max-l:
    if max == m:
      randommatching.append([poolmen[k], -1])
    else:
      randommatching.append([-1, poolwomen[k]])
    k= k+1
  return randommatching