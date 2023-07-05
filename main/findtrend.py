import pandas as pd 
from typing import Tuple, List
from ..utils.check import TypeChecker


# TODO: 可否再精简一下逻辑
# TODO: 可否使用递归
class FindTrend(object):
    """
    寻找笔的底点和顶点
    """

    def __init__(self) -> None:

        self._high_stack = []
        self._low_stack = []
        self._high_invalid = []
        self._low_invalid = []

    def _top(self, high: pd.Series, i: int) -> None:
        """_summary_

        Args:
            high (pd.Series): 最高价序列,index类型必须为pd.DatetimeIndex
            i (int): 指针，定位K线的位置
        """
        if i - self._low_stack[-1] >= 4 and high[self._low_stack[-1]-1] < high[i] and high[self._low_stack[-1]+1] < high[i]:
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

    def _bottom(self, low: pd.Series, i: int) -> None:
        """_summary_

        Args:
            low (pd.Series): 最低价序列,index类型必须为pd.DatetimeIndex
            i (int): 指针，定位K线的位置
        """
        if i - self._high_stack[-1] >= 4 and low[self._high_stack[-1]-1] > low[i] and low[self._high_stack[-1]+1] > low[i]:
            if len(self._low_invalid) == 0:
                self._low_stack.append(i)
            else:
                if self._low_invalid[-1] > self._high_stack[-1]:
                    self._low_stack.append(i)
                else:
                    if low[self._low_invalid[-1]] >= low[i]:
                        self._low_stack.append(i)
        else:
            self._low_invalid.append(i)


    def _trend_top(self, high: pd.Series, i: int) -> None:
        """_summary_

        Args:
            high (pd.Series): 最高价序列,index类型必须为pd.DatetimeIndex
            i (int): 指针，定位K线的位置
        """
        if len(self._high_stack) == 0 and len(self._low_stack) == 0:
            self._high_stack.append(i)
        else:
            if len(self._high_stack) > len(self._low_stack):
                if high[self._high_stack[-1]] <= high[i]:
                    self._high_stack.pop()
                    self._high_stack.append(i)
            elif len(self._high_stack) == len(self._low_stack):
                if self._high_stack[0] < self._low_stack[0]:
                    self._top(high,i)
                else:
                    if high[self._high_stack[-1]] <= high[i]:
                        self._high_stack.pop()
                        self._high_stack.append(i)
            else:
                self._top(high,i)

    def _trend_bottom(self, low: pd.Series, i: int) -> None:
        """_summary_

        Args:
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
            elif len(self._low_stack) == len(self._high_stack):
                if self._low_stack[0] < self._high_stack[0]:
                    self._bottom(low,i)
                else:
                    if low[self._low_stack[-1]] >= low[i]:
                        self._low_stack.pop()
                        self._low_stack.append(i)
            else:
                self._bottom(low,i)

    @TypeChecker.datetime_index_check
    def find_trend(self, high: pd.Series, low: pd.Series) -> Tuple[List[int], List[int]]:
        """_summary_

        Args:
            high (pd.Series): 最高价序列,index类型必须为pd.DatetimeIndex
            low (pd.Series): 最低价序列,index类型必须为pd.DatetimeIndex

        Returns:
            Tuple[List[int], List[int]]: 笔的顶点和底点的位置列表
        """
        n = len(high)
        for i in range(1, n-1):
            if high[i-1] < high[i] and high[i] > high[i+1]:
                self._trend_top(high, i)
            elif low[i-1] > low[i] and low[i] < low[i+1]:
                self._trend_bottom(low, i)

        return self._high_stack, self._low_stack
