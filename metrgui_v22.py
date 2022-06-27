from msilib.schema import ComboBox
from tkinter import *
from tkinter import ttk
import tkinter
import tkinter.font as tkfont
from PIL import Image
import pandas as pd
import json
import csv
import matplotlib
matplotlib.use('TkAgg')
import numpy as np
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import seaborn as sns
import METR_functions as fun
import threading

'''
-----------------------------------------------------------------------------------------------
                                Read the data for METR parameters
-----------------------------------------------------------------------------------------------
'''
data1 = pd.read_excel('metr_paramsnew.xlsx')
country_list = []
for countries in data1['Country']:
    country_list+=[countries]

country_list.sort()
sector_list = [' ', 'Manufacturing', 'Services', 'Other']
#asset_list = ['equipment', 'building', 'Land', 'Inventory']


'''Convert csv to json file '''
file = open('metrparams.csv')
data = csv.DictReader(file)
dict={}

for rows in data:
    key = rows['Country']
    dict[key] = rows 

with open('metrparams1.json', 'w') as jsonf:
    jsonString = json.dumps(dict, indent=3)
    jsonf.write(jsonString)

'''Read the json file '''
with open('metrparams1.json') as file:
    data = json.load(file)
'''
-----------------------------------------------------------------------------------------------
                                    Create an interface
-----------------------------------------------------------------------------------------------
'''

root = Tk()

'''Specify the interface size'''
#getting screen width and height of display
win_width= root.winfo_screenwidth() 
win_height= root.winfo_screenheight()
#setting tkinter window size
root.geometry("%dx%d" % (win_width, win_height))

#root.attributes('-fullscreen', True)

'''Change the window logo'''
img=Image.open('wblogo.png')
img.save('icon.ico', format='ICO', sizes=[(30,30)])
root.iconbitmap('icon.ico')
root.title('World Bank')

'''Create a frame in root'''
frame_width='800'
frame_height='800'
bg_color1 = 'white'
bg_color2 = '#D3D3D3'
frame1=Frame(root, background=bg_color1, height=frame_height, width=frame_width)
frame1.config(relief=RIDGE, padx=2, pady=2, border=1, borderwidth=1, 
             highlightbackground='black', highlightthickness=1)
frame1.place(relx=0.5, rely=0.1)
# frame2=Frame(root, background=bg_color1, height=frame_height, width=frame_width)
# #frame2.place(relx=0.75, rely=0.1, anchor='nw')
# frame3=Frame(root, background=bg_color1, height=frame_height, width=frame_width)
# #frame3.place(relx=0.5, rely=0.52)
# frame4=Frame(root, background=bg_color1, height=frame_height, width=frame_width)
# #frame4.place(relx=0.75, rely=0.52)

""" frame_list=[frame1, frame2, frame3, frame4]

for frame in frame_list:
    frame.config(relief=RIDGE, padx=2, pady=2, border=1, borderwidth=1, 
             highlightbackground='black', highlightthickness=1)
 """
'''Specify font style'''
fontStyle_title = tkfont.Font(family="Arial", size="24", weight="bold")
fontStyle_sub_title = tkfont.Font(family="Times", size="18", weight="bold")
fontStyle_sub_sub_title = tkfont.Font(family="Times", size="15", weight="bold")
fontStyle_text = tkfont.Font(family="Andes", size="14", weight="normal")
fontStyle_comment = tkfont.Font(family="Andes", size="10", weight="normal")

'''Specify width of entry widgets'''
entry_width=10

''' Create and place a title at the top '''
Title = Label(root, text='ETR MODEL', font= fontStyle_title)
Title.config(bg='blue', fg='white')
Title.place(relx=0.5, y=0, anchor='n')


'''Create units for positioning widgets'''

x_init = 0.05
x_right_step = 0.15
y_init = 0.1
y_down_step = 0.04

'''Create a command for action when a country / asset is selected '''

tax_param_list=['Corporate income tax rate', 'Personal income tax rate', 'Asset tax rate',
                'Capital input salestax rate', 'Capital transfer tax rate','Dividend distribution tax rate',
                'Dividend tax rate', 'Capital gains tax rate','Property tax rate', 'Tax depr (equipment)', 
                'Tax depr (building)', 'Investment allowance']
corp_param_list=['Debt asset ratio', 'Dividend payout ratio', 'Weight - equipment', 'Weight - building', 
                'Weight - land', 'Weight - inventory']
data_col_list=['Country', 'CIT_rate_2019', 'CIT_rate_2020', 'inflation', 'tax_depreciation_building', 
                'tax_depreciation_equipment', 'inventory_accounting', 'asset_tax', 
                'capital_input_sale_tax', 'capital_transfer_tax', 'financial_transfer_tax_flag',
                'dividend_payout_ratio', 'dividend_distribution_tax', 'domestic_tax_rate_dividend',
                'international_interest_rate', 'debt_asset_ratio', 'domestic_pit_interest',
                'domestic_pit_capital_gain', 'economic_depreciation_equipment', 
                'economic_depreciation_building', 'investment_allowance_equipment', 
                'investment_allowance_building', 'property_tax', 'mining_royalty',
                'capital_weight_equipment', 'capital_weight_building', 'capital_weight_land',
                'capital_weight_inventory']
data_taxparam_col_list = ['CIT_rate_2020', 'domestic_pit_interest', 'asset_tax', 'capital_input_sale_tax', 
                         'capital_transfer_tax', 'dividend_distribution_tax', 'domestic_tax_rate_dividend', 
                         'domestic_pit_capital_gain','property_tax', 'tax_depreciation_equipment', 
                         'tax_depreciation_building', 'investment_allowance_equipment']
data_corpparam_col_list=['debt_asset_ratio', 'dividend_payout_ratio', 'capital_weight_equipment', 
                        'capital_weight_building', 'capital_weight_land','capital_weight_inventory']                

def selected_country_params(event):
    #Disable sector selection
    sector['state'] = 'disabled' 
    METR['METR  - Equipment'].delete(0, END)
    METR['METR - Buildings'].delete(0, END)
    METR['METR - Land'].delete(0, END)
    METR['METR - Inventory'].delete(0, END)
    METR['METR - Overall'].delete(0, END)
    
    inv_acc.delete(0, END)
    inv_acc.insert(0, data[country.get()]['inventory_accounting'])
    
    eco_param_val['Inflation rate'].delete(0, END)
    eco_param_val['Inflation rate'].insert(0, data[country.get()]['inflation'])
    eco_param_val['Economic depr (equipment)'].delete(0, END)
    eco_param_val['Economic depr (equipment)'].insert(0, data[country.get()]['economic_depreciation_equipment'])
    eco_param_val['Economic depr (building)'].delete(0, END)
    eco_param_val['Economic depr (building)'].insert(0, data[country.get()]['economic_depreciation_building'])
    eco_param_val['Interest rate'].delete(0, END)
    eco_param_val['Interest rate'].insert(0, data[country.get()]['international_interest_rate'])
    i=0
    for param in tax_param_list:
        tax_param_val[param].delete(0, END)
        tax_param_val[param].insert(0, data[country.get()][data_taxparam_col_list[i]])
        i+=1
    i=0
    for param in corp_param_list:
        corp_param_val[param].delete(0, END)
        corp_param_val[param].insert(0, data[country.get()][data_corpparam_col_list[i]])
        i+=1


def selected_sector_params(event):
    country['state'] = 'disabled'   
    
def enable_CB_sector():
    sector['state'] = 'normal'
    country['state'] = 'disabled'

def enable_CB_country():
    country['state'] = 'normal'
    sector['state'] = 'disabled'
    sector.current(0)


''' Create a scatter plot of METR by country in frame 1 '''   

df=pd.read_csv('METR_Countries.csv')
df=df[['Country', 'CIT_rate_2020', 'METR_Overall']]
df=df[(df['METR_Overall']<1)&(df['METR_Overall']>-1)]
fig=Figure(figsize=(7, 7))
ax1=fig.add_subplot(111)
ax1.scatter(df.CIT_rate_2020, df.METR_Overall, c=df.METR_Overall)
ax1.set_title('METR by country', fontsize=24, color='black', weight='bold')
ax1.set_xlabel('CIT rate', fontsize=18, color='blue', weight='bold')
ax1.set_ylabel('METR', fontsize=18, color='blue', weight='bold')
canvas = FigureCanvasTkAgg(fig, master=frame1)
canvas.get_tk_widget().pack()
canvas.draw() 
 
''' Create a function to compute METR params'''


def calc_metr():
    #Economic params
    for widget in frame1.winfo_children():
        widget.destroy()
        
    pi = float(eco_param_val['Inflation rate'].get())
    delta_E = float(eco_param_val['Economic depr (equipment)'].get())
    delta_B= float(eco_param_val['Economic depr (building)'].get())
    r_d= float(eco_param_val['Interest rate'].get())
    #Tax params
    u= float(tax_param_val['Corporate income tax rate'].get())
    m= float(tax_param_val['Personal income tax rate'].get())
    alpha_E= float(tax_param_val['Tax depr (equipment)'].get())
    alpha_B = float(tax_param_val['Tax depr (building)'].get())
    #asset_tax_rate=tax_param_val['Asset tax rate'].get()
    T_d= float(tax_param_val['Capital input salestax rate'].get())
    T_L= float(tax_param_val['Capital transfer tax rate'].get())
    ddt= float(tax_param_val['Dividend distribution tax rate'].get())
    t_div= float(tax_param_val['Dividend tax rate'].get())
    t_g= float(tax_param_val['Capital gains tax rate'].get())
    T_P= float(tax_param_val['Property tax rate'].get())
    phi= float(tax_param_val['Investment allowance'].get())
    inv_acc_val = inv_acc.get()
    if inv_acc_val == 'FIFO':
        p_FIFO = 1
    else:
        p_FIFO = 0
    #p_FIFO = float(inv_acc.get())
    #Corp params
    beta= float(corp_param_val['Debt asset ratio'].get())
    dpr= float(corp_param_val['Dividend payout ratio'].get())
    r_d = r_d + pi
    t_rho=fun.get_tax_rate_equity(dpr, t_div, ddt, t_g)
    rho_n=fun.get_cost_of_equity(r_d, m, t_rho)
    r_f=fun.get_cost_of_financing(r_d, beta, u, rho_n)
    r_n=fun.get_hurdle_rate(beta, r_d, rho_n, pi)

    #npv of depr allowances
    Z_E = fun.NPV_Depr(phi, alpha_E, r_f, SLM=False)
    Z_B = fun.NPV_Depr(0, alpha_B, r_f, SLM=True)

    #gross pre tax ROR for assets
    r_g_E = fun.gross_pretax_rate_equip_bld(T_d, r_f, pi, delta_E, u, Z_E)
    r_g_B = fun.gross_pretax_rate_equip_bld(T_d, r_f, pi, delta_B, u, Z_B)
    r_g_L = fun.gross_pretax_rate_land(r_f, pi, u, T_L, T_P)
    r_g_I = fun.gross_pretax_rate_inventory(r_f, pi, u, p_FIFO)
    metr_E = fun.METR(r_g_E, r_n)
    metr_B = fun.METR(r_g_B, r_n)
    metr_L = fun.METR(r_g_L, r_n)
    metr_I = fun.METR(r_g_I, r_n)
    wt_eq = float(corp_param_val['Weight - equipment'].get())
    wt_bld = float(corp_param_val['Weight - building'].get())
    wt_land= float(corp_param_val['Weight - land'].get())
    wt_inv= float(corp_param_val['Weight - inventory'].get())
    metr_overall = (wt_eq*metr_E + wt_bld*metr_B + wt_land*metr_L + wt_inv*metr_I)
    metr_E = "{:.2%}".format(fun.METR(r_g_E, r_n))
    metr_B = "{:.2%}".format(fun.METR(r_g_B, r_n))
    metr_L = "{:.2%}".format(fun.METR(r_g_L, r_n))
    metr_I = "{:.2%}".format(fun.METR(r_g_I, r_n))

    METR['METR  - Equipment'].delete(0, END)
    METR['METR  - Equipment'].insert(0, metr_E)
    METR['METR - Buildings'].delete(0, END)
    METR['METR - Buildings'].insert(0, metr_B)
    METR['METR - Land'].delete(0, END)
    METR['METR - Land'].insert(0, metr_L)
    METR['METR - Inventory'].delete(0, END)
    METR['METR - Inventory'].insert(0, metr_I)
    METR['METR - Overall'].delete(0, END)
    METR['METR - Overall'].insert(0, "{:.2%}".format(metr_overall))
    
    con_name=country.get()
    fig=Figure(figsize=(7, 7))
    ax1=fig.add_subplot(111)
    ax1.scatter(df.CIT_rate_2020, df.METR_Overall, c=df.METR_Overall)
    ax1.set_title('METR by country', fontsize=24, color='black', weight='bold')
    ax1.set_xlabel('CIT rate', fontsize=18, color='blue', weight='bold')
    ax1.set_ylabel('METR', fontsize=18, color='blue', weight='bold')
    ax1.scatter(u, metr_overall)
    ax1.text(u, metr_overall, con_name[:3], fontsize=18, color='red')
    plt.show()
    canvas = FigureCanvasTkAgg(fig, master=frame1)
    canvas.get_tk_widget().pack()
    canvas.draw() 

'''Create a label & Combobox for selecting country '''
country_label=Label(root, text='Select country', font=fontStyle_sub_title)
country_label.config(fg="blue")
country_label.place(relx=x_init, rely=y_init, anchor='w')
country = ttk.Combobox(root, value = country_list, font=fontStyle_text, state='normal')
country.place(relx=x_init, rely=(y_init+y_down_step), anchor='w')
country.current()
country.bind('<<ComboboxSelected>>', selected_country_params)

""" '''Create a label & Combobox for selecting Sector '''
sector_label=Label(root, text='Select Sector', font=fontStyle_sub_title)
sector_label.config(fg="blue")
sector_label.place(relx=(x_init+x_right_step), rely=(y_init), anchor='w')
sector = ttk.Combobox(root, value = sector_list)
sector.place(relx=(x_init+x_right_step), rely=(y_init+y_down_step), anchor='w')
sector.current()
sector.bind('<<ComboboxSelected>>', selected_sector_params) """

'''Create a label & Combobox for selecting Sector '''
Sector_label=Label(root, text='Select Sector', font=fontStyle_sub_title)
Sector_label.config(fg="blue")
Sector_label.place(relx=(x_init+x_right_step), rely=(y_init), anchor='w')
sector = ttk.Combobox(root, value = sector_list, font=fontStyle_text, state='normal')
sector.place(relx=(x_init+x_right_step), rely=(y_init+y_down_step), anchor='w')
sector.current(0)
sector.bind('<<ComboboxSelected>>', selected_sector_params)

'''Create a Label and Combobox for selecting inventory accounting'''
#inv_acc_list = ['FIFO', 'LIFO', 'Optional']
Inv_label = Label(root, text='Inventory accounting', font=fontStyle_sub_title)
Inv_label.configure(fg="blue")
Inv_label.place(relx=x_init+2*x_right_step, rely=y_init, anchor='w')
inv_acc = Entry(root, width=entry_width, font=fontStyle_text)
inv_acc.place(relx=x_init+2*x_right_step, rely=y_init+y_down_step, anchor='w')
Inv_label2 = Label(root, text='FIFO = 1, Other = 0', font=fontStyle_comment)
Inv_label2.configure(fg="grey")
Inv_label2.place(relx=x_init+2*x_right_step, rely=y_init+1.5*y_down_step, anchor='w')
# inv_acc = ttk.Combobox(root, value = inv_acc_list, font=fontStyle_text, state='normal')
# inv_acc.place(relx=x_init+2*x_right_step, rely=y_init+y_down_step, anchor='w')
# inv_acc.current(0)
# inv_acc.bind('<<ComboboxSelected>>', selected_inv_acc)

''' Create a Label and entry widget for economic params '''
ecoparam_label = Label(root, text='Economic parameters', font=fontStyle_sub_title)
ecoparam_label.config(fg="blue")
ecoparam_label.place(relx=x_init, rely=(y_init+2*y_down_step), anchor='w')

econ_param_list=['Inflation rate', 'Economic depr (equipment)', 'Economic depr (building)',
                'Interest rate']
num=3
eco_param_val = {}

for param in econ_param_list:
    label = Label(root, text=param, font=fontStyle_text)
    label.place(relx=x_init, rely=(y_init+num*y_down_step), anchor='w')
    eco_param_val[param] = Entry(root, width=entry_width, font=fontStyle_text)
    eco_param_val[param].place(relx=x_init+x_right_step, rely=(y_init+num*y_down_step), anchor='w')
    num+=1

''' Create a Label and entry widget for tax params '''
taxparam_label = Label(root, text='Tax parameters', font=fontStyle_sub_title)
taxparam_label.config(fg="blue")
taxparam_label.place(relx=x_init, rely=(y_init+num*y_down_step), anchor='w')

tax_param_list1=['Corporate income tax rate', 'Personal income tax rate', 'Tax depr (equipment)', 
                'Tax depr (building)', 'Asset tax rate', 'Capital input salestax rate', 
                'Capital transfer tax rate', 'Dividend distribution tax rate', 
                'Dividend tax rate', 'Capital gains tax rate','Property tax rate', 'Investment allowance']

num+=1
tax_param_val={}
for param in tax_param_list1:
    label = Label(root, text=param, font=fontStyle_text)
    label.place(relx=x_init, rely=(y_init+num*y_down_step), anchor='w')
    tax_param_val[param] = Entry(root, width=entry_width, font=fontStyle_text)
    tax_param_val[param].place(relx=x_init+x_right_step, rely=(y_init+num*y_down_step), anchor='w')
    num+=1

'''Create a exit button '''
exit_button=Button(root, text="Exit", height=1, width=5, command=root.destroy)
exit_button.config(font=fontStyle_sub_title, fg="red", borderwidth=1)
exit_button.place(relx=x_init+1.5*x_right_step, rely=y_init+num*y_down_step, anchor='w')

''' Create a Label and entry widget for corporate params '''
corpparam_label = Label(root, text='Corporate parameters', font=fontStyle_sub_title)
corpparam_label.config(fg="blue")
corpparam_label.place(relx=x_init+1.5*x_right_step, rely=(y_init+2*y_down_step), anchor='w')

corp_param_list=['Debt asset ratio', 'Dividend payout ratio', 'Weight - equipment', 'Weight - building', 
                'Weight - land', 'Weight - inventory']
num1=3
corp_param_val={}
for param in corp_param_list:
    label = Label(root, text=param, font=fontStyle_text)
    label.place(relx=x_init+1.5*x_right_step, rely=(y_init+num1*y_down_step), anchor='w')
    corp_param_val[param] = Entry(root, width=entry_width, font=fontStyle_text)
    corp_param_val[param].place(relx=x_init+2.25*x_right_step, rely=(y_init+num1*y_down_step), anchor='w')
    num1+=1

'''Create labels for METR values'''
METR={}
metr_list=['METR  - Equipment', 'METR - Buildings', 'METR - Land', 'METR - Inventory', 'METR - Overall']
for metr in metr_list:
    label = Label(root, text=metr, font=fontStyle_text)
    label.place(relx=x_init+1.5*x_right_step, rely=(y_init+num1*y_down_step), anchor='w')
    METR[metr] = Entry(root, width=entry_width, font=fontStyle_text, state='normal')
    METR[metr].place(relx=x_init+2.25*x_right_step, rely=(y_init+num1*y_down_step), anchor='w')
    num1+=1

''' Create a button for computing METR '''
num1+=1
Metr_button = Button(root, text="Compute METR", padx=10, pady=10, command=calc_metr)
Metr_button.config(font=fontStyle_sub_sub_title, fg="red")
Metr_button.place(relx=x_init+1.5*x_right_step, rely=y_init+num1*y_down_step, anchor="w")


num1+=2
'''Create a Combobox enable button '''
enable_button1=Button(root, text="Enable Sector", height=1, width=11, command=enable_CB_sector)
enable_button1.config(font=fontStyle_sub_sub_title, fg="red", borderwidth=1)
enable_button1.place(relx=x_init+1.5*x_right_step, rely=y_init+num1*y_down_step, anchor='w')

num1+=2
'''Create a Combobox enable button '''
enable_button2=Button(root, text="Enable Country", height=1, width=11, command=enable_CB_country)
enable_button2.config(font=fontStyle_sub_sub_title, fg="red", borderwidth=1)
enable_button2.place(relx=x_init+1.5*x_right_step, rely=y_init+num1*y_down_step, anchor='w')



root.mainloop()