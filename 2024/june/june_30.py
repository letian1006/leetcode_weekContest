from typing import List


class Solution:
    """
    链接: https://leetcode.cn/problems/find-the-maximum-length-of-valid-subsequence-ii/description/
    描述:
    给你一个整数数组 nums 和一个 正 整数 k 。
    nums的一个子序列sub 的长度为 x ，如果其满足以下条件，则称其为有效子序列 ：
    (sub[0] + sub[1]) % k == (sub[1] + sub[2]) % k == ... == (sub[x - 2] + sub[x - 1]) % k
    返回 nums 的 最长有效子序列 的长度。
    示例:
    输入：nums = [1,2,3,4,5], k = 2
    输出：5
    解释：
    最长有效子序列是 [1, 2, 3, 4, 5] 。
    """

    def maximumLength(self, nums: List[int], k: int) -> int:
        ans = 0
        for m in range(k):
            f = [0] * k
            # 枚举两项之和模k之后的结果为m
            # f[i]表示i结尾的最长子序列的长度 因此f[x] = f[(m - x) % k] + 1
            # 即前后项之和取模后的结果为m，且最后一个数字是x的最长子序列的长度 为f[x]
            for x in nums:
                x %= k
                f[x] = f[(m - x) % k] + 1
            # 比较答案即可
            ans = max(ans, max(f))
        return ans

        # 树形dp求一棵树的直径

    def diameter(self, edges):
        g = [[] for _ in range(len(edges) + 1)]
        for a, b in edges:
            g[a].append(b)
            g[b].append(a)

        res = 0

        def dfs(x, fa):
            nonlocal res
            mx_len = 0  # 最大长度
            # 枚举每个以x为头的最长链条
            for y in g[x]:
                if y != fa:
                    sub_len = dfs(y, x) + 1  # 次大长度
                    res = max(res, sub_len + mx_len)
                    mx_len = max(mx_len, sub_len)
            # 以到x点的最长链条 作为返回值
            return mx_len

        dfs(0, -1)
        return res

    """
    链接: https://leetcode.cn/problems/find-minimum-diameter-after-merging-two-trees/description/
    描述:
    给你两棵 无向 树，分别有 n 和 m 个节点，节点编号分别为 0 到 n - 1 和 0 到 m - 1 。
    给你两个二维整数数组 edges1 和 edges2 ，长度分别为 n - 1 和 m - 1 ，
    其中 edges1[i] = [ai, bi] 表示在第一棵树中节点 ai 和 bi 之间有一条边，edges2[i] = [ui, vi] 表示在第二棵树中节点 ui 和 vi 之间有一条边。    
    你必须在第一棵树和第二棵树中分别选一个节点，并用一条边连接它们。
    请你返回添加边后得到的树中，最小直径 为多少。
    一棵树的 直径 指的是树中任意两个节点之间的最长路径长度。    
    示例:
    输入：edges1 = [[0,1],[0,2],[0,3]], edges2 = [[0,1]]
    输出：3
    解释：
    将第一棵树中的节点 0 与第二棵树中的任意节点连接，得到一棵直径为 3 的树。
    """

    def minimumDiameterAfterMerge(self, edges1: List[List[int]], edges2: List[List[int]]) -> int:
        d1, d2 = self.diameter(edges1), self.diameter(edges2)
        # 选取两棵树的直径中点，连接即可得到合并两棵树后的最小直径 与之前两棵树的直径大小进行比较即可
        # 记住选取后的直径中点 到这棵树的最远距离是直径长度除以2 上取整 所以最后就是两个直径的中点到直径长度的一半(上取整) 再加上添加的一条边
        return max(d1, d2, (d1 + 1) // 2 + (d2 + 1) // 2 + 1)
