from typing import List

class Solution:
    # 链接: https://leetcode.cn/problems/shortest-distance-after-road-addition-queries-ii/
    def shortestDistanceAfterQueries(self, n: int, queries: List[List[int]]) -> List[int]:
        fa = list(range(n - 1))

        # 将n个点形成的n-1条线段看成 n-1个连通块
        # 每次添加一个query就相当于将编号从l,l+1 ... r-1的线段合并成一个块
        # 每次添加完询问后剩下多少个联通块 就相当于最短需要走多少步才能最后到达终点
        # 这里之所以能够使用并查集 是因为queries[i][0] < queries[j][0] < queries[i][1] < queries[j][1]这个条件
        # 所以不会有交叉的询问 我们只需要关注有多少个连通块即可
        
        def find(x):
            if fa[x] != x:
                fa[x] = find(fa[x])
            return fa[x]
        
        def union(x, y):
            fx, fy = find(x), find(y)
            if fx != fy:
                fa[fx] = fy
        
        cnt = n - 1  # 一开始剩下的连通块数目 n - 1
        ans = []

        for l, r in queries:
            cur = find(l)  # 先找最左边那个线段的所在连通块的父亲
            while cur < r - 1:
                union(cur, cur + 1) 
                # 每次合并
                cur = find(cur + 1)  # 跳过中途的连通块的其他节点 直接往后走 降低复杂度
                cnt -= 1  # 合并一次减少一个连通块的数量
            ans.append(cnt)
        return ans