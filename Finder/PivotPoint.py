def get_cpr_pivots(data):

    #CPR
    data['Pivot'] = (data['high'] + data['low'] + data['close'])/3
    data['BC'] = (data['high'] + data['low'])/2
    data['TC'] = (data['Pivot'] - data['BC']) + data['Pivot']
    data['Pivot_Range'] = abs(data['TC'] - data['BC'])

    #Standard Pivot Points
    data['R1'] = (2*data['Pivot']) - data['low']
    data['S1'] = (2*data['Pivot']) - data['high']
    data['R2'] = (data['Pivot']) + (data['high'] - data['low'])
    data['S2'] = (data['Pivot']) - (data['high'] - data['low'])
    data['R3'] = (data['R1']) + (data['high'] - data['low'])
    data['S3'] = (data['S1']) - (data['high'] - data['low'])
    data['R4'] = (data['R3']) + (data['R2'] - data['R1'])
    data['S4'] = (data['S3']) - (data['S1'] - data['S2'])

    return data