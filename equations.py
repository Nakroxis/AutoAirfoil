import numpy as np
from math import pi


def liftOrDrag(constant,v,area,density) -> float:
    '''calculates lift or drag based on the constant. Both lift and drag equations are the same apart from the constant Cl or Cd'''
    y=constant*density*pow(v,2)*.5*area
    return y

def coeffInducedDrag(span,area,Cl,efficiency) -> float:
    '''calculates induced drag coefficient'''
    aspectRatio=pow(span,2)/area
    y=pow(Cl,2)/(pi*aspectRatio*efficiency)
    return y

def stallSpeed(w,Cl,density,area)->float:
    '''calculates stall speed using lift equation'''
    v=(Cl*density*.5*area/w)**-0.5
    return v

def momentofInertia(diaOut,diaIn) -> float:
    '''returns moment of inertia for a pipe'''
    i=pi*(pow(diaOut,4)-pow(diaIn,4))/64
    return i

def deflection(q,l,E,i) -> list:
    ''' returns material deflection as meters and angle. Assumes uniform load on the entire material.

        q= load per length (newton/meter)

        l= length

        E= modulus of elasticity

        i= moment of inertia
    '''
    sigma=q*pow(l,4)/(8*E*i)
    theta=q*pow(l,3)/(6*E*i)

    return [sigma,theta]
