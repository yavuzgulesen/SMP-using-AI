# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 20:17:36 2020

@author: YavuzGulesen
"""
import random
from Converter import changeStructure
from LocalSearchMethods import random_match, F, RemoveBP, se_cost, eg_cost, UND, NBP_NS

def Egalitarian_SexEqual(mpref, wpref, steps, algo):
    n1 = len(mpref)
    n2 = len(wpref)
    mrank, wrank = changeStructure(mpref, wpref, n1, n2)
    arraysize = (n1 + n2)
    M = [-1]*arraysize
    M = random_match(M, mrank, n1, n2)
    
    stableFound = False
    Mbest = M
    begin = steps
    
    fs_return = []
    costs_return = []
    
    perfectFound = False
    stableFound = False
    
    while steps:
        print("| step:", begin-steps)
        nbp, ns = NBP_NS(M, mpref, wpref, mrank, wrank)
        cost_val = se_cost(M, mrank, wrank) if algo == "se" else eg_cost(M, mrank, wrank)
        f = nbp + ns
        #print("| f:", f)
        fs_return.append(f)
        costs_return.append(cost_val)
        if f == 0 and cost_val == 0:
            Mbest = M
            break
        
        if nbp == 0:
            if ns == 0:
                if perfectFound == True:
                    compare_cost = se_cost(Mbest, mrank,wrank) if algo == "se" else eg_cost(Mbest, mrank, wrank)
                    if compare_cost < cost_val:
                        Mbest = M
                else:
                    Mbest = M
                    perfectFound = True
            else:
                if perfectFound == False:
                    if stableFound == True:
                        if ns < F(Mbest, mpref, wpref, mrank, wrank):
                            Mbest = M
                    else:
                        Mbest = M
                stableFound = True
            M = random_match(M, mrank, n1, n2)
        else:           
            undominated_bps = UND(M, mrank, wrank, steps%2)
            #print(undominated_bps)
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
                f_evals = [F(nei, mpref, wpref, mrank, wrank) for nei in neis]
                min_eval = min(f_evals)
                indices = [i for i, v in enumerate(f_evals) if v == min_eval]
                cost_evals = [se_cost(nei, mrank, wrank) for nei in neis] if algo == "se" else [eg_cost(nei, mrank, wrank) for nei in neis]
                min_cost = min(cost_evals)
                compare_cost2 = se_cost(M, mrank, wrank) if algo == "se" else eg_cost(M, mrank, wrank)
                indices2 = [i for i, v in enumerate(cost_evals) if v == min_cost]
                if min_eval < f:  #if there is an improvement
                    if min_cost <= compare_cost2:  
                        indices3 = []
                        for i in indices:
                            for j in indices2:
                                if i == j:
                                    indices3.append(i)
                        if len(indices3) != 0:
                            M = neis[random.choice(indices3)]
                        else:
                            M = neis[random.choice(indices)]
                    else:
                        #M = neis[random.randint(0, len(neis)-1)]
                        M = neis[random.choice(indices2)]
                else:
                    M = neis[random.choice(indices2)]
                    #M = neis[random.randint(0, len(neis)-1)]
        steps -= 1
        
    nbp_val, ns_val = NBP_NS(Mbest, mpref, wpref, mrank, wrank)
    f_val = nbp_val + ns_val
    cost_val = se_cost(M, mrank, wrank) if algo == "se" else eg_cost(M, mrank, wrank)
    return f_val, cost_val, nbp_val, ns_val, fs_return, costs_return, begin-steps