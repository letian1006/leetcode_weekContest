"""
391场周赛 三题选手
t4涉及到一个曼哈顿距离转换为切比雪夫距离的技巧
"""
from math import inf
from typing import List

from sortedcontainers import SortedList


# 两个点|xi - xj| + |yi - yj| = max(|xi_ - xj_|, |yi_ - yj_|)
# 其中xi_ = yi + xi, yi_ = yi - xi
class Solution:
    def minimumDistance(self, points: List[List[int]]) -> int:
        # 使用sl保存这些点的坐标
        x_st = SortedList()
        y_st = SortedList()
        for x, y in points:
            x_st.add(y + x)
            y_st.add(y - x)
        ans = inf
        for x, y in points:
            # 曼哈顿距离转换为切比雪夫距离
            # 这就是坐标转换 这样就不用枚举o(n^2)来计算最大曼哈顿距离了
            x, y = y + x, y - x
            x_st.remove(x)
            y_st.remove(y)
            ans = min(ans, max(x_st[-1] - x_st[0], y_st[-1] - y_st[0]))
            x_st.add(x)
            y_st.add(y)
        return ans
