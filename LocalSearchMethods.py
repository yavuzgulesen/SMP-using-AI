# -*- coding: utf-8 -*-
"""
Created on Thu Oct 8 16:02:23 2020

@author: gules
"""
import random
def se_cost(M, mrank, wrank):
    cost1 = 0
    cost2 = 0
    n1 = len(mrank)
    n2 = len(wrank)
    for i in range(n1):
        if M[i] != -1:
            cost1 += mrank[i][M[i]]
    for j in range(n2):
        if M[j+n1] != -1:
            cost2 += wrank[j][M[j+n1]]            
    return cost2-cost1 if cost2 >= cost1 else cost1-cost2
#------------------------------------------------------------------------------
def eg_cost(M, mrank, wrank):
    cost = 0
    n1 = len(mrank)
    n2 = len(wrank)
    for i in range(n1):
        if M[i] != -1:
            cost += mrank[i][M[i]]
    for j in range(n2):
        if M[j+n1] != -1:
            cost += wrank[j][M[j+n1]]
    return cost
#------------------------------------------------------------------------------
def prefers(M, i, j, rank, n1, n2, gender):
    #Check is i STRICTLY prefers j over his/her current partner M(i)
    #M(i) is denoted by M_i
    
    #ACCEPTABILITY CHECK-------------------------------------------------------
    n = n1 if gender == 0 else n2 #if gender = woman
    #n = n1 bec. we firstly check whether rank[woman][man] = n1
                #else, n = n2 since we check whether rank[man][woman] = n2
                
    if rank[i][j] ==  n:
        return False #because i does not even accept j      
    #--------------------------------------------------------------------------
    else:  #Then i accept j
        #if gender = woman, then her partner is M[n1 + i]; else, M[i])
        M_i = M[i] if gender == 1 else M[i+n1]
        #IS SINGLE? CHECK------------------------------------------------------
        if M_i == -1:   #if s/he is single, then True since j is acceptable
            return True
        #----------------------------------------------------------------------
        else:   #S/he has a partner
            #then check if i STRICTLY prefers j over M_i
            if rank[i][j] < rank[i][M_i]:
                return True
            else:
                return False
#------------------------------------------------------------------------------
def isBP(M, m, w, mrank, wrank):
    n1 = len(mrank)
    n2 = len(wrank)
    # This function checks if (m, w) is a blocking pair of M
    if prefers(M, m, w, mrank, n1, n2, 1) and prefers(M, w, m, wrank, n1, n2, 0):
        return True
    return False
#------------------------------------------------------------------------------
def NBP_NS(M, mpref, wpref, mrank, wrank):
    n1 = len(mpref)
    n2 = len(wpref)
    wom_in_a_bp = []
    men_in_a_bp = []
    nbp_counter = 0
    for man in range(len(mpref)):
        for pref_i in mpref[man]:
            for woman in pref_i:
                if prefers(M, man, woman, mrank, n1, n2, 1) and prefers(M, woman, man, wrank, n1, n2, 0):
                    nbp_counter += 1
    ns_counter = 0
    for i in range(n1):
        if M[i] == -1 and i not in men_in_a_bp:
            ns_counter += 1
    for j in range(n2):
        if M[n1+j] == -1 and j not in wom_in_a_bp:
            ns_counter += 1     
    return nbp_counter, ns_counter
#------------------------------------------------------------------------------
def F(M, mpref, wpref, mrank, wrank):
    nbp, ns = NBP_NS(M, mpref, wpref, mrank, wrank)
    return nbp + ns
#------------------------------------------------------------------------------
def random_match(M, mrank, n1, n2): #for the first matching and random restart
    M = [-1]*(n1+n2)
    women = [j for j in range(n2)]
    for m in range(n1):
        random_index = random.randint(0, len(women)-1)
        w = women[random_index]
        if mrank[m][w] != n2:    #if acceptable, match them
            M[m] = w
            M[n1+w] = m
            women.remove(w)
    return(M)
#------------------------------------------------------------------------------
def RemoveBP(M, bp, n1):
    m = bp[0]
    w = bp[1]
    m_partner = M[m]
    w_partner = M[n1+w]
    
    #Match them
    M[m] = w
    M[n1+w] = m
    
    #What about their previous partners?
    if m_partner != -1:
        M[n1+m_partner] = -1    #Make them single if they were not -1
    if w_partner != -1:
        M[w_partner] = -1
    return M
#------------------------------------------------------------------------------
def UND_BP_MFWS(M, mpref,wpref, mrank, wrank):
    #Undominated blocking pairs (Men First Women Second)
    n1 = len(mpref)
    n2 = len(wpref)
    
    und_bp_list = [] 
    for man_i in range(len(mpref)): #her bir adam için
        und_found = False
        
        for pref_i in mpref[man_i]:  #o adamın listesindeki her kadın için
            #print(pref_i)
            if und_found:
                break
            for woman in pref_i:
                if prefers(M, man_i, woman, mrank, n1, n2, 1) and prefers(M, woman, man_i, wrank, n1, n2, 0):
                    #hem blocking pair hem de ranki en düşük olanı yani undominatedları tutacak
                    #bulduğunda ranki daha yüksek olan için artık arama yapmayacak
                    und_bp_list.append([man_i, woman])
                    und_found = True
    #print("from men p.o.w.:", und_bp_list)
    final = []
    for w in range(len(wpref)):
        min_rank = len(mpref)
        for u in und_bp_list:
            if u[1] == w:
                #print(wrank[w][u[0]], min_rank)
                if wrank[w][u[0]] < min_rank:
                    min_rank = wrank[w][u[0]]
                elif wrank[w][u[0]] > min_rank:
                    und_bp_list.remove(u)
                    
        for u in und_bp_list:
            if w == u[1]  and wrank[w][u[0]] == min_rank:
                final.append(u)
                und_bp_list.remove(u)
    #print("after women p.o.w.:", final)
    return final
#------------------------------------------------------------------------------
def UND_BP_WFMS(M, mpref, wpref, mrank, wrank):
    #Undominated blocking pairs (Women First Men Second)
    n1 = len(mpref)
    n2 = len(wpref)
    
    und_bp_list = [] 
    for wom_i in range(len(wpref)): #her bir adam için
        und_found = False
        
        for pref_i in wpref[wom_i]:  #o adamın listesindeki her kadın için
            #print(pref_i)
            if und_found:
                break
            for man in pref_i:
                if prefers(M, wom_i, man, wrank, n1, n2, 0) and prefers(M, man, wom_i, mrank, n1, n2, 1):
                    #hem blocking pair hem de ranki en düşük olanı yani undominatedları tutacak
                    #bulduğunda ranki daha yüksek olan için artık arama yapmayacak
                    und_bp_list.append([man, wom_i])
                    und_found = True
    #print("from women p.o.w.:", und_bp_list)

    final = []
    for m in range(len(mpref)):
        min_rank = len(wpref)
        for u in und_bp_list:
            if u[0] == m:
                if mrank[m][u[1]] < min_rank:
                    #print("True")
                    min_rank = mrank[m][u[1]]
                elif mrank[m][u[1]] > min_rank:
                    #print("False")
                    und_bp_list.remove(u)
                    
        for u in und_bp_list:
            if m == u[0] and mrank[m][u[1]] == min_rank:
                final.append(u)
                und_bp_list.remove(u)
    #print("after men p.o.w.:", final)

    return final
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
def UND_BP_WFMS2(M, mpref, wpref, mrank, wrank):
    #Undominated blocking pairs (Women First Men Second)
    wom_in_und_bp = []
    men_in_und_bp = []
    n1 = len(mpref)
    n2 = len(wpref)
    
    und_bp_list = [] 
    for wom_i in range(len(wpref)): #her bir adam için
        und_found = False
        
        for pref_i in wpref[wom_i]:  #o adamın listesindeki her kadın için
            #print(pref_i)
            if und_found:
                break
            for man in pref_i:
                if prefers(M, wom_i, man, wrank, n1, n2, 0) and prefers(M, man, wom_i, mrank, n1, n2, 1):
                    #hem blocking pair hem de ranki en düşük olanı yani undominatedları tutacak
                    #bulduğunda ranki daha yüksek olan için artık arama yapmayacak
                    und_bp_list.append([man, wom_i])
                    und_found = True
    #print("from women p.o.w.:", und_bp_list)

    final = []
    for m in range(len(mpref)):
        min_rank = len(wpref)
        for u in und_bp_list:
            if u[0] == m:
                if mrank[m][u[1]] < min_rank:
                    #print("True")
                    min_rank = mrank[m][u[1]]
                elif mrank[m][u[1]] > min_rank:
                    #print("False")
                    und_bp_list.remove(u)
                    
        for u in und_bp_list:
            if m == u[0] and mrank[m][u[1]] == min_rank:
                final.append(u)
                men_in_und_bp.append(u[0])
                wom_in_und_bp.append(u[1])
                und_bp_list.remove(u)
    #print("after men p.o.w.:", final)
    ns_counter = 0
    for i in range(n1):
        if M[i] == -1 and i not in men_in_und_bp:
            ns_counter += 1
    for j in range(n2):
        if M[n1+j] == -1 and j not in wom_in_und_bp:
            ns_counter += 1     

    return len(final), ns_counter
#------------------------------------------------------------------------------
def UND_BP_MFWS2(M, mpref,wpref, mrank, wrank):
    #Undominated blocking pairs (Men First Women Second)
    n1 = len(mpref)
    n2 = len(wpref)
    wom_in_und_bp = []
    men_in_und_bp = []
    und_bp_list = [] 
    for man_i in range(len(mpref)): #her bir adam için
        und_found = False
        
        for pref_i in mpref[man_i]:  #o adamın listesindeki her kadın için
            #print(pref_i)
            if und_found:
                break
            for woman in pref_i:
                if prefers(M, man_i, woman, mrank, n1, n2, 1) and prefers(M, woman, man_i, wrank, n1, n2, 0):
                    #hem blocking pair hem de ranki en düşük olanı yani undominatedları tutacak
                    #bulduğunda ranki daha yüksek olan için artık arama yapmayacak
                    und_bp_list.append([man_i, woman])
                    und_found = True
    #print("from men p.o.w.:", und_bp_list)
    final = []
    for w in range(len(wpref)):
        min_rank = len(mpref)
        for u in und_bp_list:
            if u[1] == w:
                #print(wrank[w][u[0]], min_rank)
                if wrank[w][u[0]] < min_rank:
                    min_rank = wrank[w][u[0]]
                elif wrank[w][u[0]] > min_rank:
                    und_bp_list.remove(u)
                    
        for u in und_bp_list:
            if w == u[1]  and wrank[w][u[0]] == min_rank:
                final.append(u)
                men_in_und_bp.append(u[0])
                wom_in_und_bp.append(u[1])
                und_bp_list.remove(u)
        
    ns_counter = 0
    for i in range(n1):
        if M[i] == -1 and i not in men_in_und_bp:
            ns_counter += 1
    for j in range(n2):
        if M[n1+j] == -1 and j not in wom_in_und_bp:
            ns_counter += 1  
    #print("after women p.o.w.:", final)
    
    return len(final), ns_counter
"""def NS(M):
    return M.count(-1)"""
#------------------------------------------------------------------------------
"""def NBP(M, mrank, wrank):
    n1 = len(mrank)
    n2 = len(wrank)
    nbp_counter = 0
    for m in range(n1):
        for w in range(n2):
            if isBP(M, m, w, mrank, wrank):
                nbp_counter += 1
    return nbp_counter"""
#-----------------------------------------------------------------------------
"""def NBP_NS(M, mrank, wrank):
    n1 = len(mrank)
    n2 = len(wrank)
    nbp_counter = 0
    wom_in_a_bp = []
    men_in_a_bp = []
    for m in range(n1):
        for w in range(n2):
            if isBP(M, m, w, mrank, wrank):
                nbp_counter += 1
                wom_in_a_bp.append(w) if w not in wom_in_a_bp else wom_in_a_bp
                men_in_a_bp.append(m) if m not in men_in_a_bp else men_in_a_bp
    
    ns_counter = 0
    for i in range(n1):
        if M[i] == -1 and i not in men_in_a_bp:
            ns_counter += 1
    for j in range(n2):
        if M[n1+j] == -1 and j not in wom_in_a_bp:
            ns_counter += 1       
            
    return nbp_counter, ns_counter"""
#------------------------------------------------------------------------------
"""
def F(M, mrank, wrank):
    return NS(M) + NBP(M, mrank, wrank)
"""
#------------------------------------------------------------------------------
def UND(M, mrank, wrank, gender):
    bps = []
    n1 = len(mrank)
    n2 = len(wrank)
    for i in range(n1):
        for j in range(n2):
            if isBP(M, i, j, mrank, wrank):
                bps.append([i, j])
    
    bps = man_undominated(bps, mrank, wrank, n1, n2) if gender == 0 else woman_undominated(bps, mrank, wrank, n1, n2)
    bps = woman_undominated(bps, mrank, wrank, n1, n2) if gender == 0 else man_undominated(bps, mrank, wrank, n1, n2)
    
    return bps
def man_undominated(bps, mrank, wrank, n1, n2):
    for m in range(n1):
        min_rank = n2
        for bp in bps:
            if bp[0] == m:
                if mrank[m][bp[1]] < min_rank:
                    min_rank = mrank[m][bp[1]]
        for bp in bps:
            if bp[0] == m:
                if mrank[m][bp[1]] != min_rank:
                    bps.remove(bp)
    return bps
def woman_undominated(bps, mrank, wrank, n1, n2):
    for w in range(n2):
        min_rank = n1
        for bp in bps:
            if bp[1] == w:
                if wrank[w][bp[0]] < min_rank:
                    min_rank = wrank[w][bp[0]]           
        for bp in bps:
            if bp[1] == w:
                if wrank[w][bp[0]] != min_rank:
                    bps.remove(bp)
    return bps

def new_NS(M, bps, n1, n2):
    men_in_bps = []
    wom_in_bps = []
    for bp in bps:
        men_in_bps.append(bp[0]) if bp[0] not in men_in_bps else men_in_bps
        wom_in_bps.append(bp[1]) if bp[1] not in wom_in_bps else wom_in_bps
    
    ns = 0
    for i in range(n1):
        if M[i] == -1 and i not in men_in_bps:
            ns += 1
    for j in range(n2):
        if M[n1+j] == -1 and j not in wom_in_bps:
            ns+=1
    return ns

def Fnew(M, mrank, wrank, n1, n2, gender):
    un = UND(M, mrank, wrank, gender)
    ns = new_NS(M, un, n1, n2)
    return len(un)+ns
#------------------------------------------------------------------------------
def printMatching(M, n1):
    print("-------")
    print("m\tw")
    for i in range(n1):
        print(i, "x", M[i])
            
def printPref(P):
    for i in range(len(P)):
        print(i, ":", P[i])