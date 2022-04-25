
"""

This program contains functions to compute MARGINAL EFFECTIVE TAX RATES (METR) 
of Investment in Assets (Equipment, Buildings, Land & Inventory) 
in the Manufacturing Sector.

"""
'''
-------------------------------------------------------------------------------
DEFINE FUNCTIONS
-------------------------------------------------------------------------------
'''
import math as math
import numpy_financial as npf
import matplotlib.pyplot as plt
import numpy as np

def get_tax_rate_equity(dpr, t_d, ddt, t_g):
    '''
    Parameters
    ----------
    dpr : dividend payout ratio
    t_d : tax rate on dividend income
    ddt : dividend distribution tax rate 
    t_g : tax rate on income from capital gains

    Returns
    -------
    tax rate on income from investment in equity

    '''
    t_rho = dpr*(t_d + ddt) + (1-dpr)*t_g
    return t_rho


def get_cost_of_equity(r_d, m, t_rho):
    '''
    Parameters
    ----------
    m : PIT rate on interest income
    r_d : cost of debt 
    t_rho : PIT rate on equity income

    Returns
    -------
    rho_n : cost of equity (assuming that at equilibirium, 
            post tax return from debt and equity are equal)

    '''
    
    rho_n = r_d * (1 - m) / (1 - t_rho)
    return rho_n 
 
def get_cost_of_financing(r_d, beta, u, rho_n):
    '''
    Parameters
    ----------
    r_d : cost of debt 
    beta : debt to asset ratio
    u : CIT rate
    rho_n : cost of equity

    Returns
    -------
    r_f : real cost of financing for the firm -weighted average 
    cost of debt (tax deductible) and cost of equity 

    '''
    r_f = r_d*beta*(1-u) + rho_n*(1-beta)
    return r_f

def get_alpha(r, N, phi):
    # NPV_DBM = alpha/(alpha + r)
    NPV_SLM = - npf.pv(r, N, 1/N)
    alpha = r/(((1-phi)/(NPV_SLM-phi)) - 1)
    return alpha


def NPV_Depr(phi, alpha, r, SLM=False):
    '''
    Parameters
    ----------
    phi : initial investment allowance
    alpha : tax depreciation of equipments
    r : discount rate

    Returns
    -------
    Net Present Value of Tax Depreciation (declining balance method)
    and Investment Allowance discounted at opportunity cost of capital 
    
    '''
    if SLM==False:
        NPV = phi + (1 - phi)*alpha/(r + alpha)
    else:
        alpha=get_alpha(r, 1/alpha, phi)
        NPV = phi + (1 - phi)*alpha/(r + alpha)
    return NPV

def NPV_Depr_SLM(r, alpha):
    '''
    Parameters
    ----------
    r : discount rate
    n : useful life of asset for Straight Line Method for depreciation

    Returns
    -------
    Net Present Value of Tax Depreciation (straight line method)
    and Investment Allowance discounted at opportunity cost of capital

    '''
    n = 1/alpha
    NPV = 0
    i=1
    while i < (n+1):
        NPV += (alpha)/((1 + r)**i)
        i+=1
    return NPV

def gross_pretax_rate(T_d, r_f, pi, delta, u, Z, T_L, T_P, p_FIFO, A):
    '''
    Parameters
    ----------
    T_d : Sales tax on asset
    r_f : cost of financing
    pi : inflation rate.
    delta : economic depreciation of asset
    u : CIT rate
    Z : NPV of tax depreciation and investment allowance
    p_FIFO : Proportion of inventory  valued as per first in first out (FIFO=1, LIFO=0)
    A : Asset type A = 1 (Equipment), 2(Building), 3 (Land), 4 (Inventory)

    Returns
    -------
    gross pre-tax real rate of return on investment in asset

    '''
    if A == 1 or A == 2:
        r_g = ((1+T_d)*(r_f - pi + delta)*(1 - u*Z)/(1-u)) - delta
    elif A == 3:
        r_g = ((r_f - pi)*(1 + T_L)/(1 - u)) + T_P
    elif A == 4:
        r_g = (r_f - pi + u*pi*p_FIFO)/(1-u)
    return r_g

def gross_pretax_rate_equip_bld(T_d, r_f, pi, delta, u, Z):
    '''
    Parameters
    ----------
    T_d : Sales tax on asset
    r_f : cost of financing
    pi : inflation rate.
    delta : economic depreciation of asset
    u : CIT rate
    Z : NPV of tax depreciation and investment allowance
    p_FIFO : Proportion of inventory  valued as per first in first out (FIFO=1, LIFO=0)
    A : Asset type A = 1 (Equipment), 2(Building), 3 (Land), 4 (Inventory)

    Returns
    -------
    gross pre-tax real rate of return on investment in asset

    '''
    r_g = ((1+T_d)*(r_f - pi + delta)*(1 - u*Z)/(1-u)) - delta
    return r_g

def gross_pretax_rate_land(r_f, pi, u, T_L, T_P):
    '''
    Parameters
    ----------
    T_d : Sales tax on asset
    r_f : cost of financing
    pi : inflation rate.
    delta : economic depreciation of asset
    u : CIT rate
    Z : NPV of tax depreciation and investment allowance
    p_FIFO : Proportion of inventory  valued as per first in first out (FIFO=1, LIFO=0)
    A : Asset type A = 1 (Equipment), 2(Building), 3 (Land), 4 (Inventory)

    Returns
    -------
    gross pre-tax real rate of return on investment in asset

    '''
    r_g = ((r_f - pi)*(1 + T_L)/((1 - u)*(1 - T_P)))
    
    return r_g

def gross_pretax_rate_inventory(r_f, pi, u, p_FIFO):
    '''
    Parameters
    ----------
    T_d : Sales tax on asset
    r_f : cost of financing
    pi : inflation rate.
    delta : economic depreciation of asset
    u : CIT rate
    Z : NPV of tax depreciation and investment allowance
    p_FIFO : Proportion of inventory  valued as per first in first out (FIFO=1, LIFO=0)
    A : Asset type A = 1 (Equipment), 2(Building), 3 (Land), 4 (Inventory)

    Returns
    -------
    gross pre-tax real rate of return on investment in asset

    '''
    r_g = (r_f - pi + u*pi*p_FIFO)/(1-u)
    return r_g

def get_hurdle_rate(beta, r_d, rho_n, pi):
    '''
    Parameters
    ----------
    beta : debt to asset ratio
    r_d : cost of debt
    rho_n : cost of equity
    pi : inflation

    Returns
    -------
    hurdle rate or minimum rate of return expected by investor - weighted average 
    return from debt and equity

    '''
    r_n = (beta*r_d) + (1-beta)*rho_n - pi
    return r_n

def METR(r_g, r_n):
    '''
    Parameters
    ----------
    r_g : gross pre-tax real rate of return from investment in asset
    r_n : net post-tax real rate of return from investment in asset

    Returns
    -------
    Marginal Effective Tax Rate as a ratio of difference in 
    pre-tax and post-tax rate of return to pre-tax rate of return
    '''
    
    METR = (r_g - r_n)/r_g
    return METR
    





def get_EATR(r_n, delta, u, N, phi, r_f):
    alpha=get_alpha(r_f, N, phi)
    print(alpha)
    Z = NPV_Depr_DBM(0, alpha, r_f)
    print(Z)
    EATR = u*(r_n + delta*(1+Z) - r_f*Z)/r_n
    
    return EATR


def get_EMTR(u, N, phi, r_f, delta):
    alpha=get_alpha(r_f, N, phi)
    print(alpha)
    Z = NPV_Depr_DBM(0, alpha, r_f)
    print(Z)
    EMTR = (1-Z)*u*(r_f+delta)/((1-u*Z)*r_f + (1-Z)*u*delta)    
    return EMTR


def get_EATR_dev(u, t_d, t_c, t_e, r_f, N, phi, delta, r_n):
    alpha=get_alpha(r_f, N, phi)
    print(alpha)
    Z = NPV_Depr(phi, alpha, r_f, SLM=True)
    print(Z)
    A = u*Z
    gamma = (1 - t_d)/((1 - t_c)*(1 - t_e))
    print(gamma)
    EATR = 1 - gamma*(1-u) - (gamma*(1 - r_f*(1-A)) - gamma*delta*(u - A))/r_n
    return(EATR)

def get_EATR2(metr, u, r_g, r_n):
    EATR = (r_g/r_n)*metr + (1 - r_g/r_n)*u
    return EATR


def get_r_g_taxholiday(u, r_f, r_f_post, N, T, delta, r_n, pi):
    alpha = get_alpha(r_f, N, 0)
    print(alpha)
    A=[]
    R_g=[]
    t=[]
    METR=[]
    for i in range(T+3):
        #z = alpha*(1+r_f)/(alpha+r_f)
        z=0.5837
        t+=[i]
        if i == 0:
            Z=z
            r_g = ((delta + r_f_post - pi)*(1-u*z)/(1-u)) - delta
        
        elif i>0 and i < T:
            Z = (alpha*(1+r_f)/(r_f + alpha))*((1-alpha)/(1+r_f))**(T-i)
            
            r_g = (r_f+delta-pi)*(1-u*Z) + (u*alpha*(1+r_f)*((1-alpha)/(1+r_f)**(T-i))) - delta
            
        elif i==T:
            Z=z
            r_g = ((delta + r_f_post - pi)*(1-u*z)/(1-u) + (1+r_f)*u*alpha/(1-u)) - delta
        else:
            Z=z
            r_g = ((delta + r_f_post - pi)*(1-u*z)/(1-u)) - delta
        
        metr = (r_g - r_n)/r_g
        metr=round(metr*100, 2)
        Z=round(Z*100, 2)
        r_g=round(r_g*100, 2)
        A+=[Z]
        R_g+=[r_g]
        METR+=[metr] 
    METR_ave = sum(METR[1:6])/5
    fig, ax = plt.subplots()
    ax.plot(t, A, '--r', label='NPV tax depr')
    ax.plot(t, R_g, '--b', label='Gross pre-tax ROR')
    ax.plot(t, METR, 'g', lw=3, label='METR')
    ax.plot([5,5], [0, 100], 'y')
    ax.set_xlabel('Years')
    ax.set_title('CIT rate: 6%, Tax holiday period: 5 years')
    ax.legend(loc='best')
    plt.show()
    return A, R_g, METR, METR_ave
