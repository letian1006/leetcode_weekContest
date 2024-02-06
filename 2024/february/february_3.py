"""
2024-2-3的周赛
三题选手
最后一题一个二维前缀和 或者排序后枚举的题目
"""
from math import inf
from typing import List


class Solution:
    """
    链接: https://leetcode.cn/problems/find-the-number-of-ways-to-place-people-ii/description/

    描述:
    给你一个  n x 2 的二维数组 points ，它表示二维平面上的一些点坐标，其中 points[i] = [xi, yi] 。
    我们定义 x 轴的正方向为 右 （x 轴递增的方向），x 轴的负方向为 左 （x 轴递减的方向）。
    类似的，我们定义 y 轴的正方向为 上 （y 轴递增的方向），y 轴的负方向为 下 （y 轴递减的方向）。
    你需要安排这 n 个人的站位，这 n 个人中包括 liupengsay 和小羊肖恩 。
    你需要确保每个点处 恰好 有 一个 人。同时，liupengsay 想跟小羊肖恩单独玩耍，
    所以 liupengsay 会以 liupengsay 的坐标为 左上角 ，小羊肖恩的坐标为 右下角 建立一个矩形的围栏
    （注意，围栏可能 不 包含任何区域，也就是说围栏可能是一条线段）。如果围栏的 内部 或者 边缘 上有任何其他人，
    liupengsay 都会难过。
    请你在确保 liupengsay 不会 难过的前提下，返回 liupengsay 和小羊肖恩可以选择的 点对 数目。

    示例:
    输入：points = [[6,2],[4,4],[2,6]]
    输出：2
    解释：总共有 2 种方案安排 liupengsay 和小羊肖恩的位置，使得 liupengsay 不会难过：
    - liupengsay 站在 (4, 4) ，小羊肖恩站在 (6, 2) 。
    - liupengsay 站在 (2, 6) ，小羊肖恩站在 (4, 4) 。
    不能安排 liupengsay 站在 (2, 6) 且小羊肖恩站在 (6, 2) ，因为站在 (4, 4) 的人处于围栏内。
    """

    def numberOfPairs(self, points: List[List[int]]) -> int:
        # 先排序 然后枚举两个点
        # 按照第一个维度从小到大排序 第二个维度从大到小排序
        points.sort(key=lambda x: (x[0], -x[1]))
        n = len(points)
        ans = 0
        for i in range(n):
            max_y = -inf
            _, y0 = points[i]
            for j in range(i + 1, n):
                _, y = points[j]
                # 如果y比y0小 且比max_y大 那么就是一个合法的点对
                # x0, y0在左上角 x, y在右下角 而且这个区域内没有其他的点
                if max_y < y <= y0:
                    ans += 1
                    max_y = y
        return ans
