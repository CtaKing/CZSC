import sys
import os
sys.path.append(os.getcwd() + "/..")

import pandas as pd
from main import combinekline, findtrend, findcentre
from utils.plot import KlineChart




df = pd.read_csv('data.csv',index_col=0)
df['date'] = pd.to_datetime(df['date'])
df = df.set_index('date')
low = df['low']
high = df['high']
cbk = combinekline.CombineKLine()
high,low = cbk.combine_K_line(high, low)
ft = findtrend.FindTrend()
point,high_point,low_point = ft.find_trend(high,low)
fc = findcentre.FindCentre()
high_centre, low_centre = fc.find_centre(high_point,low_point)
kplot = KlineChart(df,point,high_centre,low_centre)
kplot.plot()
