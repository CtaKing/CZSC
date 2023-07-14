import pandas as pd 
from typing import Tuple, List
from utils.check import TypeChecker


# TODO: 可否再精简一下逻辑
# TODO: 可否使用递归
class FindTrend(object):
    """
    寻找笔的底点和顶点
    """

    def __init__(self) -> None:
        self._high_stack = []  # 保存笔顶点的位置
        self._low_stack = []  # 保存笔底点的位置
        self._high_invalid = []  # 保存无效的笔顶点位置
        self._low_invalid = []  # 保存无效的笔底点位置

    def _top(self, high: pd.Series, low: pd.Series, i: int) -> None:
        """
        寻找笔的顶点
        -----------------------------------------------------------------
        顶分型和底分型之间至少有多余的一根k线
        构成底分型的k线没有破坏顶分型

        Args:
            high (pd.Series): 最高价序列,index类型必须为pd.DatetimeIndex
            low (pd.Series): 最低价序列,index类型必须为pd.DatetimeIndex
            i (int): 指针，定位K线的位置
        """
        if i - self._low_stack[-1] >= 4 and low[self._low_stack[-1]] < low[i + 1]:
            if len(self._high_invalid) == 0:
                self._high_stack.append(i)
            else:
                if self._high_invalid[-1] < self._low_stack[-1]:
                    self._high_stack.append(i)
                else:
                    if high[self._high_invalid[-1]] <= high[i]:
                        self._high_stack.append(i)
        else:
            self._high_invalid.append(i)

    def _bottom(self, high: pd.Series, low: pd.Series, i: int) -> None:
        """
        寻找笔的底点
        -----------------------------------------------------------------
        底分型和顶分型分型之间至少有多余的一根k线
        构成顶分型的k线没有破坏底分型

        Args:
            high (pd.Series): 最高价序列,index类型必须为pd.DatetimeIndex
            low (pd.Series): 最低价序列,index类型必须为pd.DatetimeIndex
            i (int): 指针，定位K线的位置
        """
        if i - self._high_stack[-1] >= 4 and high[self._high_stack[-1]] > high[i + 1]:
            if len(self._low_invalid) == 0:
                self._low_stack.append(i)
            else:
                if self._low_invalid[-1] < self._high_stack[-1]:
                    self._low_stack.append(i)
                else:
                    if low[self._low_invalid[-1]] >= low[i]:
                        self._low_stack.append(i)
        else:
            self._low_invalid.append(i)


    def _trend_top(self, high: pd.Series, low: pd.Series, i: int) -> None:
        """_summary_
        将高点加入笔的顶点序列

        Args:
            high (pd.Series): 最高价序列,index类型必须为pd.DatetimeIndex
            low (pd.Series): 最低价序列,index类型必须为pd.DatetimeIndex
            i (int): 指针，定位K线的位置
        """
        if len(self._high_stack) == 0 and len(self._low_stack) == 0:
            self._high_stack.append(i)
        else:
            if len(self._high_stack) > len(self._low_stack):
                if high[self._high_stack[-1]] <= high[i]:
                    self._high_stack.pop()
                    self._high_stack.append(i)
                    if self._low_stack:
                        slice = low[self._low_stack[-1]:i+1]
                        min_index_label_slice = slice.idxmin()
                        min_index_slice = low.index.get_loc(min_index_label_slice)
                        self._low_stack.pop()
                        self._low_stack.append(min_index_slice)
            elif len(self._high_stack) == len(self._low_stack):
                if self._high_stack[0] < self._low_stack[0]:
                    self._top(high,low,i)
                else:
                    if high[self._high_stack[-1]] <= high[i]:
                        self._high_stack.pop()
                        self._high_stack.append(i)
                        slice = low[self._low_stack[-1]:i+1]
                        min_index_label_slice = slice.idxmin()
                        min_index_slice = low.index.get_loc(min_index_label_slice)
                        self._low_stack.pop()
                        self._low_stack.append(min_index_slice)
            else:
                self._top(high,low,i)

    def _trend_bottom(self, high: pd.Series, low: pd.Series, i: int) -> None:
        """
        将低点加入笔的底点序列

        Args:
            high (pd.Series): 最高价序列,index类型必须为pd.DatetimeIndex
            low (pd.Series): 最低价序列,index类型必须为pd.DatetimeIndex
            i (int): 指针，定位K线的位置
        """
        if len(self._high_stack) == 0 and len(self._low_stack) == 0:
            self._low_stack.append(i)
        else:
            if len(self._low_stack) > len(self._high_stack):
                if low[self._low_stack[-1]] >= low[i]:
                    self._low_stack.pop()
                    self._low_stack.append(i)
                    if self._high_stack:
                        slice = high[self._high_stack[-1]:i+1]
                        max_index_label_slice = slice.idxmax()
                        max_index_slice = high.index.get_loc(max_index_label_slice)
                        self._high_stack.pop()
                        self._high_stack.append(max_index_slice)
            elif len(self._low_stack) == len(self._high_stack):
                if self._low_stack[0] < self._high_stack[0]:
                    self._bottom(high,low,i)
                else:
                    if low[self._low_stack[-1]] >= low[i]:
                        self._low_stack.pop()
                        self._low_stack.append(i)
                        slice = high[self._high_stack[-1]:i+1]
                        max_index_label_slice = slice.idxmax()
                        max_index_slice = high.index.get_loc(max_index_label_slice)
                        self._high_stack.pop()
                        self._high_stack.append(max_index_slice)
            else:
                self._bottom(high,low,i)

    @TypeChecker.datetime_index_check
    def _find_trend(self, high: pd.Series, low: pd.Series) -> None:
        """
        寻找笔的顶点和底点

        Args:
            high (pd.Series): 最高价序列,index类型必须为pd.DatetimeIndex
            low (pd.Series): 最低价序列,index类型必须为pd.DatetimeIndex

        Returns:
            Tuple[List[int], List[int]]: 笔的顶点和底点的位置列表
        """
        n = len(high)
        for i in range(1, n-1):
            if low[i-1] < low[i] and low[i] > low[i+1] and high[i-1] < high[i] and high[i] > high[i+1]:
                self._trend_top(high,low, i)
            elif low[i-1] > low[i] and low[i] < low[i+1] and high[i-1] > high[i] and high[i] < high[i-1]:
                self._trend_bottom(high,low, i)

    

    def find_trend(self,high: pd.Series, low: pd.Series):
        self._find_trend(high,low)
        high_point = high[self._high_stack]
        low_point = low[self._low_stack]
        point = pd.concat([high_point, low_point], axis=0) 
        point.sort_index(inplace=True)

        return point,high_point,low_point

