import pandas as pd
from talib import MACD
from main.combinekline import CombineKLine
from main.findtrend import FindTrend


class Signal(object):
    def __init__(self, df:pd.DataFrame)->None:
        self._df = df

    def _macd(self, method='test'):
        self._df['macd'], self._df['signal'], self._df['hist'] = MACD(self._df['close'])
        if method == 'trade':
            if self._df['hist'][-1] < 0:
                self._df = self._df.append(pd.DataFrame({'close':self._df.close[-1],'high':self._df.high[-1]+0.5,'low':self._df.low[-1]+0.5},index=[self._df.index[-1]]))
            else:
                self._df = self._df.append(pd.DataFrame({'close':self._df.close[-1],'high':self._df.high[-1]-0.5,'low':self._df.low[-1]-0.5},index=[self._df.index[-1]]))

    def _find_divergence(self, method='test'):
        """
        通过缠论笔的顶点和底点去寻找macd顶背离和底背离
        价格创新高，macd没有创新高，产生顶背离，卖出信号
        价格创新低，macd没有创新低，产生底背离，买入信号
        
        """
        self._top_divergence = []
        self._bottom_divergence = []
        self._macd(method)
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

    def find_divergence(self, method='test'):
        return self._find_divergence(method)