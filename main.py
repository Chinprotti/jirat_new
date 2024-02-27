import pandas as pd
import streamlit as st
import numpy as np
import joblib
import sklearn
import requests

pipeline = joblib.load('models/v3_pipeline.pkl')

st.title('V3 Model Scoring')
st.markdown('Minimum viable product for utilizing the V3 Underwriting Model')

#18 V3 Model Inputs
st.markdown('\n\nGeneral Business Info\n\n')
age_of_biz = st.number_input('Adjusted age of business')

st.markdown('\n\nBanking Data\n\n')
orig_sales_vol = st.number_input('Sales Volatility in the Last Six Months')
end_bal_25k = st.number_input('Ending Bal >$25K?', value=1)
total_end_balance_over_outflows = st.number_input("Total Ending Balance/Total Outflows in the Last Six Months")
six_m_net_cash_flow = st.number_input("Average Net Cash Flow in the Last Six Months")
net_cash_trend_3m = st.number_input('Net Cash Flow Trend (recent 3m/oldest 3m)')
net_cash_trend_2m = st.number_input('Net Cash Flow Trend (recent 2m/oldest 2m)')
six_m_net_cash_flow_ratio = st.number_input("Average Cash Netflow/Inflow Ratio in the Last Six Months")
end_bal_trend_3m = st.number_input('Ending Balance Trend (recent 3m/oldest 3m)')
end_bal_trend_2m = st.number_input('Ending Balance Trend (recent 2m/oldest 2m)')
sales_inflow_3m = st.number_input('Sales Inflow Trend (recent 3m/oldest 3m)')
sales_inflow_2m = st.number_input('Sales Inflow Trend (recent 2m/oldest 2m)')
adj_sales_vol_3m = st.number_input('Adjusted Sales Volatility (recent 3m/oldest 3m)')
adj_sales_vol_2m = st.number_input('Adjusted Sales Volatility (recent 2m/oldest 2m)')

st.markdown('\n\nCredit Bureau Data\n\n')
num_inquiries = st.number_input('Number of Inquiries in the Last Six Months')
num_30_plus_lines = st.number_input('Number of 30+ days past due tradelines in Last Six Months')
num_repaid_lines = st.number_input('Number of Fully Repaid Tradelines')
num_active_lines = st.number_input('Number of Active Tradelines')

#button handling
if st.button('Calculate'):
    # Collect input data
    data = [
        age_of_biz
        , orig_sales_vol
        , end_bal_25k
        , total_end_balance_over_outflows
        , six_m_net_cash_flow
        , net_cash_trend_3m
        , net_cash_trend_2m
        , six_m_net_cash_flow_ratio
        , end_bal_trend_3m
        , end_bal_trend_2m
        , sales_inflow_3m
        , sales_inflow_2m
        , adj_sales_vol_3m
        , adj_sales_vol_2m
        , num_inquiries
        , num_30_plus_lines
        , num_repaid_lines
        , num_active_lines
    ]
    data = np.log10(data)

    input_data = pd.DataFrame([data]
                              , columns=[
            'Adjusted_age_of_business'
            , 'Original_Sales_Volatility'
            , 'Ending_Bal._>$25K?'
            , 'Total_ending_balance/Outflows'
            , 'Average_Net_Cash_Flow'
            , 'Net_Cash_Flow_(3m)'
            , 'Net_Cash_flow_(2m)'
            , 'Average_Cash_netflow/Inflow_Ratio'
            , 'Ending_Balance_(3m)'
            , 'Ending_Balance_(2m)'
            , 'Sales_Inflow_Trend_(3m/old_3m)'
            , 'Sales_Inflow_Trend_(2m/old_2m)'
            , 'Adjusted_Sales_Volatility_(3m)'
            , 'Adjusted_Sales_Volatility_(2m)'
            , 'Number_of_inquiries_(Credit_Bureau)'
            , 'Number_of_tradelines_where_customer_went_30+_days_past_due_(Credit_Bureau)'
            , 'Number_of_fully_repaid_tradelines_(Credit_Bureau)'
            , 'Number_of_active_tradelines_(Credit_Bureau)'
            ])

    prediction = pipeline.predict_proba(input_data.replace(-np.inf, -4, in place=True)[0][1]
    
    st.info(f'V3 Score: {prediction}')