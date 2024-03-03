"""
24-03-02双周赛 两题选手
给出t3和t4的解法 t3是一个dfs 但是没有想清楚
t4是一个很巧妙的状态机dp 也可以使用树形dp 下面补充这两题的写法
"""
from math import inf
from typing import List


class Solution:
    """
    链接: https://leetcode.cn/problems/count-pairs-of-connectable-servers-in-a-weighted-tree-network/description/

    描述:
    给你一棵无根带权树，树中总共有 n 个节点，分别表示 n 个服务器，服务器从 0 到 n - 1 编号。
    同时给你一个数组 edges ，其中 edges[i] = [ai, bi, weighti] 表示节点 ai 和 bi 之间有一条双向边，
    边的权值为 weighti 。再给你一个整数 signalSpeed 。
    如果两个服务器 a ，b 和 c 满足以下条件，那么我们称服务器 a 和 b 是通过服务器 c 可连接的 ：
    a < b ，a != c 且 b != c 。
    从 c 到 a 的距离是可以被 signalSpeed 整除的。
    从 c 到 b 的距离是可以被 signalSpeed 整除的。
    从 c 到 b 的路径与从 c 到 a 的路径没有任何公共边。
    请你返回一个长度为 n 的整数数组 count ，其中 count[i] 表示通过服务器 i 可连接 的服务器对的 数目 。

    示例:
    输入：edges = [[0,1,1],[1,2,5],[2,3,13],[3,4,9],[4,5,2]], signalSpeed = 1
    输出：[0,4,6,6,4,0]
    解释：由于 signalSpeed 等于 1 ，count[c] 等于所有从 c 开始且没有公共边的路径对数目。
    在输入图中，count[c] 等于服务器 c 左边服务器数目乘以右边服务器数目。
    """

    def countPairsOfConnectableServers(self, edges: List[List[int]], signalSpeed: int) -> List[int]:
        n = len(edges) + 1
        g = [[] for _ in range(n)]
        for x, y, w in edges:
            g[x].append([y, w])
            g[y].append([x, w])

        # 这个函数就是计算这个节点的子树中有多少个节点的距离是signalSpeed的倍数
        def dfs(cur, fa, path_sum):
            res = 0 if path_sum % signalSpeed else 1
            for child, wt in g[cur]:
                if child != fa:
                    res += dfs(child, cur, path_sum + wt)
            return res

        ans = [0] * n
        for i, gi in enumerate(g):
            s = 0
            # 查看以i为头的各个子树中 有多少个节点的距离是signalSpeed的倍数
            for j, w in gi:
                now = dfs(j, i, w)
                ans[i] += s * now
                s += now
        return ans

    """
    链接: https://leetcode.cn/problems/find-the-maximum-sum-of-node-values/

    描述:
    给你一棵 n 个节点的 无向 树，节点从 0 到 n - 1 编号。树以长度为 n - 1 下标从 0 开始的二维整数数组 edges 的形式给你，
    其中 edges[i] = [ui, vi] 表示树中节点 ui 和 vi 之间有一条边。
    同时给你一个 正 整数 k 和一个长度为 n 下标从 0 开始的 非负 整数数组 nums ，其中 nums[i] 表示节点 i 的 价值 。
    日增哥哥想 最大化 树中所有节点价值之和。为了实现这一目标，日增哥哥可以执行以下操作 任意 次（包括 0 次）：
    选择连接节点 u 和 v 的边 [u, v] ，并将它们的值更新为：
    nums[u] = nums[u] XOR k
    nums[v] = nums[v] XOR k
    请你返回日增哥哥通过执行以上操作 任意次 后，可以得到所有节点 价值之和 的 最大值 。

    示例:
    输入：nums = [1,2,1], k = 3, edges = [[0,1],[0,2]]
    输出：6
    解释：日增哥哥可以通过一次操作得到最大价值和 6 ：
    - 选择边 [0,2] 。nums[0] 和 nums[2] 都变为：1 XOR 3 = 2 ，数组 nums 变为：[1,2,1] -> [2,2,2] 。
    所有节点价值之和为 2 + 2 + 2 = 6 。
    6 是可以得到最大的价值之和。
    """
    def maximumValueSum(self, nums: List[int], k: int, edges: List[List[int]]) -> int:
        # 这个题目要求我们选择边 然后对边两端进行异或k操作
        # 由于整张图是一个联通的树 我们可以任意选择两个顶点进行操作 因为他们一定有一条唯一的路经相连
        # 在对这条路径上的所有边进行异或操作时候 相当于只对两端的顶点进行了异或操作
        # 那么对应的会出现三种结果
        # 1 两端的顶点都经过了异或操作 再次异或会得到原来的值 因此少了两个异或过k的数
        # 2 两端的顶点之前都没有经过异或操作 因此增加了两个异或过k的数
        # 3 两端的顶点只有一个经过了异或操作 +1 -1抵消了 异或过k的节点数目不变
        # 因此整个问题变成了从nums中选择偶数个数字进行异或k操作 得到的最大价值和是多少
        # 所以变成一个状态机dp问题，从前i个数选择奇数个数字 和 偶数个数字进行异或k 然后得到的最大价值和
        # 最后的答案就是f[n][0]表示前n个数选择偶数个数字异或上k 得到的最大价值和
        f0, f1 = 0, -inf  # 一开始的状态 一个数字也没有 所以选偶数个数字异或k得到的最大价值和是0 选奇数个数字异或k得到的最大价值和是负无穷
        for i in nums:
            # 状态转移方程 从选奇数个数字转换到选偶数个数字 以及从选偶数个数字转换到选奇数个数字 的状态转移方程
            # f0 + i表示直接选择这个数字 不进行异或操作 所以还是选偶数个数字
            # f1 + (i ^ k)表示选择这个数字进行异或操作 从选奇数个数字转换到选偶数个数字
            # f1 + i表示直接选择这个数字 不进行异或操作 所以还是选奇数个数字
            # f0 + (i ^ k)表示选择这个数字进行异或操作 从选偶数个数字转换到选奇数个数字
            f0, f1 = max(f0 + i, f1 + (i ^ k)), max(f1 + i, f0 + (i ^ k))  
        return f0


        pass
