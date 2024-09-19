from bisect import bisect_left
from functools import reduce
from operator import or_
from typing import List



class Solution:
    
    """
    链接: https://leetcode.cn/problems/length-of-the-longest-increasing-path/
    描述:
    给你一个长度为 n 的二维整数数组 coordinates 和一个整数 k ，其中 0 <= k < n 。
    coordinates[i] = [xi, yi] 表示二维平面里一个点 (xi, yi) 。
    如果一个点序列 (x1, y1), (x2, y2), (x3, y3), ..., (xm, ym) 满足以下条件，那么我们称它是一个长度为 m 的 上升序列 ：
    对于所有满足 1 <= i < m 的 i 都有 xi < xi + 1 且 yi < yi + 1 。
    对于所有 1 <= i <= m 的 i 对应的点 (xi, yi) 都在给定的坐标数组里。
    请你返回包含坐标 coordinates[k] 的 最长上升路径 的长度。

    数据范围:
    1 <= n == coordinates.length <= 10 ^ 5
    coordinates[i].length == 2
    0 <= coordinates[i][0], coordinates[i][1] <= 10 ^ 9
    coordinates 中的元素 互不相同 。
    0 <= k <= n - 1
    """
    def maxPathLength(self, coordinates: List[List[int]], k: int) -> int:
        kx, ky = coordinates[k]
        coordinates.sort(key=lambda p: (p[0], -p[1]))  # 按照第一个维度升序排列 按照第二个维度降序排列 防止出现x相同，y不同却被选上的情况
        # 比如 [1, 2], [1, 3]在按照x排序之后 如果单纯看y的话 我们是有可能选中[1,3]的 但是x不满足递增 
        # 所以我们按照第二个元素降序排 得到[1, 3], [1, 2]这样就能保障我们选择的LIS长度是正确的 不会被重复的x困扰
        p = []
        ans = 0
        for x, y in coordinates:
            # 以k为分界点 求前后缀在ky限制下的最长递增子序列 前缀限制是小于ky 后缀限制是大于ky
            if x < kx and y < ky or x > kx and y > ky:
                cur = bisect_left(p, y)  # 二分求最长递增子序列
                if cur == len(p):
                    p.append(y)
                else:
                    p[cur] = y
        return len(p) + 1  # 返回最长递增子序列的长度 再加上k本身即可


    """
    链接: https://leetcode.cn/problems/find-the-maximum-sequence-value-of-array/description/
    描述: 
    给你一个整数数组 nums 和一个 正 整数 k 。
    定义长度为 2 * x 的序列 seq 的 值 为：
    (seq[0] OR seq[1] OR ... OR seq[x - 1]) XOR (seq[x] OR seq[x + 1] OR ... OR seq[2 * x - 1]).
    请你求出 nums 中所有长度为 2 * k 的子序列的最大值 。
    数据范围:
    2 <= nums.length <= 400
    1 <= nums[i] < 2^7
    1 <= k <= nums.length / 2
    """
    def maxValue(self, nums: List[int], k: int) -> int:
        # 前后缀分解 前面选k个数 后面选k个数 我们枚举分割点
        # 前缀中选取k个数能够or出来的所有数字我们都求出来 后缀中选取k个数能够or出来的所有数字我们也求出来 然后枚举答案即可
        # 这个题目最大
        mx = reduce(or_, nums)   # 内部函数求nums异或的最大值
        # print(or_)
        n = len(nums)
        # suf[i][j][x] 后i个数能够里面选j个数 是否能够得到x 这里优化掉第一个维度 是空间优化的写法
        f = [[False] * (mx + 1) for _ in range(k + 1)]
        f[0][0] = True
        suf = [None] * n # 这个数组是存储选取k个数字的条件下能不能弄出某些数字的异或值
        for i in range(n - 1, k - 1, -1): # 后缀的左端点
            for j in range(min(k - 1, n - 1 - i), -1, -1):
                for x, has_x in enumerate(f[j]):
                    if has_x:
                        f[j+1][x | nums[i]] = True  # 刷表法 之前选j个数能够得到has_x 那么此时选择nums[i]得到 x or nums[i]
            if i <= n - k:
                suf[i] = f[k].copy()
        ans = 0
        pre = [[False] * (mx + 1) for _ in range(k + 1)]
        pre[0][0] = True
        for i, v in enumerate(nums[:-k]):
            # 枚举前缀的右端点
            for j in range(min(k - 1, i), -1, -1):
                for x, has_x in enumerate(pre[j]):
                    if has_x:
                        pre[j+1][x | v] = True
            if i < k - 1:
                continue
            for x, has_x in enumerate(pre[k]):
                if has_x:
                    for y, has_y in enumerate(suf[i+1]):
                        if has_y and x ^ y > ans:
                            ans = x ^ y
            if ans == mx:
                return ans
        return ans
