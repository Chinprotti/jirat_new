import numpy as np

def clean_input(data):
    data.reset_index(drop=True, inplace=True)
    for i in range(0, 4):
        for c in data.columns[data.columns.to_series().str.contains(f'-{i}_') == True]:
            data[c] = np.arcsinh(np.arcsinh(data[c]))

    inflow_cols = data[data.columns[data.columns.to_series().str.contains('_inflow') == True]]
    outflow_cols = data[data.columns[data.columns.to_series().str.contains('_outflow') == True]]
    net_cash_cols = data[data.columns[data.columns.to_series().str.contains('_net_cash') == True]]
    end_bal_cols = data[data.columns[data.columns.to_series().str.contains('_end_bal') == True]]

    data['age_of_biz'] = np.arcsinh(data['age_of_biz'])
    data['avg_inflows'] = inflow_cols.mean(axis=1)
    data['avg_outflows'] = outflow_cols.mean(axis=1)
    data['avg_net_cash'] = net_cash_cols.mean(axis=1)
    data['avg_end_bal'] = end_bal_cols.mean(axis=1)
    
    data['inflow_vol'] = inflow_cols.std(axis=1)
    data['outflow_vol'] = outflow_cols.std(axis=1)
    data['net_cash_vol'] = net_cash_cols.std(axis=1)
    data['end_bal_vol'] = end_bal_cols.std(axis=1)

    data[['-3_bal/outflow', '-2_bal/outflow', '-1_bal/outflow']] = end_bal_cols.values / outflow_cols.values

    data['neg_net_cash_count'] = net_cash_cols.lt(0).sum(axis=1)
    
    data['min_end_bal'] = end_bal_cols.min(axis=1)
    data['cash_reserve'] = data['min_end_bal'] / data['avg_outflows']
    data['inflows/active_trades'] = data['avg_inflows'] / data['cb_trades_active']
    data['outflows_burden'] = (data['avg_outflows'] - data['avg_inflows']) / data['avg_inflows']
    data['age_of_biz'] = np.arcsinh(data['age_of_biz'])
    data['avg_bal/outflows'] = data['avg_end_bal'] / data['avg_outflows']
    
    data['max_cash_change'] = abs(net_cash_cols).max(axis=1)
    data['min_outflow'] = outflow_cols.min(axis=1)
    data['max_outflow'] = outflow_cols.max(axis=1)
    data['inflows/max_outflow'] = data['avg_inflows'] / data['max_outflow']
    
    
    data['outflows_burden*neg_net_cash_count'] = data['outflows_burden'] * data['neg_net_cash_count']
    data['min_end_bal*outflow_vol'] = data['min_end_bal'] * data['outflow_vol']
    data['avg_bal/outflows*cb_inquiries_l12m'] = data['avg_bal/outflows'] * data['cb_inquiries_l12m']
    data['avg_outflows*min_outflow'] = data['avg_outflows'] * data['min_outflow']

    data['inflows/active_trades'].fillna(0, inplace=True)
    data['avg_bal/outflows*cb_inquiries_l12m'].fillna(0, inplace=True)
    data['-2_bal/outflow'].replace(np.inf, 1, inplace=True)
    data['inflows/active_trades'].replace(np.inf, 1, inplace=True)


    data = data[['age_of_biz', '-1_end_bal', 'min_outflow', 'cb_trades_active',
       'avg_bal/outflows*cb_inquiries_l12m', 'inflows/active_trades',
       'min_end_bal*outflow_vol', 'min_end_bal', 'outflows_burden',
       'cash_reserve', 'inflows/max_outflow', 'avg_outflows*min_outflow',
       'avg_end_bal', 'max_cash_change', 'avg_bal/outflows', 'max_outflow',
       'net_cash_vol', 'outflows_burden*neg_net_cash_count']]

    return data