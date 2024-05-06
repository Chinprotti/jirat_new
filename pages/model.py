import pandas as pd
import streamlit as st
import joblib
import db
from st_pages import show_pages_from_config

show_pages_from_config()

model = joblib.load('models/init_uw-20240501.pkl')

st.title('V3 Model Scoring')
st.markdown('Enter Inputs Below\n\n')

company_name = st.text_input('Company Name')
company_id = st.text_input('Jeeves Company ID')
st.markdown('\n\n')

st.markdown('\n\nGeneral Business Info\n\n')
age_of_biz = st.number_input('Age of business')

st.markdown('\n\nBanking Data\n\n')
month_1_inflow = st.number_input('Month 1 Inflow')
month_2_inflow = st.number_input('Month 2 Inflow')
month_3_inflow = st.number_input('Month 3 Inflow')
month_1_outflow = st.number_input('Month 1 Outflow')
month_2_outflow = st.number_input('Month 2 Outflow')
month_3_outflow = st.number_input('Month 3 Outflow')
month_1_end_balance = st.number_input('Month 1 Ending Balance')
month_2_end_balance = st.number_input('Month 2 Ending Balance')
month_3_end_balance = st.number_input('Month 3 Ending Balance')
month_1_net_cash_flow = st.number_input('Month 1 Net Cash Flow')
month_2_net_cash_flow = st.number_input('Month 2 Net Cash Flow')
month_3_net_cash_flow = st.number_input('Month 3 Net Cash Flow')

st.markdown('\n\nCredit Bureau Data\n\n')
cb_num_active_lines = st.number_input('CB Number of active tradelines')
cb_num_inquiries = st.number_input('CB Number of Inquiries')

data = [
    age_of_biz
    , month_1_inflow
    , month_2_inflow
    , month_3_inflow
    , month_1_outflow
    , month_2_outflow
    , month_3_outflow
    , month_1_end_balance
    , month_2_end_balance
    , month_3_end_balance
    , month_1_net_cash_flow
    , month_2_net_cash_flow
    , month_3_net_cash_flow
    , cb_num_active_lines
    , cb_num_inquiries     
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

#button handling
if st.button('Calculate'):

    data_tuple = (
                company_name
                , int(company_id)
                , age_of_biz
                , month_1_inflow
                , month_2_inflow
                , month_3_inflow
                , month_1_outflow
                , month_2_outflow
                , month_3_outflow
                , month_1_end_balance
                , month_2_end_balance
                , month_3_end_balance
                , month_1_net_cash_flow
                , month_2_net_cash_flow
                , month_3_net_cash_flow
                , cb_num_active_lines
                , cb_num_inquiries   
                )
    
    sql_file_path = 'sql/insert_model_inputs.sql'
    # st.info(data_tuple)
    db.execute_sql_from_file(sql_file_path, data_tuple)
    # db.connect_to_cockroach()

    prediction = model.predict_proba(input_data)[0][1]
    
    # sql_file_path = 'sql/insert_model_scores.sql'
    # data_tuple = (
    #     company_name
    #     , int(company_id)
    #     , float(prediction)
        
    # )
    # db.execute_sql_from_file(sql_file_path, data_tuple)
    st.info(f'V3 Score: {prediction}')

    #Add waterfall chart? 