import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pprint import pprint as p


# %config Completer.use_jedi = False
import pickle
from pandas import Series, DataFrame
# import tabula
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

rng = np.random.default_rng(123545)

# df = tabula.read_pdf('pr.pdf', pages=1, area=[300, 10, 750, 600])
# df1 = tabula.read_pdf('pr.pdf', pages=2)
# DF = DataFrame(df[0])
# DF1 = DataFrame(df1[0])
# print(DF1.describe())

# DF1['Сумма в валюте'].replace(r'^0+|\.00 .|\D', "", regex=True)
# DF.notna()
# DF1.drop(columns=['Дата','Сумма операции' ], inplace=True)
# DF1.drop(0)
# pd.to_datetime(DF['data'], errors='ignore')
# d[d['comment'].str.contains('ГАЛИ',case=True)]


# d = pd.read_pickle('DB_work')


# with open("DF_vyborki",'rb') as f:
#     obj = pickle.load(f)

# print(obj[0])

# start_date = datetime(2020,9,20)
# date_list_rent =[(start_date + relativedelta(months=i)).date() for i in range(1,27)]
# date_list_duty =[(start_date + relativedelta(months=i)).date() for i in range(1,60)]




# def send_date(x):
#     for i in date_list:
#         if i == datetime.date(x):
#             date_list.remove(i)
#             return i
#         return np.NaN

# VV['date_duty'] = VV['date'].map(send_date)

# VV3.dropna(thresh=2)

#VV4.dropna(subset=['value','comment','comment2','date_duty','rent_duty',], how='all')
#VV4.loc[VV4['rent_duty'].notna(), "rent_accrual"] = 20000
# VV4['product_accrual_rub'] = VV4['product_accrual_usd'].dropna()* VV4['curs']
# VV4['product_accrual_rub']= VV4['product_accrual_rub'].fillna(0)
# VV4.loc[VV4['sum_rent_product']!=0]
# VV4['cumulative_Sum_rent'].loc[VV4['cumulative_Sum_rent']!=0]

# VV4.dropna(subset=['value','comment','comment2','date_duty','rent_duty',], how='all')
# df['date'] = pd.to_datetime(df['date'])
# VV6[['product_accrual_rub', 'sum_rent_product', 'value', 'cumulative_sum_rent_product', 'late_fee_0.1',
#             'cumulative_lete_fee']][0:50]

