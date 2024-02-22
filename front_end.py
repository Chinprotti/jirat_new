import streamlit as st
import requests

st.title('JIRAT')
st.markdown('Minimum viable product for utilizing the V3 Underwriting Model')

#18 V3 Model Inputs
total_end_balance_over_outflows = st.number_input("6m Avg Ending Balance / Outflows")
six_m_net_cash_flow = st.number_input("6m Avg")
six_m_net_cash_flow = st.number_input("6m Average")
age_of_biz = st.number_input('Adjusted age of business')
orig_sales_vol = st.number_input('Original Sales Volatility')
end_bal_over_outflows = st.number_input('Total ending balance/Outflows')
avg_net_cash_flow = st.number_input('Average Net Cash Flow')
net_cash_flow_3m = st.number_input('Net Cash Flow (3m)')
net_cash_flow_3m = st.number_input('Net Cash flow (2m)')
avg_net_cash_over_inflow = st.number_input('Average Cash netflow/Inflow Ratio')
end_bal_3m = st.number_input('Ending Balance (3m)')
end_bal_2m = st.number_input('Ending Balance (2m)')
sales_inflow_3m = st.number_input('Sales Inflow Trend (3m/old 3m)')
sales_inflow_2m = st.number_input('Sales Inflow Trend (2m/old 2m)')
adj_sales_vol_3m = st.number_input('Adjusted Sales Volatility (3m)')
adj_sales_vol_2m = st.number_input('Adjusted Sales Volatility (2m)')
num_inquiries = st.number_input('Number of inquiries')
num_30_plus_lines = st.number_input('Number of tradelines where customer went 30+ days past due')
num_repaid_lines = st.number_input('Number of fully repaid tradelines (Credit Bureau)')
num_active_lines = st.number_input('Number of active tradelines')

if st.button("Calculate"):
    data = {
        
    }

    # Adjust the backend URL if you create a custom domain on Streamlit Cloud
    response = requests.post("http://jirat.streamlitapp.com/calculate", json=data) 

    if response.status_code == 200:
        result = response.json()["result"]
        st.success(f"Calculated Result: {result}")
    else:
        st.error("Calculation failed")
