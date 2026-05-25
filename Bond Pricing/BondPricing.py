import numpy as np
import pandas as pd

#Defining the functions

def calculate_bond_cashflows(coupon_rate, face, YTM, time):
    bond_value = 0
    Years = []
    Payment = []
    PVPayment = []
    CFxT = []
    CFxtx_t_plus_one = []

    for i in range(1,time):
        CF = face * coupon_rate
        PVcashflows = ((CF) / (1+YTM)**i)
        bond_value = bond_value + PVcashflows
        cfxt = PVcashflows * i
        cfxtxtplusone = PVcashflows * i * (i+1)

        Years.append(i)
        Payment.append(CF)
        PVPayment.append(PVcashflows)
        CFxT.append(cfxt)
        CFxtx_t_plus_one.append(cfxtxtplusone)

    PVFinalCF = ((face +face * coupon_rate) / (1+YTM)**time)
    bond_value = bond_value + PVFinalCF
    
    Years.append(time)
    Payment.append(face + face*coupon_rate)
    PVPayment.append(PVFinalCF)
    CFxT.append(PVFinalCF*time)
    CFxtx_t_plus_one.append(PVFinalCF*time*(time+1))

    return bond_value, Years, Payment, PVPayment, CFxT, CFxtx_t_plus_one



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
    if abs(YTM - coupon_rate) < 0.00001:
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

def compute_durations_convexity(CFxT, bond_value, YTM, CFxtx_t_plus_one):

    macaulay_duration = sum(CFxT) / bond_value
    modified_duration = macaulay_duration / (1+YTM)
    convexity = sum(CFxtx_t_plus_one) / (bond_value * (1+YTM)**2)

    print(f"\n- The average time it takes to collect this bond's cash flows is {macaulay_duration:.2f}.")
    print(f"- For a 1% decrease in YTM, this bond's price will increase by {modified_duration:.2f}%.")
    print(f"- The bond's convexity at current YTM {YTM*100}% is {convexity:.2f}.")
    #improve interpretations

    return macaulay_duration, modified_duration, convexity


#Main function to run analysis

def run_bond_analysis(coupon_rate, face, YTM, time):

    bond_value, Years, Payment, PVPayment, CFxT, CFxtx_t_plus_one = calculate_bond_cashflows(coupon_rate,face,YTM,time)

    table = create_summary_table(Years, Payment, PVPayment, CFxT)

    interpretation = interpret_bond_value(coupon_rate, YTM)

    print(f"The value of the bond is EUR {bond_value:.2f}.")
    print(interpretation + ".")
    print("\nSummary Table: ")
    print(table.to_string(index=False))
    
    compute_durations_convexity(CFxT, bond_value, YTM, CFxtx_t_plus_one)
    
    

coupon_rate = float(input("Insert the coupon rate (0.00): "))
face = int(input("Face value in EUR: "))
YTM = float(input("Insert the YTM (0.00): "))
time = int(input("Time in years: "))

run_bond_analysis(coupon_rate, face, YTM, time)