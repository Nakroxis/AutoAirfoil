import os
from time import time
import numpy as np
from scipy import interpolate
import pandas as pd
import numpy.polynomial.polynomial as poly
import json

class Analyzer():
    def __init__(self,condenseAll=False,condenseOverride=False):
        
        self.aoaRange=15

        if condenseAll:
            foils=np.load("airfoilKeys.npy")
            condenseStart=time()
            notFound=0
            for foil in foils:
                if os.path.exists(f"data/{foil}.npy"):
                    self.airfoilCharacterics(foil,condenseOverride)
                else:
                    print(f"no data file for {foil} found")
                    notFound+=1
            condenseEnd=time()
            nfoils=len(foils)
            print(f"Successfully condensed {(nfoils-notFound)}/{nfoils} airfoils({(nfoils-notFound)/nfoils*100}% succes rate).\nTotal time taken for all airfoils to be condensed: {condenseEnd-condenseStart} seconds.")
        


    def airfoilCharacterics(self,key,override=False):
        #simplify the airfoil to a few usable values using polynomial regression
        characteristicIDs=['liftdrag','liftaoa','momentaoa','dragaoa','effeaoa']

        # do not recalculate already calculated values, unless override
        if os.path.exists(f"condensed/{key}.json") and not override:
            return

        if not key.endswith(".npy"):
            key.removesuffix(".npy")
        airfoil=np.load(f"data/{key}.npy",allow_pickle=True)
        condensed={}

        # ignoring liftdrag ratio as it is difficult to do regression on and cl/cd v alpha already covers its use
        ignoreLiftDrag=True

        charid=1
        for characteristic in airfoil:
            if ignoreLiftDrag:
                ignoreLiftDrag=False
                continue
            temp=[]
            for setting in characteristic:
                x=np.array([i[0] for i in setting])
                y=np.array([i[1] for i in setting])
                temp.append(poly.Polynomial.fit(x,y,4).convert().coef.tolist())
            condensed[characteristicIDs[charid]]=temp
            charid+=1
        
        with open(f"condensed/{key}.json", "w") as outfile:
            json.dump(condensed, outfile,indent=4)

    def optimalAoARange(pol4,topPercent=0.367):
        '''returns the optimal range of angle of attack and the threshold cl/cd
         
            topPercent= the first x percentages of cl/cd. for example: topPercent=0.2 returns 80 if max cl/cd is 100 and min cl/cd is 0
         '''

        pol=poly.Polynomial(pol4)
        localExtrema=[i for i in pol.deriv(1).roots() if -15<i<15 ]
        
        if len(localExtrema)<2:
            print("given polynomial has less then 2 maxima in the valid aoa range")
            return []
        temp=[pol(i) for i in localExtrema]
        sortedExtrema=sorted(list(zip(localExtrema,temp)),key=lambda x:x[1])
    
        minimum=sortedExtrema[0][0]
        maximum=sortedExtrema[-1][0]

        thresholdClCd=(pol(maximum)-pol(minimum))*(1-topPercent)
        
        offPoly=[pol4[0]-thresholdClCd,*pol4[1:]]


        offRoots=poly.Polynomial(offPoly).roots()
        errs=[abs(i-maximum) for i in offRoots]

        offRoots=sorted(list(zip(offRoots,errs)),key=lambda x:x[1])
        offRoots=[i[0] for i in offRoots]

        return [offRoots[:2],thresholdClCd]


ehe=Analyzer(condenseAll=True)