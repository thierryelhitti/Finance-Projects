import numpy as np
import pandas as pd

def calculate_bond_cashflows(coupon_rate, face, YTM, time):
    bond_value = 0

    for i in range(1,time):
        PVcashflows = ((face * coupon_rate) / (1+YTM)**i)
        bond_value = bond_value + PVcashflows
    PVFinalCF = ((face +face * coupon_rate) / (1+YTM)**time)
    bond_value = bond_value + PVFinalCF
    formatted_value = print(f"{bond_value:2f}")
    
    return formatted_value

calculate_bond_cashflows(0.05,100,0.05,5)




