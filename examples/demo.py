import sys
import os
sys.path.append(os.getcwd() + "/..")

import pandas as pd
from main.combinekline import CombineKLine
from main.findtrend import FindTrend
from utils.plot import KlineChart




df = pd.read_csv('data.csv',index_col=0)
df['date'] = pd.to_datetime(df['date'])
df = df.set_index('date')

low = df['low']
high = df['high']
print(type(high.index))
cbk = CombineKLine()
high,low = cbk.combine_K_line(high, low)
ft = FindTrend()
high_list,low_list = ft.find_trend(high,low)
high_point = high[high_list]
low_point = low[low_list]
point = high_point.append(low_point) 
point.sort_index(inplace=True)
kplot = KlineChart(df,point)
kplot.plot()
