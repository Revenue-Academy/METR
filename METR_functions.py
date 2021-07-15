
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

def NPV_Depr_DBM(phi, alpha, r):
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
    NPV = phi + (1 - phi)*alpha/(r + alpha)
    return NPV

def NPV_Depr_SLM(r, n):
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
    NPV = 0
    i=0
    while i < n:
        PV = (1/n)/((1 + r)**i)
        NPV = NPV + PV
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
        r_g = ((r_f - pi)*(1 + T_L)/(1 - u)) - T_P
    elif A == 4:
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
    





