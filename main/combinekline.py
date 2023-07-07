import pandas as pd
from typing import Tuple
from utils.check import TypeChecker


class CombineKLine(object):
    """
    对包含关系的K线进行合并
    -------------------------------------------------------------------------
    分为两种情况：

    1.向上趋势中的K线合并，第一根K线的最大值和最小值都小于第二根K线的最大值和最小值为向上趋势

    2.向下趋势中的K线合并，第一根K线的最大值和最小值都大于第二根K线的最大值和最小值为向上趋势
    """

    def _upward_trend(self, high: pd.Series, low: pd.Series, pointer: int, method: str) -> None:
        """
        向上趋势中的两根K线合并，最高价和最低价取两根K线中最大的值
        -------------------------------------------------------------------
        分为两种情况：

            1.第一根K线包含第二根K线，保留第一根K线，删除第二根

            2.第二根K线包含第一根K线，保留第二根K线，删除第一根

        Args:
            high (pd.Series): 最高价序列,index类型必须为pd.DatetimeIndex
            low (pd.Series): 最低价序列,index类型必须为pd.DatetimeIndex
            pointer (int): 指针，定位需要合成K线的位置
            method (str, optional):需要保留的K线，first为保留第一根，last为保留第二根
        """
        if method == 'first':
            low.at[low.index[pointer]] = low[pointer + 1]
            low.drop(low.index[pointer + 1], inplace=True)
            high.drop(high.index[pointer + 1], inplace=True)
        elif method == 'last':
            low.at[low.index[pointer + 1]] = low[pointer]
            low.drop(low.index[pointer], inplace=True)
            high.drop(high.index[pointer], inplace=True)

    def _downward_trend(self, high: pd.Series, low: pd.Series, pointer: int, method: str = 'first') -> None:
        """
        向下趋势中的两根K线合并，最高价和最低价取两根K线中最大的值
        -----------------------------------------------------------------
        分为两种情况：
            1.第一根K线包含第二根K线，保留第一根K线，删除第二根

            2.第二根K线包含第一根K线，保留第二根K线，删除第一根

        Args:
            high (pd.Series): 最高价序列,index类型必须为pd.DatetimeIndex
            low (pd.Series): 最低价序列,index类型必须为pd.DatetimeIndex
            pointer (int): 指针，定位需要合成K线的位置
            method (str, optional):需要保留的K线，first为保留第一根，last为保留第二根
        """
        if method == 'first':
            high.at[high.index[pointer]] = high[pointer + 1]
            low.drop(low.index[pointer + 1], inplace=True)
            high.drop(high.index[pointer + 1], inplace=True)
        elif method == 'last':
            high.at[high.index[pointer + 1]] = high[pointer]
            low.drop(low.index[pointer], inplace=True)
            high.drop(high.index[pointer], inplace=True)

    @TypeChecker.datetime_index_check
    def combine_K_line(self, high: pd.Series, low: pd.Series) -> Tuple[pd.Series, pd.Series]:
        """
        循环最高价和最低价序列，对包含关系的K线进行合并
        ------------------------------------------------------------------ 
        Args:
            high (pd.Series): 最高价序列,index类型必须为pd.DatetimeIndex
            low (pd.Series): 最低价序列,index类型必须为pd.DatetimeIndex
        Returns:
            Tuple[pd.Series, pd.Series]: 合并后的最大值和最小值序列
        """

        # 循环序列开始合并K线
        pointer = 1
        while pointer < len(high)-2:

            # cond0 = high[pointer] <= high[pointer + 2]
            # cond1 = high[pointer] <= high[pointer + 1]
            # cond2 = high[pointer + 1] <= high[pointer + 2]

            # cond3 = low[pointer] <= low[pointer + 1]
            # cond4 = low[pointer] <= low[pointer + 2]
            # cond5 = low[pointer + 1] <= low[pointer + 2]

            # cond6 = high[pointer - 1] <= high[pointer]
            # cond7 = low[pointer - 1] <= low[pointer]

            if high[pointer] < high[pointer + 1] and low[pointer] < low[pointer + 1]:
                if high[pointer + 1] >= high[pointer + 2] and low[pointer + 1] <= low[pointer + 2]:
                    self._upward_trend(high, low, pointer+1, method='first')
                    continue
                elif high[pointer + 1] <= high[pointer + 2] and low[pointer + 1] >= low[pointer + 2]:
                    if low[pointer] >= low[pointer + 2] and high[pointer - 1] > high[pointer] and low[pointer - 1] > low[pointer]:
                        self._downward_trend(
                            high, low, pointer+1, method='last')
                        pointer -= 1
                        continue
                    else:
                        self._upward_trend(high, low, pointer+1, method='last')
                        continue
            elif high[pointer] > high[pointer + 1] and low[pointer] > low[pointer + 1]:
                if high[pointer + 1] >= high[pointer + 2] and low[pointer + 1] <= low[pointer + 2]:
                    self._downward_trend(high, low, pointer+1, method='first')
                    continue
                elif high[pointer + 1] <= high[pointer + 2] and low[pointer + 1] >= low[pointer + 2]:
                    if high[pointer] <= high[pointer + 2] and high[pointer - 1] < high[pointer] and low[pointer - 1] < low[pointer]:
                        self._upward_trend(high, low, pointer+1, method='last')
                        pointer -= 1
                        continue
                    else:
                        self._downward_trend(
                            high, low, pointer+1, method='last')
                        continue
            pointer += 1
        return high, low


