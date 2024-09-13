from typing import List
from functools import cache
from math import inf

dirs = [[2, 1], [2, -1], [1, 2], [1, -2], [-2, 1], [-2, -1], [-1, 2], [-1, -2]]
"""
链接: https://leetcode.cn/problems/maximum-number-of-moves-to-kill-all-pawns/
描述: 见链接
提示:
0 <= kx, ky <= 49
1 <= positions.length <= 15
positions[i].length == 2
0 <= positions[i][0], positions[i][1] <= 49
positions[i] 两两互不相同。
输入保证对于所有 0 <= i < positions.length ，都有 positions[i] != [kx, ky] 。
"""
class Solution:
    def maxMoves(self, kx: int, ky: int, positions: List[List[int]]) -> int:
        n = len(positions)
        dis = [[[-1] * 50 for _ in range(50)] for _ in range(n)] # 兵到棋盘上其他位置的最短路

        for i, (px, py) in enumerate(positions):
            d = dis[i]
            q = [(px, py)]
            d[px][py] = 0
            step = 1
            while q:
                tmp = q
                q = []
                for x, y in tmp:
                    for dx, dy in dirs:
                        nx, ny = x + dx, y + dy
                        # 未越界 且没有被访问过
                        if -1 < nx < 50 and -1 < ny < 50 and d[nx][ny] < 0:
                            d[nx][ny] = step
                            q.append((nx, ny))
                step += 1
        
        positions.append([kx, ky])  # 将一开始马的位置加入进去 方便dfs函数进行 不需要特判马的位置

        all_ = (1 << n) - 1  # 还剩下哪些棋子
        @cache  # 参数的意思是 当前位置在position[i] 还有mask个棋子没有吃掉 按照最优策略能够进行的移动次数
        def dfs(i, mask):
            if mask == 0:
                return 0
            odd = (all_ ^ mask).bit_count() % 2 # 被吃掉的棋子数量是奇数还是偶数个 如果是偶数个那就是alice在进行 因此取max 否则就是取min
            x, y = positions[i]  # 马当前位置
            op = min if odd else max
            res = inf if odd else 0
            for j, d in enumerate(dis):
                if (mask >> j) & 1:
                    res = op(res, dfs(j, mask ^ (1 << j)) + d[x][y])
            return res
        
        ans = dfs(n, all_)  # 当前在刚添加进去的一开始马的位置 所有的棋子都需要被吃掉 返回动态规划函数的结果
        dfs.cache_clear()
        return ans
