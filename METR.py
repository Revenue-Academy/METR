
"""

This program computes MARGINAL EFFECTIVE TAX RATES (METR) of Investment in Assets 
(Equipment, Buildings, Land & Inventory) in the Manufacturing Sector.

"""

'''Import libraries'''
import pandas as pd
import numpy as np
from pandas import ExcelWriter
from pandas import ExcelFile
import METR_functions as fun

'''read the data '''

df = pd.read_excel('METR parameters by Country.xlsx', 'Sheet1')

#Param_val = df["Param_values"].values


''' Define Read Paramters'''
'''

-------------------------------------------------------------------------------
Param name                       Param Symbol      Param Description
-------------------------------------------------------------------------------
Cost of Debt                      r_d             Interest Rate on Bonds
Dividend Payout Ratio             dpr            Total dividend / Earnings After Tax
Domestic CIT Rate                 u               Corporate Tax Rate   
Dividend Distribution Tax Rate    ddt           Tax Rate on Dividends distributed by corporates
Dividend Tax Rate                 t_d             Tax Rate on dividends in hands of shareholders
Domestic Inflation Rate           pi              Domestic Inflation Rate
International Real Interest Rate  i               international interest rate adjusted for inflation
Debt Asset Ratio                  beta             Ratio of Debt to Total Assets
Domestic PIT on interest          m              tax rate on interest income
Domesic PIT on capital gains      t_g              tax rate on income from capital gains
Tax depr rate Equipment           alpha_E          Depreciation rate on equipments as per tax law
Tax depr rate Buildings           alpha_B          Depreciation rate on buildings as per tax law
Econ depr rate Equipment          delta_E          Rate of economic depreciation on equipments based on useful life
Econ depr rate Buildings          delta_B         Rate of economic depreciation on buildings based on useful life
investment allowance Equipments   phi_E           Initial investment allowance on investment in equipment
investment allowance Buildings    phi_B           Initial investment allowance on investment in buildings
Sales tax on equipment and land   T_d             Rate of Sales tax paid on purchase of equipment / land
Land transfer tax / stamp duty    T_L             Rate of duty / tax on transfer of land
Property tax                      T_P             Rate of local property tax
Capital tax                       T_K             Rate of tax on Capital
Mining Royalty                    g               Rate of royalty payment on mining lease
Proportion FIFO                   p_FIFO          Proportion of inventory  valued as per first in first out
K weight equip                    w_E             proportion of investment in equipment in the sector
K weight building                 w_B             proportion of investment in building in the sector
K weight land                     w_L             proportion of investment in land in the sector
K weight inventory                w_I             proportion of investment in inventory in the sector

------------------------------------------------------------------------------------
'''
'''
------------------------------------------------------------------------------
Assign values to parameters
------------------------------------------------------------------------------
'''

#(r_d, dpr, u, ddt, t_d, pi, i, beta, m, t_g, alpha_E, alpha_B, 
 #delta_E, delta_B, phi_E, phi_B, T_d, T_L, T_P, T_K, g, p_FIFO,
 #w_E, w_B, w_L, w_I) = Param_val

'''
Get values by plugging in values in the functions
'''

'''
----------------------------
Global params
----------------------------
'''

df['t_rho'] = fun.get_tax_rate_equity(df['dividend_payout_ratio'], df['domestic_tax_rate_dividend'], df['dividend_distribution_tax'], df['domestic_pit_capital_gain'])
print("Tax rate on income from equity capital 't_rho' is", round(df['t_rho']*100, 2), '%')

# Open Economy Model r_d = international interest rate + inflation
df['r_d'] = df['international_interest_rate'] + df['inflation']
print("Cost of debt capital 'r_d' is", round(df['r_d']*100, 2), '%')

df['rho_n'] = fun.get_cost_of_equity(df['r_d'], df['domestic_pit_interest'], df['t_rho'])
print("Cost of equity capital 'rho_n' is", round(df['rho_n']*100, 2), '%')

df['r_f'] = fun.get_cost_of_financing(df['r_d'], df['debt_asset_ratio'], df['CIT_rate_2020'], df['rho_n'])
print("Cost of financing for a firm 'r_f' is", round(df['r_f']*100, 2), '%')

df['r_n'] = fun.get_hurdle_rate(df['debt_asset_ratio'], df['r_d'], df['rho_n'], df['inflation'])
print("Net post-tax real rate of return for equipment 'R_n' is", round(df['r_n']*100, 2), '%')

#print()

'''
-----------------------------
METR - Equipments
-----------------------------
'''

df['Z_E'] = fun.NPV_Depr_DBM(0, df['tax_depreciation_equipment'], df['r_f'])
#print("NPV of tax depreciation allowance for equipment 'Z_E' is", round(Z_E, 3))

df['r_g_E'] = fun.gross_pretax_rate(df['capital_input_sale_tax'], df['r_f'], df['inflation'], 
                                    df['economic_depreciation_equipment'], df['CIT_rate_2020'], 
                                    df['Z_E'], 0, df['property_tax'], 0, A=1)
#print("Gross pre-tax real rate of return for equipment 'R_g' is", round(r_g_E*100, 2), '%')


df['METR_E'] = fun.METR(df['r_g_E'], df['r_n'])
print("METR of equipment in Manufacturing sector is: ", round(df['METR_E']*100, 2), '%')

print()

'''
-------------------------------
METR-Buildings
-------------------------------
'''

df['Z_B'] = fun.NPV_Depr_DBM(0, df['tax_depreciation_building'], df['r_f'])
#print("NPV of tax depreciation allowance for buildings 'Z_B' is", round(Z_B, 3))

df['r_g_B'] = fun.gross_pretax_rate(df['capital_input_sale_tax'], df['r_f'], df['inflation'], 
                                    df['economic_depreciation_building'], df['CIT_rate_2020'], 
                                    df['Z_B'], 0, df['property_tax'], 0, A=2)
#print("Gross pre-tax real rate of return for buildings 'R_g' is", round(r_g_B*100, 2), '%')


df['METR_B'] = fun.METR(df['r_g_B'], df['r_n'])
print("METR of buildings in Manufacturing sector is: ", round(df['METR_B']*100, 2), '%')

print()

'''
--------------------------------
METR-Land
--------------------------------
'''

df['r_g_L'] = fun.gross_pretax_rate(0, df['r_f'], df['inflation'], 0, df['CIT_rate_2020'], 0, 0, 0, 0, A=3)
#print("Gross pre-tax real rate of return for land 'R_g' is", round(r_g_L*100, 2), '%')


df['METR_L'] = fun.METR(df['r_g_L'], df['r_n'])
print("METR of land in Manufacturing sector is: ", round(df['METR_L']*100, 2), '%')

print()

'''
--------------------------------
METR-Inventory
--------------------------------
'''
df['p_FIFO'] = np.where((df['inventory_accounting']=='FIFO')|(df['inventory_accounting']=='Optional'),1,0)

df['r_g_I'] = fun.gross_pretax_rate(0, df['r_f'], df['inflation'], 0, df['CIT_rate_2020'], 0, 0, 0, df['p_FIFO'], A=4)
#print("Gross pre-tax real rate of return for Inventory 'R_g' is", round(r_g_I*100, 2), '%')


df['METR_I'] = fun.METR(df['r_g_I'], df['r_n'])
print("METR of Inventory in Manufacturing sector is: ", round(df['METR_I']*100, 2), '%')

print()

'''
--------------------------------
METR-Aggregate / Weighted
--------------------------------
'''
df['METR_E_wt'] = df['METR_E']*df['capital_weight_equipment']
df['METR_B_wt'] = df['METR_B']*df['capital_weight_building']
df['METR_L_wt'] = df['METR_L']*df['capital_weight_land']
df['METR_I_wt'] = df['METR_I']*df['capital_weight_inventory']

df['METR_Overall'] =  df['METR_E_wt'] + df['METR_B_wt']  + df['METR_L_wt'] + df['METR_I_wt']
print("Weighted average METR in Manufacturing sector is: ", round(df['METR_Overall']*100, 2), '%')

print()

df.to_csv("METR_Countries.csv", index=False)