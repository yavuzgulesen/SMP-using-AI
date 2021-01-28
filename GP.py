#Instance generator mentioned in Gent & Prosser's paper
#Yavuz, 23/5/2020

#Edited on 6/6/2020;
#Number of men and women can be different now

import numpy as np
import random

def CreateFile(w_pref, m_pref):
  f = open('input-smti-maxcard-s-50--i-0.9pc-t-0.9pc--1.txt', 'w')
  #line1: dummy; line 2 & 3: # of men and women
  f.write(str(0)+"\n"+str(n1)+"\n"+str(n2)+"\n")
  #--------------------------------------------
  #Writing every men's corresponding preference list:
  for i in range(len(m_pref)):
    f.write(str(i+1) + " ")
    for j in range(len(m_pref[i])):
      if len(m_pref[i][j]) > 1:
        f.write("(")
        k=0
        while k < (len(m_pref[i][j])-1):
          f.write(str(m_pref[i][j][k]+1)+" ")
          k+=1
        f.write(str(m_pref[i][j][k]+1)+")"+" ")
      else:
        f.write("("+str(m_pref[i][j][0]+1)+")"+ " ")
    f.write("\n")
  #----------------------------------------------------
  #Writing every women's corresponding preference list:
  for i in range(len(w_pref)):
    f.write(str(i+1) + " ")
    for j in range(len(w_pref[i])):
      if len(w_pref[i][j]) > 1:
        f.write("(")
        k=0
        while k < (len(w_pref[i][j])-1):
          f.write(str(w_pref[i][j][k]+1)+" ")
          k+=1
        f.write(str(w_pref[i][j][k]+1)+")"+" ")
      else:
        f.write("("+str(w_pref[i][j][0]+1)+")"+ " ")
    f.write("\n")
    #---------------------------------------------------
  f.close()


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
      temp=[]
    m_pref_list2.append(m_pref_list)

  w_pref_list2 = []
  for i in range(len(w_pref)):
    w_pref_list=[]
    for j in range(len(w_pref[i])):
      temp = []
      temp.append(w_pref[i][j])
      w_pref_list.append(temp)
      temp=[]
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
  #---------------------------------------------
  print("final m_pref:", m_pref_list2)
  print("final w_pref:", w_pref_list2)
  return m_pref_list2, w_pref_list2



def GentProsser(n1, n2, p1, p2):
  m_pref, w_pref = GenerateRandomMatching(n1, n2, p1, p2) #Step 1 & 2 is done with this function

  #Step 3 : Everyone has to have at least someone in his/her preference list
  while CheckValid(m_pref, w_pref) == False:
     m_pref, w_pref = GenerateRandomMatching(n1, n2, p1, p2)  
    

  #-------------------------------------------------------------------------
  #print("m_pref:", m_pref)

  m_pref, w_pref = AddTies(p2, m_pref, w_pref) #Step 4 is done with this function
  return m_pref, w_pref
  #file = open('input.txt', 'w')
  
n1 = int(input("Number of men:"))
n2 = int(input("Number of women:"))
p1 = float(input("p1:"))
p2= float(input("p2:"))
m_pref, w_pref = GentProsser(n1, n2, p1, p2)

#Write to an input file
CreateFile(w_pref, m_pref)
