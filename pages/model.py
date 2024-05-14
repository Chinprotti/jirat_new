import pandas as pd
import streamlit as st
import joblib
import shap
import os
from streamlit_shap import st_shap
import db
from st_pages import show_pages_from_config
import cleaner

show_pages_from_config()

X = pd.read_csv('data/data-20240510.csv', index_col=0)
X = cleaner.clean_input(X)

model = joblib.load('models/init_uw-20240501.pkl')

st.title('V3 Model Scoring')
st.markdown('Enter Inputs Below\n\n')

company_name = st.text_input('Company Name')
company_id = st.text_input('Jeeves Company ID')
testing_co = st.selectbox('Test or Actual Score',('','Test', 'Actual'))
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
cb_num_inquiries = st.number_input('CB Number of Inquiries L12M')

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

st.info(sum(data))


#button handling
if st.button('Calculate'):
    data = pd.DataFrame(data).T
    data = data.rename(columns={
                            0: 'age_of_biz', 1: '-1_inflow' , 2: '-2_inflow', 3: '-3_inflow'
                            , 4: '-1_outflow', 5: '-2_outflow', 6: '-3_outflow'
                            , 7: '-1_end_bal', 8: '-2_end_bal', 9: '-3_end_bal'
                            , 10: '-1_net_cash', 11: '-2_net_cash', 12: '-3_net_cash'
                            , 13: 'cb_trades_active', 14: 'cb_inquiries_l12m'})
    input_data = cleaner.clean_input(data)

    data_tuple = (
                company_name
                , int(company_id)
                , testing_co
                , input_data['age_of_biz']
                , input_data['-1_end_bal']
                , input_data['min_outflow']
                , input_data['cb_trades_active']
                , input_data['avg_bal/outflows*cb_inquiries_l12m']
                , input_data['inflows/active_trades']
                , input_data['min_end_bal*outflow_vol']
                , input_data['min_end_bal']
                , input_data['outflows_burden']
                , input_data['cash_reserve']
                , input_data['inflows/max_outflow']
                , input_data['avg_outflows*min_outflow']
                , input_data['avg_end_bal']
                , input_data['max_cash_change']
                , input_data['avg_bal/outflows']
                , input_data['max_outflow']
                , input_data['net_cash_vol']
                , input_data['outflows_burden*neg_net_cash_count']
                )
    # sql_file_path = 'sql/insert_model_inputs.sql'
    # st.info(data_tuple)
    # db.execute_sql_from_file(sql_file_path, data_tuple)
    # db.connect_to_cockroach()

    prediction = model.predict_proba(input_data)[0][1]

    def model_predict_proba(data):
        return model.predict_proba(data)[:, 1]
    
    explainer = shap.KernelExplainer(model_predict_proba, X, feature_names=input_data.columns)
    shap_values = explainer(input_data)
    st_shap(shap.waterfall_plot(shap_values[0]), width=1200, height=400)
    
    # sql_file_path = 'sql/insert_model_scores.sql'
    # data_tuple = (
    #     company_name
    #     , int(company_id)
    #     , float(prediction)
        
    # )
    # db.execute_sql_from_file(sql_file_path, data_tuple)
    st.info(f'V3 Score: {prediction}')

    #Add waterfall chart? 