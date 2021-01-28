# -*- coding: utf-8 -*-
"""
Created on May 23, 2020

@author: Yavuz Güleşen
"""

import numpy as np
import random

def GenerateRandomMatching(n1, n2, p1, p2):
  #Step 1 : Random Matching of size n
  m_pref = {}
  w_pref = {}
  for i in range(0, n2):
    w_pref[i] = np.random.permutation(n1).tolist()  
  for i in range(0, n1):
    m_pref[i] = np.random.permutation(n2).tolist()  
  #----------------------------------

  #Step 2 : Adding Incompleteness
  for i in range(0, n1):
    for j in range(0, n2):
      if p1 >= random.random():
        m_pref[i].remove(j)
        w_pref[j].remove(i)
  #------------------------------
  #print(m_pref)
  #print(w_pref)
  return m_pref, w_pref
#--------------------------------------------


#Step 3 : Check if the initial state is valid
def CheckValid(m_pref, w_pref):
  for i in range(0, len(m_pref)):
    if len(m_pref[i]) == 0:
      return False

  for i in range(0, len(w_pref)):
    if len(w_pref[i]) == 0:
      return False

  return True
#-------------------------------------------


#Step 4 : Adding Ties
def AddTies(p2, m_pref, w_pref):
  #Changing the format in order to store ties
  m_pref_list2 = []
  for i in range(len(m_pref)):
    m_pref_list=[]
    for j in range(len(m_pref[i])):
      temp = []
      temp.append(m_pref[i][j])
      m_pref_list.append(temp)
    m_pref_list2.append(m_pref_list)

  w_pref_list2 = []
  for i in range(len(w_pref)):
    w_pref_list=[]
    for j in range(len(w_pref[i])):
      temp = []
      temp.append(w_pref[i][j])
      w_pref_list.append(temp)
    w_pref_list2.append(w_pref_list)
  #------------------------------------------
  
  #Step 4 : Adding Ties for each man and woman
  for i in range(0, len(m_pref_list2)):
    j=1
    while j < len(m_pref_list2[i]):
      if random.random() <= p2 and j < len(m_pref_list2[i]):
        m_pref_list2[i][j-1].append(m_pref_list2[i][j][0])
        del m_pref_list2[i][j]
        j -= 1
      j += 1
  for i in range(0, len(w_pref_list2)):
    while j < len(w_pref_list2[i]):
      if random.random() <= p2 and j < len(w_pref_list2[i]):
        w_pref_list2[i][j-1].append(w_pref_list2[i][j][0])
        del w_pref_list2[i][j]
        j -= 1
      j += 1
      
  return m_pref_list2, w_pref_list2



def GentProsser(n1, n2, p1, p2):
  m_pref, w_pref = GenerateRandomMatching(n1, n2, p1, p2) #Step 1 & 2 is done with this function

  #Step 3 : Everyone has to have at least someone in his/her preference list
  while CheckValid(m_pref, w_pref) == False:
     m_pref, w_pref = GenerateRandomMatching(n1, n2, p1, p2)  
  
  m_pref, w_pref = AddTies(p2, m_pref, w_pref) #Step 4 is done with this function
  return m_pref, w_pref