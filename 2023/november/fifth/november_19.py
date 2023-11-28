import heapq
from typing import List

MOD = 10 ** 9 + 7
"""
这次周赛两题选手 t3 t4做不出来
涉及到两个知识点 一个是二进制运算的深入分析
另一个就是线段树二分我不会 但是离线也可以做这道题
"""


class Solution:
    # 链接:https://leetcode.cn/problems/maximum-xor-product/
    """
    给你三个整数 a ，b 和 n ，请你返回 (a XOR x) * (b XOR x) 的 最大值 且 x 需要满足 0 <= x < 2n。
    由于答案可能会很大，返回它对 109 + 7 取余 后的结果。
    注意，XOR 是按位异或操作。
    """

    def maximumXorProduct(self, a: int, b: int, n: int) -> int:
        """
        针对这个题目的分析 如果a和b在某个bit位上的数字都是0或者都是1
        那么我们直接将这个位置的数字置为1 使得乘积最大
        如果不一样 无论我们怎么选数字去异或a和b这个位置上一定有一个是1 一个是0
        但是有一个很关键的性质，就是0和1的总数目不变 这个题目就转换成x+y等于一个常数
        求a*b的最大值问题 也就是说要a和b尽量接近
        不妨令a >= b这时候 从0-n-1位置我们可以通过选取特定的数字改变分配
        """
        if a < b:
            a, b = b, a
        mask = (1 << n) - 1
        ax, bx = a & ~mask, b & ~mask  # 改变不了的高位
        a, b = a & mask, b & mask
        left = a ^ b  # 这个数字bit为1则表示a和b在这个位置上不一样 为0则表示一样
        now = left ^ mask  # 挑选出所有left的bit为0的位置
        ax |= now
        bx |= now
        # 如果ax == bx那么剩下的分配就是高位给大数字a 其余的位置上的1都给b
        if left and ax == bx:
            high_bit = 1 << (left.bit_length() - 1)
            ax |= high_bit
            left ^= high_bit
        bx |= left  # 不然的话 就是ax > bx 这个时候我们就要让bx尽量大 也就是低n位的1全部给b
        return ax * bx % MOD

    # 链接:https://leetcode.cn/problems/find-building-where-alice-and-bob-can-meet/
    """
    给你一个下标从 0 开始的正整数数组 heights ，其中 heights[i] 表示第 i 栋建筑的高度。
    如果一个人在建筑 i ，且存在 i < j 的建筑 j 满足 heights[i] < heights[j] ，那么这个人可以移动到建筑 j 。
    给你另外一个数组 queries ，其中 queries[i] = [ai, bi] 。第 i 个查询中，Alice 在建筑 ai ，Bob 在建筑 bi 。
    请你能返回一个数组 ans ，其中 ans[i] 是第 i 个查询中，Alice 和 Bob 可以相遇的 最左边的建筑 。如果对于查询 i ，Alice 和 Bob 不能相遇，令 ans[i] 为 -1 。
    """

    def leftmostBuildingQueries(self, heights: List[int], queries: List[List[int]]) -> List[int]:
        """
        heights = [6,4,8,5,2,7], queries = [[0,1],[0,3],[2,4],[3,4],[2,2]]
        答案:[2,5,-1,5,2]

        """
        # 离线加最小堆的做法
        # 还有一种线段树上二分的做法，其实这个题目就是要求得大于h[a]、h[b]的最小下标,前提是这两个下标在a和b的右边 这样就可以让bob和alice跳跃
        n, m = len(heights), len(queries)
        data = [[] for _ in range(n)]
        ans = [-1] * m
        for i, (a, b) in enumerate(queries):
            if a > b:
                a, b = b, a
            if a == b or heights[b] > heights[a]:
                # 此时答案就是b 就是右边柱子所在的位置
                ans[i] = b
            else:
                # 左边高右边低的时候进入这个data
                # 我们要找到第一个大于这两个高度的最左边的下标 按照右边柱子的下标添加这个询问的信息
                # 第一个是高度 第二个是询问的下标 因为我们是要按照询问的顺序返回答案的 所以我们需要保存这个信息
                data[b].append([heights[a], i])
        heap = []
        for i, h in enumerate(heights):
            # 从左到右遍历 第一个大于h的下标就是答案
            # 此时由于是最小堆 所以我们需要将小于h的下标全部弹出
            while heap and heap[0][0] < h:
                # 因为是最小堆而且是从左到右遍历 所以只要大于最小的高度就可以是答案
                _, idx = heapq.heappop(heap)
                ans[idx] = i
            # 然后加入最小堆 保证我们遍历到i的时候 这些柱子的下标都是小于i的
            # 也就是说都在此时遍历到的i的柱子的左边 符合题目意思
            for tmp in data[i]:
                heapq.heappush(heap, tmp)
        return ans


if __name__ == '__main__':
    Solution()
