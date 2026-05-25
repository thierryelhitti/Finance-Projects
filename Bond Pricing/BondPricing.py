import numpy as np
import pandas as pd

#Defining the functions

def calculate_bond_cashflows(coupon_rate, face, YTM, time):
    bond_value = 0
    Years = []
    Payment = []
    PVPayment = []
    CFxT = []

    for i in range(1,time):
        CF = face * coupon_rate
        PVcashflows = ((CF) / (1+YTM)**i)
        bond_value = bond_value + PVcashflows
        cfxt = PVcashflows * i

        Years.append(i)
        Payment.append(CF)
        PVPayment.append(PVcashflows)
        CFxT.append(cfxt)

    PVFinalCF = ((face +face * coupon_rate) / (1+YTM)**time)
    bond_value = bond_value + PVFinalCF
    
    Years.append(time)
    Payment.append(face + face*coupon_rate)
    PVPayment.append(PVFinalCF)
    CFxT.append(PVFinalCF*time)

    return bond_value, Years, Payment, PVPayment, CFxT



def create_summary_table(Years, Payment, PVPayment,CFxT):
    table = pd.DataFrame({
        "Year": Years,
        "Cash Flow": Payment,
        "PV Cash Flows": PVPayment,
        "CF * Time": CFxT
    })

    total_row = pd.DataFrame({
        "Year": ["Total"],
        "Cash Flow": [sum(Payment)],
        "PV Cash Flows": [sum(PVPayment)],
        "CF * Time": [sum(CFxT)]
    })
    
    table = pd.concat([table, total_row], ignore_index=True)

    return table.round(2)

def interpret_bond_value(coupon_rate, YTM):
    if abs(YTM - coupon_rate) < 0.01:
        status = "par"
    elif YTM < coupon_rate:
        status = "premium"
    elif YTM > coupon_rate:
        status = "discount"
    
    if status in ["discount", "premium"]:
        interpretation = "The bond is trading at a " + status
    else:
        interpretation = "The bond is trading at " + status
    
    return interpretation 

#Next add Macd, Modd and Convexity Analysis 

#Main function to run analysis

def run_bond_analysis(coupon_rate, face, YTM, time):

    bond_value, Years, Payment, PVPayment, CFxT = calculate_bond_cashflows(
        coupon_rate,face,YTM,time
    )

    table = create_summary_table(Years, Payment, PVPayment, CFxT)

    interpretation = interpret_bond_value(coupon_rate, YTM)

    print(f"The value of the bond is EUR {bond_value:.2f}.")
    print(interpretation + ".")
    print("\nSummary Table: ")
    print(table.to_string(index=False))

coupon_rate = float(input("Insert the coupon rate (0.00): "))
face = int(input("Face value in EUR: "))
YTM = float(input("Insert the YTM (0.00): "))
time = int(input("Time in years: "))

run_bond_analysis(coupon_rate, face, YTM, time)