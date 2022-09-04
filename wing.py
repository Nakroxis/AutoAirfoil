import json
import numpy as np
import numpy.polynomial.polynomial as poly
from equations import *

REYNOLDS=[50,100,200,500,1000]
TURBULANCE=["n9","n5"]

class Wing():
    def __init__(self,span,chord,airfoil) -> None:
        self.span=span
        self.chord=chord
        self.area=span*chord
        with open(f"condensed/{airfoil}.json",'r') as jsfile:
            self.airfoil=json.load(jsfile)
        

    def calculateLiftDrag(self,v,aoa,setting):
        if not isinstance(setting,int):
            try:
                temp=setting.split("-")
                indRey=REYNOLDS.index(int(temp[0]))
                indTurb=TURBULANCE.index(temp[1])
                setting=indRey*2+indTurb
            except:
                print(f"invalid setting: {setting}")
                return []
        
        clvalpha=poly.Polynomial(self.airfoil["liftaoa"][setting])
        cdvalpha=poly.Polynomial(self.airfoil["dragaoa"][setting])

        cl=clvalpha(aoa)
        cd0=cdvalpha(aoa)

        lift=liftOrDrag(cl,v,self.area)
        cdi=coeffInducedDrag(self.span,self.area,cl)
        cd=cd0+cdi
        drag=liftOrDrag(cd,v,self.area)

        return [lift,drag]


testWing=Wing(2,.275,"n22-il")
print(testWing.calculateLiftDrag(40,-5,"200-n5"))

