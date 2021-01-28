# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 21:55:53 2021

@author: gules
"""
from GentProsser import GentProsser
from Converter import changeStructure
from LocalSearchMethods import eg_cost, F, RemoveBP, NBP_NS, random_match, UND
import random

def ChangeInEgCost(M, man, wom, mrank, wrank, mpref, wpref):
    M_m = M[man]
    M_w = M[len(mrank)+wom]
    cost = None
    M_copy = M[:]
    bp1 = [man, wom]
    bp2 = [M_w, M_m]
    M_copy = RemoveBP(M_copy, bp1, len(mrank))
    M_copy = RemoveBP(M_copy, bp2, len(mrank))
    f_val = F(M_copy, mpref, wpref, mrank, wrank)
    if mrank[M_w][M_m] != len(wrank) and wrank[M_m][M_w] != len(mrank) and f_val == 0:
        cost = 0
        cost += mrank[man][wom]
        cost += wrank[wom][man]    
        
        cost -= mrank[man][M_m]
        cost -= wrank[M_m][man]
        
        cost -= mrank[M_w][wom]
        cost -= wrank[wom][M_w]
        
        cost += mrank[M_w][M_m]
        cost += wrank[M_m][M_w]
    return cost

def LTIU2(mpref, wpref):
    n1 = len(mpref)
    n2 = len(wpref)
    mrank, wrank = changeStructure(mpref, wpref, n1, n2)
    arraysize = (n1 + n2)
    M = [-1]*arraysize
    M = random_match(M, mrank, n1, n2)
    Fprev = F(M, mpref, wpref, mrank, wrank)
    Fbest = Fprev
    stableFound = False
    NSbest = 2*n1*n2 
    Mbest = M
    steps = 10000
    print("Random Restart (LTIU)")
    while steps:
        nbp, ns = NBP_NS(M, mpref, wpref, mrank, wrank)
        #nbp = NBP(M, mrank, wrank)
        #ns = NS(M)
        f = nbp + ns
        if stableFound == False and f < Fbest:
            Fbest = f
            Mbest = M
        #If a perfect matching found
        if f == 0: 
            Mbest = M
            Fbest = 0 #f
            break
        #If a stable (but not perfect) matching found
        if nbp == 0:  
            stableFound = True
            #Is it the best Stable matching among stable matchings found so far?
            if ns < NSbest: 
                Mbest = M
                NSbest = ns
                Fbest = f   # = ns
            M = random_match(M, mrank, n1, n2)  
        #If unstable
        else:
            #Find neighbors
            undominated_bps = UND(M, mrank, wrank, steps%2)
            neis = []
            for un in undominated_bps:
                copyM = M[:]
                copyM = RemoveBP(copyM, un, n1)
                neis.append(copyM)
            random_walk = True if random.random() <= 0.2 else False
            if random_walk:
                M = neis[random.randint(0, len(neis)-1)] #Choose a random neighbor
            else:
                #Choose a neighbor with the minimum evaluation value
                evaluations = [F(nei, mpref, wpref, mrank, wrank) for nei in neis]
                min_eval = min(evaluations)
                if min_eval <= f:  #if there is an improvement
                    indices = [i for i, v in enumerate(evaluations) if v == min_eval]
                    M = neis[random.choice(indices)]
                else:   #no improvement, choose a random neighbor
                    M  = neis[random.randint(0, len(neis)-1)]
        steps -= 1
    nbp, ns = NBP_NS(Mbest, mpref, wpref, mrank, wrank)    
    f = ns + nbp
    return Mbest, f

n1 = 20
n2 = n1
mpref, wpref = GentProsser(n1, n2, 0.2, 0.5)
mrank, wrank = changeStructure(mpref, wpref, n1, n2)


#Initialize M
M, f = LTIU2(mpref, wpref)
iters = 1000
Mbest = M
best_cost = 2*n1*n2
while iters:
    f = F(M, mpref, wpref, mrank, wrank)
    if f != 0:
        M, f = LTIU2(mpref, wpref)
    else:
        cost = eg_cost(M, mrank, wrank)
        if cost == 0:
            print(M)    #return M
            print(cost)
        else:
            if cost < best_cost:
                Mbest = M
                best_cost = cost
            #Choose a random man
            random_man = random.randint(0, len(mpref)-1)
            women = []
            for w in range(len(mrank[random_man])):
                if mrank[random_man][w] != n2:
                    women.append(w)
            women.remove(M[random_man])
            changes = [ChangeInEgCost(M, random_man, wom, mrank, wrank, mpref, wpref) for wom in women]
            final_women_list = []
            for wo in range(len(women)):
                if changes[wo] != None:
                    final_women_list.append(women[wo])
            changes = [c for c in changes if c != None]
            if len(changes) != 0:
                min_change = min(changes)
                if min_change < 0:
                    ind = [i for i, v in enumerate(changes) if v == min_change]
                    woman = final_women_list[random.choice(ind)]
                    
                    M_m = M[random_man]
                    M_w = M[n1 + woman]
                    
                    M[random_man] = woman
                    M[n1 + woman] = random_man
                    M[M_m+n1] = M_w
                    M[M_w] = M_m
            
                
    iters -= 1

print(Mbest)
print("cost:", best_cost)