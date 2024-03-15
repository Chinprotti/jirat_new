INSERT INTO public.model_inputs (
    company_name,
    jeeves_company_id,
    age_of_biz,
    sum_ending_bal_trend,
    avg_sales_inflow_trend,
    ending_bal_3m_2m_trend,
    net_cash_flow_2m_1m_trend,
    sum_sales_inflow_trend,
    ending_bal_2m_1m_trend,
    avg_ending_bal_trend,
    net_cash_flow_3m_2m_trend,
    avg_net_cash_flow_trend,
    sales_inflow_3m_2m_trend,
    sales_inflow_2m_1m_trend,
    total_end_balance_over_outflows,
    six_m_net_cash_flow_ratio,
    adj_sales_volatility,
    orig_sales_vol,
    num_inquiries,
    num_30_plus_lines,
    num_repaid_lines,
    num_active_lines 
) VALUES (
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
);