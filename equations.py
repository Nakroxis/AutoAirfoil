import numpy as np
from math import pi


def liftOrDrag(constant,v,area,density=1.225) -> float:
    '''calculates lift or drag based on the constant. Both lift and drag equations are the same apart from the constant Cl or Cd'''
    y=constant*density*pow(v,2)*.5*area
    return y

def coeffInducedDrag(span,area,Cl,efficiency=.75) -> float:
    '''calculates induced drag coefficient'''
    aspectRatio=pow(span,2)/area
    y=pow(Cl,2)/(pi*aspectRatio*efficiency)
    return y

def stallSpeed(w,Cl,area,density=1.225)->float:
    '''calculates stall speed using lift equation'''
    v=(Cl*density*.5*area/w)**-0.5
    return v

def momentofInertia(diaOut,diaIn) -> float:
    '''returns moment of inertia for a pipe'''
    i=pi*(pow(diaOut,4)-pow(diaIn,4))/64
    return i

def deflection(q,l,E,i) -> list:
    ''' returns material deflection as meters and angle. Assumes uniform load on the entire material.\n
        q= load per length (newton/meter)\n
        l= length\n
        E= modulus of elasticity\n
        i= moment of inertia
    '''
    sigma=q*pow(l,4)/(8*E*i)
    theta=q*pow(l,3)/(6*E*i)

    return [sigma,theta]


def reynoldsNumber(v,l,Vk=0.000014776,rho=1.225):
    '''returns reynolds number for airspeed v, characteristic length l (chord length)\n
        Vk= kinematic viscosity\n
        rho=fluid density
    '''
    Re=rho*v*l/Vk
    return Re