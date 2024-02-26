import pandas as pd
import streamlit as st
import pickle
import requests

st.title('V3 Model Scoring')
st.markdown('Minimum viable product for utilizing the V3 Underwriting Model')

#18 V3 Model Inputs
st.markdown('\n\nGeneral Business Info\n\n')
age_of_biz = st.number_input('Adjusted age of business')

#This is a new branch as an example

st.markdown('\n\nBanking Data\n\n')
total_end_balance_over_outflows = st.number_input("Total Ending Balance/Total Outflows in the Last Six Months")
six_m_net_cash_flow = st.number_input("Average Net Cash Flow in the Last Six Months")
six_m_net_cash_flow_ratio = st.number_input("Average Cash Netflow/Inflow Ratio in the Last Six Months")
end_bal_25k = st.number_input('Ending Bal. >$25K?')
net_cash_trend_3m = st.number_input('Net Cash Flow Trend (recent 3m/oldest 3m)')
net_cash_trend_2m = st.number_input('Net Cash Flow Trend (recent 2m/oldest 2m)')
end_bal_trend_3m = st.number_input('Ending Balance Trend (recent 3m/oldest 3m)')
end_bal_trend_2m = st.number_input('Ending Balance Trend (recent 2m/oldest 2m)')
orig_sales_vol = st.number_input('Sales Volatility in the Last Six Months')
sales_inflow_3m = st.number_input('Sales Inflow Trend (recent 3m/oldest 3m)')
sales_inflow_2m = st.number_input('Sales Inflow Trend (recent 2m/oldest 2m)')
adj_sales_vol_3m = st.number_input('Adjusted Sales Volatility (recent 3m/oldest 3m)')
adj_sales_vol_2m = st.number_input('Adjusted Sales Volatility (recent 2m/oldest 2m)')

st.markdown('\n\nCredit Bureau Data\n\n')
num_inquiries = st.number_input('Number of Inquiries in the Last Six Months')
num_30_plus_lines = st.number_input('Number of 30+ days past due tradelines in Last Six Months')
num_repaid_lines = st.number_input('Number of Fully Repaid Tradelines')
num_active_lines = st.number_input('Number of Active Tradelines')

if st.button('Calculate'):
    # Collect input data
    data = [
        age_of_biz
        , total_end_balance_over_outflows
        , six_m_net_cash_flow
        , six_m_net_cash_flow_ratio
        , end_bal_25k
        , net_cash_trend_3m
        , net_cash_trend_2m
        , end_bal_trend_3m
        , end_bal_trend_2m
        , orig_sales_vol
        , sales_inflow_3m
        , sales_inflow_2m
        , adj_sales_vol_3m
        , adj_sales_vol_2m
        , num_inquiries
        , num_30_plus_lines
        , num_repaid_lines
        , num_active_lines
    ]


    
    st.info(f"""Calculation Complete\n\n
    Adjusted Age of Business: {age_of_biz}
    Six Month Net Cash Flow: {six_m_net_cash_flow}
    Ending Balance Over 25k: {end_bal_25k}
    """)

    # if response.status_code == 200:
    #     result = response.json()["result"]
    #     st.success(f"Calculated Result: {result}")
    # else:
    #     st.error("Calculation failed")