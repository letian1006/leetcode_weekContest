"""
周赛379
这次周赛罚时比较多 很难上分
第四题直接定义状态也不是那么简单 参看灵神的题解
周赛链接地址:https://leetcode.cn/contest/weekly-contest-379/
三题选手 t4未能做出
"""
from functools import cache


# 链接:https://leetcode.cn/problems/maximize-the-number-of-partitions-after-operations/description/

class Solution:
    def maxPartitionsAfterOperations(self, s: str, k: int) -> int:
        """
        给你一个下标从 0 开始的字符串 s 和一个整数 k。
        你需要执行以下分割操作，直到字符串 s 变为 空：
        选择 s 的最长前缀，该前缀最多包含 k 个 不同 字符。
        删除 这个前缀，并将分割数量加一。如果有剩余字符，它们在 s 中保持原来的顺序。
        执行操作之 前 ，你可以将 s 中 至多一处 下标的对应字符更改为另一个小写英文字母。
        在最优选择情形下改变至多一处下标对应字符后，用整数表示并返回操作结束时得到的最大分割数量。
        """
        n = len(s)

        # 缓存
        @cache
        def dfs(i, mask, changed):
            # i代表当前位置 mask代表当前的状态 changed代表是否已经修改过字符
            if i == n:
                return 1
            cur_digit = ord(s[i]) - ord('a')
            bit = 1 << cur_digit
            new_mask = mask | bit
            res = 0
            if new_mask.bit_count() > k:
                # 如果之前的状态加上当前字符 那么这个字符只能放在一个新的分组里面
                res = dfs(i + 1, bit, changed) + 1
            else:
                # 否则的话就必须在同一个分组当中
                res = dfs(i + 1, new_mask, changed)
            # 枚举修改的字符
            if not changed:
                for char in range(26):
                    # 跳过和当前字符相同的字符 因为这样的话就没有意义了 不算修改
                    if char == cur_digit:
                        continue
                    bit = 1 << char
                    new_mask = mask | bit
                    if new_mask.bit_count() > k:
                        res = max(res, dfs(i + 1, bit, True) + 1)
                    else:
                        res = max(res, dfs(i + 1, mask | bit, True))
            return res
        ans = dfs(0, 0, False)
        dfs.cache_clear()
        return ans
