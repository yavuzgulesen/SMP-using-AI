# -*- coding: utf-8 -*-
"""
Created on Nov 9, 2020

@author: YavuzGulesen
"""
import random
import sys
import time
from Converter import changeStructure


def printSolution(M, n):
    print("m", "\t", "w")
    for i in range(n):
        if(M[i] != -1):
            print(i+1,"-", M[i]+1)
    
def random_match(M, mrank, n):
    #Before calling this,
    #M should be initialized to be [-1]*2*n
    women = [j for j in range(n)]
    for m in range(n):
        #print("men:", m)
        #print("women:", women)
        random_index = random.randint(0, len(women)-1)
        #print("random_index:", random_index)
        w = women[random_index]#women index
        #print("w:", w)
        #if acceptable
        if mrank[m][w] != n:
            #then match them
            M[m] = w
            M[n+w] = m
            #print("M:", M)
            women.remove(w)
        #print("-----------------------------------------------")
    return(M)

def prefers(M, i, j, rank, n, gender):
    # This function checks if i STRICTLY prefers j over his/her current partner M(i)
    # M(i) is denoted by M_i
    k = i
    if rank[i][j] == n: #acceptability check
        return False #because i does not accept j
    else:   #acceptable   
        if gender == 0: #then i is a woman
            i = i + n #len(rank) = n

        M_i = M[i] #his/her partner
        if M_i == -1:   #if s/he is single, then True
            return True
        else:   #if not..
            #then check if i STRICTLY prefers j over M_i
            if rank[k][j] < rank[k][M_i]:
                return True
            else:
                return False
    
def bp(M, m, w, mrank, wrank, n):
    # This function checks if (m, w) is a blocking pair of M
    if prefers(M, m, w, mrank, n, 1) and prefers(M, w, m, wrank, n, 0):
        return True
    return False

def ns(M):
    singles = 0
    for i in M:
        if i == -1:
            singles += 1
    return singles

def nbp(M, mrank, wrank, n):
    no = 0
    for m in range(n):
        for w in range(n):
            if bp(M, m, w, mrank, wrank, n):
                no += 1
    return no

def F(M, mrank, wrank, n):
    return ns(M) + nbp(M, mrank, wrank, n)

def M_has_no_blocking_pairs(M, mrank, wrank, n):
    for m in range(n):
        for w in range(n):
            if bp(M, m, w, mrank, wrank, n):
                return False
    return True

def man_that_generates_max_bp(M, mrank, wrank, n):
    max_men = [0]*n    
    m = 0
    while m < n:
        for w in range(n):
            if bp(M, m, w, mrank, wrank, n):
                max_men[m]+=1
        m += 1
    max_val = max(max_men)
    best_m = []
    for i in range(n):
        if max_men[i] == max_val:
            best_m.append(i)
    return best_m[random.randint(0, len(best_m)-1)]
    
def random_best_woman_for_m(mpref, m):
    w = mpref[m][0][random.randint(0, len(mpref[m][0])-1)]
    return w
    
def RemoveBP(M, m, w, n):
    #Find their partners:
    M_m = M[m]
    M_w = M[int(w)+int(n)]
    
    
    #Remove the blocking pair by matching them
    M[m] = w
    M[n+w] = m
    #-----------------------------------------
    #Release the partners:
    if M_m != -1: #if man had a partner
        M[n+M_m] = -1 # release her
        
    if M_w != -1: #if woman had a partner
        M[M_w] = -1 # release him
    #-----------------------------------------
    return M
    
            
def findbps(M, mrank, wrank, n):
    bps = []
    for m in range(n):
        Mm = M[m]
        for w in range(n):
            Mw = M[w + n]
            if Mm == -1:
                if Mw == -1:
                    #if they accept each other:
                    if mrank[m][w] != n and wrank[w][m] != n:
                        bps.append([m, w])
                else:
                    #if m accepts w and  w prefers m to Mw
                    if mrank[m][w] != n and wrank[w][Mw] > wrank[w][m]:
                        bps.append([m, w])
            else:
                if Mw == -1:
                    #if m prefers w to Mm  and  w accepts m
                    if mrank[m][w] < mrank[m][Mm] and wrank[w][m] != n:
                        bps.append([m, w])
                else:
                    #if m prefers w to Mm  and  w prefers m to Mw
                    if mrank[m][w] < mrank[m][Mm] and wrank[w][Mw] > wrank[w][m]:
                        bps.append([m, w])
    return bps

def max_err_m(Y):
    wlist = []
    for y in Y:
        if y[1] != -1:
            wlist.append(y[1])
    return wlist

def best_w(my, wlist2, mrank):
    rank = 9999
    rt = wlist2[0]
    for wy in wlist2:
        if mrank[my][wy] < rank:
            rank = mrank[my][wy]
            rt = wy
    return rt

def nobpsofmex(bps, n):
    arr = [0] * n
    for bp in bps:
        if bp[0] != -1:
            arr[bp[0]] += 1
    
    max_m = max(arr)
    ind = 0
    while ind < len(arr):
        if max_m == arr[ind]:
            break
        ind += 1
    
    ret_bp = [bp for bp in bps if bp[0] == ind]
    return ret_bp, ind


def ns(a):
    x = 0
    for i in range(len(a)):
        if a[i] == -1:
            x+=1
    return x

def GenerateRankList(preferencesInLine):
    # it will get preferences in input file and convert it into a ranked list so that we can put the ranks in the preference list
    result = []

    while len(preferencesInLine) != 0:
        element = preferencesInLine[preferencesInLine.find("(") + 1: preferencesInLine.find(")")]
        # typecasting the preference ID to an int
        element = element.split(" ")
        for i in range(len(element)):
            element[i] = int(element[i])-1
            
        result.append(element)

        preferencesInLine = preferencesInLine[preferencesInLine.find(")") + 1:]
    return result



import os
with os.scandir('../INPUTS/') as entries:
    for entry in entries:   
        filename = '../INPUTS/' + entry.name
        f = open(filename, "r")  # Read the input file
        lines = f.readlines()
        f.close()
        numberOfMan = int(lines[1])
        numberOfWoman = int(lines[2])
        n = numberOfMan
        mpref = [None] * numberOfMan  # np.empty(numberOfMan, dtype=object)
        wpref = [None] * numberOfWoman  # np.empty(numberOfWoman, dtype=object)
        for i in range(3, 3 + numberOfMan):
            line = lines[i]  # line = "ID Preferences"
            line = line.replace("\n", "")  # getting rid of \n character at the end of the line
            line = line.rstrip()  # getting rid of whitepace at the end of the line
            line = line.split(" ", 1)  # line = [ID, Preferences]
            id = int(line[0])  # this is the id of man or woman
            preferenceList = GenerateRankList(line[1])  # line[1] is the rest of the line and it has the form "(x y z)" or "(x) (y) (z)" or "(x y) (z)" ...
            # rankList will have a value ['x y z'] or ['x', 'y', 'z'] or ['x y', 'z']. Each of this ids in indices of this list will be their rank in preference list
            mpref[id - 1] = preferenceList
        
        for i in range(3 + numberOfMan, 3 + numberOfMan + numberOfWoman):
            line = lines[i]  # line = "ID Preferences"
            line = line.replace("\n", "")  # getting rid of \n character at the end of the line
            line = line.rstrip()  # getting rid of whitepace at the end of the line
            line = line.split(" ", 1)  # line = [ID, Preferences]
            id = int(line[0])  # this is the id of man or woman
        
            preferenceList = GenerateRankList(line[1])  # line[1] is the rest of the line and it has the form "(x y z)" or "(x) (y) (z)" or "(x y) (z)" ...
            # rankList will have a value ['x y z'] or ['x', 'y', 'z'] or ['x y', 'z']. Each of this ids in indices of this list will be their rank in preference list
        
            wpref[id - 1] = preferenceList        
    
        #print(mpref)
        #print(wpref)
        mrank, wrank = changeStructure(mpref, wpref, n, n)
        arraysize = 2*n
        
        M = [-1]*arraysize
        M = random_match(M, mrank, n)
        
        Mbest = M    
        
        iters = 6000
        iterstart = iters
        start = time.time()
        while iters and time.time()-start < 2000:
            if ns(Mbest) == 0:
                break
            X = findbps(M, mrank, wrank, n)
            if len(X) == 0:
                #M is stable
                #random restart
                if ns(M) < ns(Mbest):
                    Mbest = M
                M = [-1]*arraysize
                M = random_match(M, mrank, n)
            else:
                m = man_that_generates_max_bp(M, mrank, wrank, n)
                randWalk = random.random()
                if randWalk <= 0.2:
                    pIndex = random.randint(0, len(mpref[m])-1)
                    wIndex = random.randint(0, len(mpref[m][pIndex])-1)
                    w = mpref[m][pIndex][wIndex]
                else:
                    w = random_best_woman_for_m(mpref, m)
                M = RemoveBP(M, m, w, n)
            iters -= 1
        
        runtime = round(time.time()-start,5)
        ns_ = ns(Mbest)
        nbp_ =nbp(Mbest, mrank, wrank, n)
        steptotal = iterstart - iters
        #Write to file
        out = "../OUT_LCV/"+"output-"+filename[16:len(filename)-4]+"_LCV.txt"
        f = open(out, "a")
        f.write("Run time: "+ str(runtime) + "\n")
        f.write("Number of steps: "+ str(steptotal) + "\n")
        f.write("Number of singles: "+ str(ns_) + "\n")
        f.write("Number of blocking pairs: "+ str(nbp_) + "\n")
        f.write("Solution: \n")
        f.write("m" + "   "+ "w" + "\n")
        for i in range(n):
            if(M[i] != -1):
                f.write(str(i+1) + " - " + str(M[i]+1) + "\n")
        f.close()
        
        summary = open("summary.txt", "a")
        summary.write(filename[31:33] + "," +filename[37:40] + "," + filename[45:48] + "," + str(runtime)+","+str(steptotal)+","+str(ns_)+","+str(nbp_)+"\n")
    summary.close()
    sys.exit()
