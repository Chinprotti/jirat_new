import pandas as pd
import streamlit as st
import numpy as np
import joblib
import db
from st_pages import show_pages_from_config

show_pages_from_config()

pipeline = joblib.load('models/new_v3_risk_modelinit_uw-20240501.pkl')

st.title('V3 Model Scoring')
st.markdown('Enter Inputs Below\n\n')

company_name = st.text_input('Company Name')
company_id = st.text_input('Jeeves Company ID')
st.markdown('\n\n')

st.markdown('\n\nGeneral Business Info\n\n')
age_of_biz = st.number_input('Age of business')

st.markdown('\n\nBanking Data\n\n')
outflows_burden = st.number_input('Outflows Burden')
cash_reserve = st.number_input('Cash Reserve')
inflows_active_trades = st.number('Average Inflows / CB Active Tradelines')
net_cash_vol = st.number('Net Cash Flow Volatility')
avg_bal_outflows_cb_inquiries_l12m = st.number('(Avg Ending Balance / Outflows) / CB Recent Inquiries')
max_outflow = st.number_input('Max Outflow')
min_outflow = st.number_input('Min Outflow')
max_cash_change = st.number_input('Max Cash Change')
latest_end_bal = st.number_input('Latest Month Ending Balance')
outflows_burden_neg_net_cash_count = st.number_input('Outflows Burden * Negative Net Cash Count')
avg_outflows_min_outflow = st.number_input('Avg Outflows * Min Outflow')
min_end_bal_outflow_vol = st.number_input('Min Ending Balance * Outflow Volatility')
inflows_max_outflow = st.number_input('Avg Inflows / Max Outflow')
min_end_bal = st.number_input('Min Ending Balance')
avg_bal_outflows = st.number_input('Avg Ending Balance / Avg Outflows')
avg_end_bal = st.number_input('Avg Ending Balance')

st.markdown('\n\nCredit Bureau Data\n\n')
num_active_lines = st.number_input('CB Number of active tradelines')

data = [
    age_of_biz
    ,latest_end_bal
    ,min_outflow
    ,num_active_lines
    ,avg_bal_outflows_cb_inquiries_l12m
    ,inflows_active_trades
    ,min_end_bal_outflow_vol
    ,min_end_bal
    ,outflows_burden
    ,cash_reserve
    ,inflows_max_outflow
    ,avg_outflows_min_outflow
    ,avg_end_bal
    ,max_cash_change
    ,avg_bal_outflows
    ,max_outflow
    ,net_cash_vol
    ,outflows_burden_neg_net_cash_count       
]

input_data = pd.DataFrame([data], columns=[
        'age_of_biz'
        , '-1_end_bal'
        , 'min_outflow'
        , 'cb_trades_active'
        , 'avg_bal/outflows*cb_inquiries_l12m'
        , 'inflows/active_trades'
        , 'min_end_bal*outflow_vol'
        , 'min_end_bal'
        , 'outflows_burden'
        , 'cash_reserve'
        , 'inflows/max_outflow'
        , 'avg_outflows*min_outflow'
        , 'avg_end_bal'
        , 'max_cash_change'
        , 'avg_bal/outflows'
        , 'max_outflow'
        , 'net_cash_vol'
        , 'outflows_burden*neg_net_cash_count'
        ])

input_data_sum = input_data.sum().sum()

#button handling
if st.button('Calculate'):

    data_tuple = (
                company_name
                , int(company_id)
                , age_of_biz
                ,latest_end_bal
                ,min_outflow
                ,int(num_active_lines)
                ,avg_bal_outflows_cb_inquiries_l12m
                ,inflows_active_trades
                ,min_end_bal_outflow_vol
                ,min_end_bal
                ,outflows_burden
                ,cash_reserve
                ,inflows_max_outflow
                ,avg_outflows_min_outflow
                ,avg_end_bal
                ,max_cash_change
                ,avg_bal_outflows
                ,max_outflow
                ,net_cash_vol
                ,outflows_burden_neg_net_cash_count 
                )
    
    sql_file_path = 'sql/insert_model_inputs.sql'
    # st.info(data_tuple)
    db.execute_sql_from_file(sql_file_path, data_tuple)
    # db.connect_to_cockroach()

  
    prediction = pipeline.predict_proba(imputed_input_data)[0][1]
    
    sql_file_path = 'sql/insert_model_scores.sql'
    data_tuple = (
        company_name
        , int(company_id)
        , float(prediction)
        
    )
    db.execute_sql_from_file(sql_file_path, data_tuple)
    st.info(f'Sum of input data checkpoint: {input_data_sum}')
    st.info(f'V3 Score: {prediction}')

    #Add waterfall chart? 