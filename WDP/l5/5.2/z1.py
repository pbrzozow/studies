import pandas as pd
def getData():
    df =pd.read_csv('WDP/l5/5.2/demografia.csv',decimal='.',na_values=['NA', 'n/a', 'NaN'])
    return df
print(getData)