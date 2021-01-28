import random
from Converter import changeStructure
from GentProsser import GentProsser
from LocalSearchMethods import random_match, F, RemoveBP, NBP_NS, UND
import matplotlib.pyplot as plt

def deney(n1, n2, s):
    count = 0
    for k in range(10):
        #file = open("out.txt", "a")
        for i in range(1, 5):
            fig, axs = plt.subplots(4)
            p1 = round(i*0.2, 1)
            
            for j in range(1, 5):
                p2 = round(j*0.2, 1)
                mpref, wpref = GentProsser(n1, n2, p1, p2)
                
                f, nbp, ns, steps, y = LTIU_always_min_neighbor(n1, n2, mpref, wpref, s)
                axs[j-1].plot(y, "tab:green")
                count+=1
                print(count)
                f1, nbp1, ns1, steps1, y = LTIU_random_restart(n1, n2, mpref, wpref, s)
                axs[j-1].plot(y, "tab:blue")
                count+=1
                print(count)
                f2, nbp2, ns2, steps2, y = LTIU_random_neighbor(n1,n2,mpref, wpref, s)
                axs[j-1].plot(y, "tab:orange")
                count+=1
                print(count)
                """
                file.write("1"+ str(p1)+","+str(p2)+","+str(f)+","+str(nbp)+","+str(ns)+","+str(steps)+"\n")
                file.write("2"+ str(p1)+","+str(p2)+","+str(f1)+","+str(nbp1)+","+str(ns1)+","+str(steps1)+"\n")
                file.write("3"+ str(p1)+","+str(p2)+","+str(f2)+","+str(nbp2)+","+str(ns2)+","+str(steps2)+"\n")
                file.write("4"+ str(p1)+","+str(p2)+","+str(f3)+","+str(nbp3)+","+str(ns3)+","+str(steps3)+"\n")
                """
                fig.tight_layout()
                fig.suptitle("exp:"+ str(k+1) +", n:"+str(n1)+ ", p1:"+ str(p1))
        #file.close()
    
def LTIU_always_min_neighbor(n1, n2, mpref, wpref, steps):
    mrank, wrank = changeStructure(mpref, wpref, n1, n2)
    arraysize = (n1 + n2)
    M = [-1]*arraysize
    M = random_match(M, mrank, n1, n2)
    Fprev = F(M, mpref, wpref, mrank, wrank)
    Fbest = Fprev
    stableFound = False
    NSbest = 2*n1*n2 
    Mbest = M
    begin = steps
    y = []
    while steps:
        nbp, ns = NBP_NS(M, mpref, wpref, mrank, wrank)
        #nbp = NBP(M, mrank, wrank)
        #ns = NS(M)
        f = nbp + ns
        y.append(f)
        if stableFound == False and f < Fbest:
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
            if stableFound == False and f < Fbest:
                Fbest = f
                Mbest = M
            
            #Find neighbors
            undominated_bps = UND(M, mrank, wrank, steps%2)
            #undominated_bps = UND_BP_MFWS(M, mpref, wpref, mrank, wrank)
            #undominated_bps = UND_BP_WFMS(M, mpref, wpref, mrank, wrank)
            #print(undominated_bps)
            neis = []
            for un in undominated_bps:
                copyM = M[:]
                copyM = RemoveBP(copyM, un, n1)
                neis.append(copyM)
            random_walk = 1 if random.random() <= 0.2 else 0
            if random_walk:
                M = neis[random.randint(0, len(neis)-1)] #Choose a random neighbor
            else:
                #Choose a neighbor with the minimum evaluation value
                evaluations = [F(nei, mpref, wpref, mrank, wrank) for nei in neis]
                min_eval = min(evaluations)
                if min_eval < f:  #if there is an improvement
                    indices = [i for i, v in enumerate(evaluations) if v == min_eval]
                    M = neis[random.choice(indices)]
                else:   #no improvement, random restart
                    #M = random_match(M, mrank, n1, n2)
                    
                    indices = [i for i, v in enumerate(evaluations) if v == min_eval]
                    M = neis[random.choice(indices)]
                
            steps -= 1
    
    #print(Mbest)
    nbp, ns = NBP_NS(Mbest, mpref, wpref, mrank, wrank)    
    f = ns + nbp
    return f, nbp, ns, begin-steps, y


def LTIU_random_restart(n1, n2, mpref, wpref,steps):
    mrank, wrank = changeStructure(mpref, wpref, n1, n2)
    arraysize = (n1 + n2)
    M = [-1]*arraysize
    M = random_match(M, mrank, n1, n2)
    Fprev = F(M, mpref, wpref, mrank, wrank)
    Fbest = Fprev
    stableFound = False
    NSbest = 2*n1*n2 
    Mbest = M
    begin = steps
    y = []
    while steps:
        nbp, ns = NBP_NS(M, mpref, wpref, mrank, wrank)
        #nbp = NBP(M, mrank, wrank)
        #ns = NS(M)
        f = nbp + ns
        y.append(f)
        
        
        if stableFound == False and f < Fbest:
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
            if stableFound == False and f < Fbest:
                Fbest = f
                Mbest = M
            
            #Find neighbors
            undominated_bps = UND(M, mrank, wrank, steps%2)
            #undominated_bps = UND_BP_MFWS(M, mpref, wpref, mrank, wrank)
            #undominated_bps = UND_BP_WFMS(M, mpref, wpref, mrank, wrank)
            #print(undominated_bps)
            neis = []
            for un in undominated_bps:
                copyM = M[:]
                copyM = RemoveBP(copyM, un, n1)
                neis.append(copyM)
            random_walk = 1 if random.random() <= 0.2 else 0
            if random_walk:
                M = neis[random.randint(0, len(neis)-1)] #Choose a random neighbor
            else:
                #Choose a neighbor with the minimum evaluation value
                evaluations = [F(nei, mpref, wpref, mrank, wrank) for nei in neis]
                min_eval = min(evaluations)
                if min_eval < f:  #if there is an improvement
                    indices = [i for i, v in enumerate(evaluations) if v == min_eval]
                    M = neis[random.choice(indices)]
                else:   #no improvement, random restart
                    M = random_match(M, mrank, n1, n2)
                
        steps -= 1
    
    
    #print(Mbest)
    nbp, ns = NBP_NS(Mbest, mpref, wpref, mrank, wrank)    
    f = ns + nbp
    return f, nbp, ns, begin-steps, y

def LTIU_random_neighbor(n1, n2, mpref, wpref, steps):
    mrank, wrank = changeStructure(mpref, wpref, n1, n2)
    arraysize = (n1 + n2)
    M = [-1]*arraysize
    M = random_match(M, mrank, n1, n2)
    Fprev = F(M, mpref, wpref, mrank, wrank)
    Fbest = Fprev
    stableFound = False
    NSbest = 2*n1*n2 
    Mbest = M
    begin = steps
    y = []
    while steps:
        nbp, ns = NBP_NS(M, mpref, wpref, mrank, wrank)
        #nbp = NBP(M, mrank, wrank)
        #ns = NS(M)
        f = nbp + ns
        y.append(f)   
        if stableFound == False and f < Fbest:
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
            if stableFound == False and f < Fbest:
                Fbest = f
                Mbest = M
            
            #Find neighbors
            undominated_bps = UND(M, mrank, wrank, steps%2)
            #undominated_bps = UND_BP_MFWS(M, mpref, wpref, mrank, wrank)
            #undominated_bps = UND_BP_WFMS(M, mpref, wpref, mrank, wrank)
            #print(undominated_bps)
            neis = []
            for un in undominated_bps:
                copyM = M[:]
                copyM = RemoveBP(copyM, un, n1)
                neis.append(copyM)
            random_walk = 1 if random.random() <= 0.2 else 0
            if random_walk:
                M = neis[random.randint(0, len(neis)-1)] #Choose a random neighbor
            else:
                #Choose a neighbor with the minimum evaluation value
                evaluations = [F(nei, mpref, wpref, mrank, wrank) for nei in neis]
                min_eval = min(evaluations)
                if min_eval < f:  #if there is an improvement
                    indices = [i for i, v in enumerate(evaluations) if v == min_eval]
                    M = neis[random.choice(indices)]
                else:   #no improvement, random restart
                    #M = random_match(M, mrank, n1, n2)
                    
                    #indices = [i for i, v in enumerate(evaluations) if v == min_eval]
                    M = neis[random.randint(0,len(neis)-1)]
                
        steps -= 1

    
    
    #print(Mbest)
    nbp, ns = NBP_NS(Mbest, mpref, wpref, mrank, wrank)    
    f = ns + nbp
    return f, nbp, ns, begin-steps, y



from lcvlib import findbps2, random_best_woman_for_m, man_that_generates_max_bp, ns2, nbp2, random_match2, RemoveBP2
def LCV_deney(n1, n2, mpref, wpref, iters):

        n = n1
        mrank, wrank = changeStructure(mpref, wpref, n, n)
        arraysize = 2*n
        
        M = [-1]*arraysize
        M = random_match2(M, mrank, n)
        
        Mbest = M    
        
        iterstart = iters
        y = []
        while iters:
           
            if ns2(Mbest) == 0:
                break
            X = findbps2(M, mrank, wrank, n)
            y.append(len(X)+ns2(Mbest))
            if len(X) == 0:
                #M is stable
                #random restart
                if ns2(M) < ns2(Mbest):
                    Mbest = M
                M = [-1]*arraysize
                M = random_match2(M, mrank, n)
            else:
                m = man_that_generates_max_bp(M, mrank, wrank, n)
                randWalk = random.random()
                if randWalk <= 0.2:
                    pIndex = random.randint(0, len(mpref[m])-1)
                    wIndex = random.randint(0, len(mpref[m][pIndex])-1)
                    w = mpref[m][pIndex][wIndex]
                else:
                    w = random_best_woman_for_m(mpref, m)
                M = RemoveBP2(M, m, w, n)
            iters -= 1
        
        ns_ = ns2(Mbest)
        nbp_ = nbp2(Mbest, mrank, wrank, n)
        steptotal = iterstart - iters
        return ns_+nbp_, nbp_, ns_, steptotal, y
        
deney(20, 20, 5001)