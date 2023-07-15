import pandas as pd

class FindCentre(object):
    def __init__(self) -> None:
        self._high_stack = []
        self._low_stack = []
        self._centre_high = []
        self._centre_low = []

    def find_centre(self, high_point: pd.Series, low_point: pd.Series):
        """找到中枢的高点和低点

        Args:
            high_point (pd.Series): 笔高点序列
            low_point (pd.Series): 笔低点序列

        Returns:
            pd.Series: 中枢高点序列
            pd.Series: 中枢低点序列
        """
        n = min(len(high_point), len(low_point))
        i = 0
        while i < n:
            if not self._high_stack or not self._low_stack:
                self._high_stack.append(high_point[i])
                self._low_stack.append(low_point[i])
                self._centre_high.append(high_point[i:i+1])
                self._centre_low.append(low_point[i:i+1])
            else:
                if low_point[i] > self._high_stack[-1]:
                    self._high_stack.pop()
                    self._low_stack.pop()
                    if high_point.index[0] > low_point.index[0]:
                        i -= 1
                    continue
                if high_point[i] < self._low_stack[-1]:
                    self._high_stack.pop()
                    self._low_stack.pop()
                    if high_point.index[0] < low_point.index[0]:
                        i -= 1
                    continue
                if high_point[i] < self._high_stack[-1]:
                    self._high_stack.pop()
                    self._high_stack.append(high_point[i])
                    self._centre_high.pop()
                    self._centre_high.append(high_point[i:i+1])
                if low_point[i] > self._low_stack[-1]:
                    self._low_stack.pop()
                    self._low_stack.append(low_point[i])
                    self._centre_low.pop()
                    self._centre_low.append(low_point[i:i+1])
            i +=1

        return pd.concat(self._centre_high), pd.concat(self._centre_low)