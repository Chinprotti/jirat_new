import pandas as pd
import streamlit as st
import numpy as np
import joblib
import db
import sklearn

pipeline = joblib.load('models/pipeline_19.pkl')
imputer = joblib.load('models/imputer_3m.pkl')

st.title('V3 Model Scoring')
st.markdown('Enter Inputs Below\n\n')

company_name = st.text_input('Company Name')
company_id = st.text_input('Jeeves Company ID')
st.markdown('\n\n')

st.markdown('\n\nGeneral Business Info\n\n')
age_of_biz = st.number_input('Age of business')

st.markdown('\n\nBanking Data\n\n')
sum_ending_bal_trend = st.number_input('Sum of Ending Balance Trend')
avg_sales_inflow_trend = st.number_input('Average Sales Inflow Trend')
ending_bal_3m_2m_trend = st.number_input('Ending Balance (3m_2m)')
net_cash_flow_2m_1m_trend = st.number_input('Net Cash Flow (2m_1m)')
sum_sales_inflow_trend = st.number_input('Sum Sales Inflow Trend')
ending_bal_2m_1m_trend = st.number_input('Ending Balance (2m_1m)')
avg_ending_bal_trend = st.number_input('Avg Ending Balance Trend')
net_cash_flow_3m_2m_trend = st.number_input('Net Cash Flow (3m_2m)')
avg_net_cash_flow_trend = st.number_input('Avg Net Cash Flow Trend')
sales_inflow_3m_2m_trend = st.number_input('Sales Inflow Trend (3m_2m)')
sales_inflow_2m_1m_trend = st.number_input('Sales Inflow Trend (2m_1m)')
total_end_balance_over_outflows = st.number_input('Total ending balance/Outflows')
six_m_net_cash_flow_ratio = st.number_input('Average Cash netflow/Inflow Ratio')
adj_sales_volatility = st.number_input('Adjusted Sales Volatility')
orig_sales_vol = st.number_input('Original Sales Volatility')


st.markdown('\n\nCredit Bureau Data\n\n')
num_inquiries = st.number_input('CB Number of inquiries')
num_30_plus_lines = st.number_input('CB Number of tradelines where customer went 30+ days past due')
num_repaid_lines = st.number_input('CB Number of fully repaid tradelines')
num_active_lines = st.number_input('CB Number of active tradelines')

data = [
    sum_ending_bal_trend
    ,avg_sales_inflow_trend
    ,num_active_lines
    ,ending_bal_3m_2m_trend
    ,num_repaid_lines
    ,net_cash_flow_2m_1m_trend
    ,sum_sales_inflow_trend
    ,ending_bal_2m_1m_trend
    ,avg_ending_bal_trend
    ,net_cash_flow_3m_2m_trend
    ,num_inquiries
    ,avg_net_cash_flow_trend
    ,num_30_plus_lines
    ,sales_inflow_3m_2m_trend
    ,sales_inflow_2m_1m_trend
    ,total_end_balance_over_outflows
    ,six_m_net_cash_flow_ratio
    ,adj_sales_volatility
    ,age_of_biz
    ,orig_sales_vol        
]

input_data = pd.DataFrame([data], columns=[
        'Sum of Ending Balance Trend'
        , 'Average Sales Inflow Trend'
        , 'CB Number of active tradelines'
        , 'Ending Balance (3m_2m)'
        , 'CB Number of fully repaid tradelines'
        , 'Net Cash Flow (2m_1m)'
        , 'Sum Sales Inflow Trend'
        , 'Ending Balance (2m_1m)'
        , 'Avg Ending Balance Trend'
        , 'Net Cash Flow (3m_2m)'
        , 'CB Number of inquiries'
        , 'Avg Net Cash Flow Trend'
        , 'CB Number of tradelines where customer went 30+ days past due'
        , 'Sales Inflow Trend (3m_2m)'
        , 'Sales Inflow Trend (2m_1m)'
        , 'Total ending balance/Outflows'
        , 'Average Cash netflow/Inflow Ratio'
        , 'Adjusted Sales Volatility'
        , 'Age of business'
        , 'Original Sales Volatility'
        ])

input_data['Age of business'] = np.log10(input_data['Age of business'])
input_data.replace(-np.inf, -4, inplace=True)

#button handling
if st.button('Calculate'):

    data_tuple = (
                company_name
                , int(company_id)
                , age_of_biz
                , sum_ending_bal_trend
                , avg_sales_inflow_trend
                , ending_bal_3m_2m_trend
                , net_cash_flow_2m_1m_trend
                , sum_sales_inflow_trend
                , ending_bal_2m_1m_trend
                , avg_ending_bal_trend
                , net_cash_flow_3m_2m_trend
                , avg_net_cash_flow_trend
                , sales_inflow_3m_2m_trend
                , sales_inflow_2m_1m_trend
                , total_end_balance_over_outflows
                , six_m_net_cash_flow_ratio
                , adj_sales_volatility
                , orig_sales_vol
                , int(num_inquiries)
                , int(num_30_plus_lines)
                , int(num_repaid_lines)
                , int(num_active_lines)
                )
    
    sql_file_path = 'sql/insert_model_inputs.sql'
    # st.info(data_tuple)
    db.execute_sql_from_file(sql_file_path, data_tuple)
    # db.connect_to_cockroach()

    imputed_input_data = imputer.transform(input_data)
    prediction = pipeline.predict_proba(imputed_input_data)[0][1]
    
    sql_file_path = 'sql/insert_model_scores.sql'
    data_tuple = (
        company_name
        , int(company_id)
        , float(prediction)
    )
    db.execute_sql_from_file(sql_file_path, data_tuple)
    st.info(f'V3 Score: {prediction}')