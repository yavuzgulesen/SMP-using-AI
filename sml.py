# -*- coding: utf-8 -*-
"""sml.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1VmACDEx1A9VS9U28wZB0MD3wt2OaGQnC
"""

#SML v2
import random

def prefer_m_over_c(w_preference, w, m, c):
    #if m == c:
    #  return False
    for i in range(0, len(w_preference)):
        if (w_preference[w][i] == m):
            return True
        if (w_preference[w][i] == c):
            return False

def randomMatch(n): #n = len(M) or len(W)
  randommatching = []
  poolmen = [i for i in range(n)]
  poolwomen = [j for j in range(n)]
  l = 0
  while l<n:
    i = random.randint(0, n-1)
    i = poolmen[i%len(poolmen)]
    j = random.randint(0, n-1)
    j = poolwomen[i%len(poolwomen)]
    poolmen.remove(i)
    poolwomen.remove(j)
    randommatching.append([i, j])
    l= l+1
  return randommatching

def better_w_partners_of_m(M, m, w):
  better_than_w_for_m = []
  for i in range(0, len(M)):
    if M[m][i] == w:
      break
    else:
      better_than_w_for_m.append(M[m][i])
  return better_than_w_for_m

def better_m_partners_of_w(W, m, w):
  better_than_m_for_w = []
  for i in range(len(W)):
    if W[w][i] == m:
      break
    else:
      better_than_m_for_w.append(W[w][i])
  return better_than_m_for_w

def find_current_marriage_of_w(state, w):
  for j in range(len(state)):
    if [j, w] in state:
      return j

def find_current_marriage_of_m(state, m):
  for i in range(len(state)):
    if [m, i] in state:
      return i

def blockingpairs(M, W, state):
  bp = [] #first index: m; second index: w
  better_women = []
  better_men = []
  for l in range(0, len(M)):
    m = state[l][0]
    w = state[l][1]
    better_women = better_w_partners_of_m(M, m, w)
    for bm in better_women:
      current_man_partner = find_current_marriage_of_w(state, bm)
      if prefer_m_over_c(W, bm, m, current_man_partner) == True:
        bp.append([state[l][0], bm])
  return bp

def remove_bp(bp, tstate):
  m = bp[0]
  w = bp[1]
  c_of_m = find_current_marriage_of_m(tstate, m)

  c_of_w = find_current_marriage_of_w(tstate, w)
  tstate.remove([m, c_of_m])
  tstate.remove([c_of_w, w])
  tstate.append([c_of_w, c_of_m])
  tstate.append([m, w])
  return tstate



M = [[0,2,3,1], [0,3,1,2], [1,0,2,3], [0,1,2,3]]
W = [[1,0,2,3], [1,0,3,2], [0,2,3,1], [2,0,3,1]]
state = randomMatch(len(M))
#state = [[1, 1], [0, 0], [2, 2], [3, 3]]
print("Initial state:", state)
print()

bp = blockingpairs(M, W, state)
print("Blocking pairs of initial state:", bp)
print()
print()

tempstate = state
quit_ = False
step = 0
while len(bp) != 0 and quit_ == False:
  print("STEP", step)
  print("From:", tempstate, "with nbp:", len(bp))
  neighbors = []
  min_neighbors = []
  bps = blockingpairs(M, W, tempstate) #we got the bps of tempstate

  nbps1 = []
  #calculate neighbor states
  for b in range(0, len(bps)): #for each bp of bps of tempstate
    findstates = remove_bp(bps[b],tempstate)
    neighbors.append(findstates)
    #print(findstates)
    nbps1.append(len(blockingpairs(M, W, findstates)))
  print("Neighbors:", neighbors)
  print("Neighbors.nbps:", nbps1)
  #calculate minimum nbp of neighbors
  min_nbp = (len(state)-1) * (len(state)-1) #number of maximum possible blocking pairs
  for n in range(0, len(neighbors)):
    no = len(blockingpairs(M, W, neighbors[n]))
    if no < min_nbp:
      min_nbp = no

  nbps2 = []
  #take those who have minimum nbp
  for n in range(0, len(neighbors)):
    no = len(blockingpairs(M, W, neighbors[n]))
    if no == min_nbp:
      min_neighbors.append(neighbors[n])
      nbps2.append(no)
  print("Min_Neighbors:", min_neighbors)
  print("Min_Neighbors.nbp:", nbps2[0], "and there is/are", len(nbps2), "successors state(s) with this npb value.")
  #if min_nbp <= current_nbp >> then choose a random min_neighbor to go
  
  if min_nbp <= len(bp):
    #choose a random min_neighbor
    random_min_neighbor = min_neighbors[random.randint(0, len(min_neighbors)-1)]
    #go to that state
    tempstate = random_min_neighbor
    bp = blockingpairs(M, W, tempstate)
    print("To:", tempstate, "with npb:", len(bp))
    print("---------------------------------------------------------------------------------")
    print()
  else:
    quit_ = True

if quit_ == True:
  print("Result: Not stable:", tempstate, "with nbp", len(bp))
else:
  print("Result: Stable Matching found as:", tempstate, "with nbp:", len(bp))
  if len(bp) > 0:
    print("BPs:", bp)