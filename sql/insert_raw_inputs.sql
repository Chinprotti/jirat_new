INSERT INTO public.v3_1_raw_vars (
    jeeves_company_id
    , age_of_business
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
    , cb_inquiries_l12m
) VALUES (
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
);