"""
2024-1-21的周赛 三体选手 t4没有做出
现在给出t4的代码 用到的技巧包括差分数组和精密分析
"""
from itertools import accumulate
from typing import List


class Solution:
    """
    链接:https://leetcode.cn/problems/count-the-number-of-houses-at-a-certain-distance-ii/

    描述:
    给你三个 正整数 n 、x 和 y 。
    在城市中，存在编号从 1 到 n 的房屋，由 n 条街道相连。对所有 1 <= i < n ，
    都存在一条街道连接编号为 i 的房屋与编号为 i + 1 的房屋。另存在一条街道连接编号为 x 的房屋与编号为 y 的房屋。
    对于每个 k（1 <= k <= n），你需要找出所有满足要求的 房屋对 [house1, house2] ，
    即从 house1 到 house2 需要经过的 最少 街道数为 k 。
    返回一个下标从 1 开始且长度为 n 的数组 result ，其中 result[k] 表示所有满足要求的房屋对的数量，
    即从一个房屋到另一个房屋需要经过的 最少 街道数为 k 。
    注意，x 与 y 可以 相等 。

    示例:
    输入：n = 3, x = 1, y = 3
    输出：[6,0,0]
    解释：让我们检视每个房屋对
    - 对于房屋对 (1, 2)，可以直接从房屋 1 到房屋 2。
    - 对于房屋对 (2, 1)，可以直接从房屋 2 到房屋 1。
    - 对于房屋对 (1, 3)，可以直接从房屋 1 到房屋 3。
    - 对于房屋对 (3, 1)，可以直接从房屋 3 到房屋 1。
    - 对于房屋对 (2, 3)，可以直接从房屋 2 到房屋 3。
    - 对于房屋对 (3, 2)，可以直接从房屋 3 到房屋 2。
    """

    def countOfPairs(self, n: int, x: int, y: int) -> List[int]:
        if x > y:
            # 交换位置 让x一定在y的右边
            x, y = y, x
        diff = [0] * (n + 1)

        # 将一段区间内的数通过差分数组的方式全部加上2
        # 首先假设没有x-y这条边 当我们遍历到编号为i的房屋时
        # 我们会增加哪些最短路 由于(i, j)和(j, i)都会计算一次
        # 因此我们只看一个房屋右边的房屋到当前房屋的最短路 最后再乘2即可
        def add(l, r):
            diff[l] += 2
            diff[r + 1] -= 2

        for i in range(1, n + 1):
            if x + 1 >= y:
                # 这样的边相当于没有影响
                # 因为最短路不受影响 x直接和它右边的房屋相连 等于没有
                add(1, n - i)
                continue
            if i <= x:
                k = (x + y + 1) // 2  # 在这个点的左边包括这个点 我们正常走
                # 这个点右边到y 和 y到n号房屋 走x-y这条边 路都会更短
                add(1, k - i)  # 第一段
                add(x - i + 2, y - k + x - i)  # x-y之间的后半段 适合走捷径
                add(x - i + 1, x - i + 1 + n - y)  # y之后的部分 适合走捷径
            elif i < (x + y) // 2:
                # 这个地方同理
                k = i + (y - x + 1) // 2  # 解不等式得到的分割点
                add(1, k - i)
                add(i - x + 2, y - k + i - x)
                add(i - x + 1, i - x + 1 + n - y)
            else:
                add(1, n - i)

        return list(accumulate(diff))[1:]
