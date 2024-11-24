from typing import List
from collections import defaultdict

class Solution:
    # https://leetcode.cn/contest/weekly-contest-425/problems/maximize-sum-of-weights-after-edge-removals/description/
    # 树形dp 加上贪心
    def maximizeSumOfWeights(self, edges: List[List[int]], k: int) -> int:
        g = defaultdict(list)
        for a, b, w in edges:
            g[a].append((b, w))
            g[b].append((a, w))


        # 子树向父节点返回两个信息 父子节点之间的边不选的话 最大边权是多少 父子节点之间的边选的话最大边权是多少
        def dfs(cur, fa):
            s = 0
            inc = [] # 增量
            for nex, w in g[cur]:
                if nex != fa:
                    nc, c = dfs(nex, cur)
                    s += nc
                    d = c + w - nc  # 这里代表cur节点和nex节点之间的边选的话 能够带来的增量收益是多少 相对于不选来看
                    if d > 0:
                        inc.append(d)
            
            inc.sort(reverse=True)
            # 最后返回的是cur节点和fa节点之间的边选或不选能得到的最大边权收益 如果不选就可以选择k个边 否则最多只能选择k-1条边
            # 向父节点返回
            return s + sum(inc[:k]), s + sum(inc[:k - 1])

        return max(dfs(0, -1))