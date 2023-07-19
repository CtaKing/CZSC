import pandas as pd
from talib import MACD
from main.combinekline import CombineKLine
from main.findtrend import FindTrend


class MACDDivergence(object):
    """
    通过缠论笔的顶点和底点去寻找macd顶背离和底背离
    """
    def __init__(self,df:pd.DataFrame)->None:
        self._df = df
        self._top_divergence = []
        self._bottom_divergence = []

    def find_divergence(self):
        """
        价格创新高，macd没有创新高，产生顶背离，卖出信号
        价格创新低，macd没有创新低，产生底背离，买入信号
        
        """

        self._df['macd'], self._df['signal'], self._df['hist'] = MACD(self._df['close'])
        cbk = CombineKLine()
        high,low = cbk.combine_K_line(self._df['high'], self._df['low'])
        ft = FindTrend()
        _,high_point,low_point = ft.find_trend(high,low)

        high_hist = self._df['hist'][high_point.index]
        low_hist = self._df['hist'][low_point.index]

        for i in range(len(high_point)-1):
            if high_point[i] < high_point[i+1] and high_hist[i] > high_hist[i+1]:
                self._top_divergence.append(high_point[i+1:i+2].index)
        for i in range(len(low_point)-1):
            if low_point[i] > low_point[i+1] and low_hist[i] < low_hist[i+1]:
                self._bottom_divergence.append(low_point[i+1:i+2].index)

        return self._top_divergence, self._bottom_divergence