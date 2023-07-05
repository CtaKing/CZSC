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
cbk = CombineKLine()
high,low = cbk.combine_K_line(high, low)
ft = FindTrend()
point = ft.find_trend(high,low)
kplot = KlineChart(df,point)
kplot.plot()
