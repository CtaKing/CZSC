import sys
import os
import pandas as pd
from main.combinekline import CombineKLine
from main.findtrend import FindTrend

sys.path.append(os.getcwd() + "/..")


df = pd.read_csv('data.csv')
print(df.dtypes)
low = df['low']
high = df['high']
cbk = CombineKLine()
high,low = cbk.combine_K_line(high, low)
ft = FindTrend()
high_list,low_list = ft.find_trend(high,low)
high_point = high[high_list]
low_point = low[low_list]
point = high_point.append(low_point) 
point.sort_index(inplace=True)
print(point)
