"""
Created on Fri Jan 22 04:55:53 2021

@author: YavuzGulesen
"""
from GentProsser import GentProsser
from Converter import changeStructure
from LocalSearchMethods import se_cost, eg_cost, F, NBP_NS, random_match, UND, RemoveBP
import random
import matplotlib.pyplot as plt
import time

def BreakMarriageSMTI(M, mrank, wrank, mpref, wpref):
    perfect_ones = []
    for m in range(len(mrank)):
        possible_partners = [i for i in range(len(mrank[m])) if mrank[m][i] != len(wrank)]
        for wom in possible_partners:
            copyM = M[:]
            M_m = M[m]
            M_w = M[len(mrank)+wom]
            
            copyM[m] = wom
            copyM[wom + len(mrank)] = m
            copyM[len(mrank) + M_m] = M_w
            copyM[M_w] = M_m
            if F(copyM, mpref, wpref, mrank, wrank) == 0:
                perfect_ones.append(copyM)
    return perfect_ones

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
    steps = 5000
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

def Egalitarian_Sexequal_3(mpref, wpref, algo):
    mrank, wrank = changeStructure(mpref, wpref, n1, n2)
 
    #Initialize M
    M, f = LTIU2(mpref, wpref)
    Mbest = M
    bestCost = 2*n1*n2 
    iters = 500
    clist = []
    start = time.time()
    while iters and time.time()-start < 2000:
        f = F(M, mpref, wpref, mrank, wrank)
        if f != 0:
            M, f = LTIU2(mpref, wpref)
        else:
            cost = eg_cost(M, mrank, wrank) if algo == "eg" else se_cost(M, mrank, wrank)
            clist.append(cost)
            if cost < bestCost:
                bestCost = cost
                Mbest = M
            if cost == 0:
                return M, cost
            else:
                neighbors = BreakMarriageSMTI(M, mrank, wrank, mpref, wpref)
                print("neigbors")
                for ne in neighbors:
                    print(ne)
                randwalk = True if random.random() <= 0.2 else False
                if randwalk:
                    M = neighbors[random.randint(0, len(neighbors)-1)]
                else:  
                    costs = [eg_cost(nei, mrank, wrank) for nei in neighbors] if algo == "eg" else [se_cost(nei, mrank, wrank) for nei in neighbors]
                    min_cost = min(costs)
                    if min_cost < cost:
                        indices = [i for i, v in enumerate(costs) if v == min_cost]
                        M = neighbors[random.choice(indices)]
                    else:
                        M = neighbors[random.randint(0, len(neighbors)-1)]
        iters -= 1
    plt.plot(clist)
    plt.show()
    return_cost = eg_cost(Mbest, mrank, wrank) if algo=="eg" else se_cost(Mbest,mrank, wrank)
    return Mbest, return_cost

n1 = 20
n2 = n1
p1 = round(random.random(),1)
p2 = round(random.random(),1)
mpref, wpref = GentProsser(n1, n2, p1, p2)
M, cost_val = Egalitarian_Sexequal_3(mpref, wpref, "se")
print("Returned matching:")
print(M)
print("cost:",cost_val)