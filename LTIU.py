#LTIU Implementation
#Yavuz Güleşen, 10/10/2020

import random
from Converter import changeStructure
from LocalSearchMethods import random_match, F, RemoveBP, UND, NBP_NS
import matplotlib.pyplot as plt
from GentProsser import GentProsser

def LTIU(mpref, wpref):
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
    begin = steps
    y = []
    while steps:
        print("| LTIU")
        print("| step:", begin-steps)
        nbp, ns = NBP_NS(M, mpref, wpref, mrank, wrank)
        #nbp = NBP(M, mrank, wrank)
        #ns = NS(M)
        f = nbp + ns
        print("| f:", f)
        print("-------------")
        y.append(f)
        
        
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
    """
    plt.plot(y)
    plt.title("LTIU n:" + str(n1) + ", p1:" + str(p1) + ", p2:"+ str(p2))
    plt.xlabel("steps")
    plt.ylabel("f = nbp + ns")
    plt.show() 
    """
    if Fbest == 0:
        print("Perfect matching found")
    elif stableFound == True:
        print("Stable matching found")
    else:
        print("Nonstable matching found")

    #print(Mbest)
    nbp, ns = NBP_NS(Mbest, mpref, wpref, mrank, wrank)    
    f = ns + nbp
    print("ns:", ns, " nbp:", nbp," f:", f, " steps:", begin-steps)
    print("------------------------------")
    return f, nbp, ns, begin-steps, y

def main():
    p1 = round(random.random(), 1)
    p2 = round(random.random(), 1)
    n1 = 20
    n2 = n1
    mpref, wpref = GentProsser(n1, n2, p1, p2)
    f, nbp, ns, steps, flist = LTIU(mpref, wpref)
    plt.plot(flist)
    plt.title("LTIU n:" + str(n1) + ", p1:" + str(p1) + ", p2:"+ str(p2))
    plt.xlabel("steps")
    plt.ylabel("f = nbp + ns")
    plt.show() 
    
main()
