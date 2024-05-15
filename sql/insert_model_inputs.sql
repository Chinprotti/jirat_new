INSERT INTO public.v3_1_model_inputs (
    company_name
    , jeeves_company_id
    , is_test
    , age_of_business
    , month_1_end_bal
    , min_outflows
    , cb_trades_active
    , avg_bal_over_outflows_times_cb_inquiries_l12m
    , inflows_over_active_trades
    , min_end_bal_times_outflow_vol
    , min_end_bal
    , outflows_burden
    , cash_reserve
    , inflows_over_max_outflow
    , avg_outflows_times_min_outflow
    , avg_end_bal
    , max_cash_change
    , avg_bal_over_outflows
    , max_outflow
    , net_cash_vol
    , outflows_burden_times_neg_net_cash_count
) VALUES (
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
);