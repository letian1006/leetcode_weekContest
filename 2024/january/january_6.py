"""
121场双周赛
三题选手 t3没有做出 t4数位dp耗时过长
周赛链接:https://leetcode.cn/contest/biweekly-contest-121/
"""


class Solution:
    # 链接:https://leetcode.cn/problems/minimum-number-of-operations-to-make-x-and-y-equal/description/
    def minimumOperationsToMakeEqual(self, x: int, y: int) -> int:
        """
        给你两个正整数 x 和 y 。
        一次操作中，你可以执行以下四种操作之一：
        如果 x 是 11 的倍数，将 x 除以 11 。
        如果 x 是 5 的倍数，将 x 除以 5 。
        将 x 减 1 。
        将 x 加 1 。
        请你返回让 x 和 y 相等的 最少 操作次数。
        思路bfs
        """
        if x < y:
            # 如果x小于y 那么我只能通过操作4 不断加上1 来使得x等于y
            return y - x
        ans = x - y  # 通过减1的操作次数 得到y 这就是本题答案的上限
        vis = [False] * (x + x - y + 1)  # vis数组开这么大的原因是 我们最多增加x-y次操作 就可以得到答案 因此x最大也就是x+x-y
        q = [x]
        step = 0

        def add(val):
            if not vis[val]:
                vis[val] = True
                q.append(val)

        while True:
            tmp = q
            q = []
            for v in tmp:
                if v == y:
                    return min(step, ans)
                if v % 11 == 0:
                    add(v // 11)
                if v % 5 == 0:
                    add(v // 5)
                add(v - 1)
                add(v + 1)
            step += 1
