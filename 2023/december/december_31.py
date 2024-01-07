"""
12月31号的周赛 起晚了没有参加
第378场周赛
23年的最后一次周赛 参与虚拟竞赛 最后一个大模拟没有做出来
链接:https://leetcode.cn/contest/weekly-contest-378/
"""
from itertools import accumulate
from typing import List


class Solution:
    def canMakePalindromeQueries(self, s: str, queries: List[List[int]]) -> List[bool]:
        """
        给你一个长度为 偶数 n ，下标从 0 开始的字符串 s 。
        同时给你一个下标从 0 开始的二维整数数组 queries ，其中 queries[i] = [ai, bi, ci, di] 。
        对于每个查询 i ，你需要执行以下操作：
        将下标在范围 0 <= ai <= bi < n / 2 内的 子字符串 s[ai:bi] 中的字符重新排列。
        将下标在范围 n / 2 <= ci <= di < n 内的 子字符串 s[ci:di] 中的字符重新排列。
        对于每个查询，你的任务是判断执行操作后能否让 s 变成一个 回文串 。
        每个查询与其他查询都是 独立的 。
        请你返回一个下标从 0 开始的数组 answer ，如果第 i 个查询执行操作后，可以将 s 变为一个回文串，那么 answer[i] = true，否则为 false 。
        子字符串 指的是一个字符串中一段连续的字符序列。
        s[x:y] 表示 s 中从下标 x 到 y 且两个端点 都包含 的子字符串。
        链接:https://leetcode.cn/problems/palindrome-rearrangement-queries/description/
        """

        """
        输入：s = "abcabc", queries = [[1,1,3,5],[0,2,5,5]]
        输出：[true,true]
        解释：这个例子中，有 2 个查询：
        第一个查询：
        - a0 = 1, b0 = 1, c0 = 3, d0 = 5
        - 你可以重新排列 s[1:1] => abcabc 和 s[3:5] => abcabc 。
        - 为了让 s 变为回文串，s[3:5] 可以重新排列得到 => abccba 。
        - 现在 s 是一个回文串。所以 answer[0] = true 。
        第二个查询：
        - a1 = 0, b1 = 2, c1 = 5, d1 = 5.
        - 你可以重新排列 s[0:2] => abcabc 和 s[5:5] => abcabc 。
        - 为了让 s 变为回文串，s[0:2] 可以重新排列得到 => cbaabc 。
        - 现在 s 是一个回文串，所以 answer[1] = true 。
        """
        # 基本思路分类讨论 先拆分后半段字符串 然后倒转和前半段对齐 方便我们思考
        n = len(s)
        half = n >> 1
        t = s[half:][::-1]
        s = s[:half]
        # 先求字母出现的频次前缀和
        sum_s, sum_t = [[0 for _ in range(26)]], [[0 for _ in range(26)]]
        for i in range(half):
            sum_s.append(sum_s[-1][:])
            sum_s[-1][ord(s[i]) - ord('a')] += 1
            sum_t.append(sum_t[-1][:])
            sum_t[-1][ord(t[i]) - ord('a')] += 1
        # 再求字符串不相等的前缀和
        sum_ne = list(accumulate([x != y for x, y in zip(s, t)], initial=0))

        def get_fre(sm, l, r):
            # 得到l-r区间内字符的频率
            return [sm[r + 1][i] - sm[l][i] for i in range(26)]

        def sub(sum_s, l1, r1, sum_t, l2, r2):
            # 减去sum_t的字符频率
            cur_s = [sum_s[r1 + 1][i] - sum_s[l1][i] for i in range(26)]
            cur_t = [sum_t[r2 + 1][i] - sum_t[l2][i] for i in range(26)]
            res = [0] * 26
            for i in range(26):
                if cur_s[i] - cur_t[i] < 0:
                    return None
                res[i] = cur_s[i] - cur_t[i]
            return res

        def check(l1, r1, l2, r2, sum_s, sum_t):
            # 两个区间的三种情况 讨论一下
            # 首先讨论两个区间最左边和最右边不能有不同的字符 如果有不同的字符 但是我们又不能重新排列这段字符 那么就不可能构成回文串
            # 直接返回False
            if sum_ne[l1] > 0 or sum_ne[half] - sum_ne[max(r1, r2) + 1] > 0:
                return False
            if r2 <= r1:
                # 一个区间被另一个区间包含
                # 此时只要考虑大区间的字符频率是不是和对应的另一个字符串的字符频率相等
                # 这样的话 我们就可以通过重新排列让这一段相等
                if get_fre(sum_s, l1, r1) != get_fre(sum_t, l1, r1):
                    return False
            elif r1 < l2:
                # 两个区间不相交
                if sum_ne[l2] - sum_ne[r1 + 1] != 0 or get_fre(sum_s, l1, r1) != get_fre(sum_t, l1, r1) or get_fre(
                        sum_s, l2, r2) != get_fre(sum_t, l2, r2):
                    return False
            else:
                # 两个区间交叉的情况 此时需要将一个区间减去另一个区间的字符频率
                # 然后看看剩下的字符频率是不是相等 也即是优先满足不能变动的区间 然后看看剩下的可以自由排列的部分是不是能够
                # 通过重新排列变成回文串 也就是字符频率相等
                res1, res2 = sub(sum_s, l1, r1, sum_t, l1, l2 - 1), sub(sum_t, l2, r2, sum_s, r1 + 1, r2)
                if res1 is None or res2 is None or res1 != res2:
                    return False
            return True

        ans = [False] * len(queries)
        for i, (l1, r1, l, r) in enumerate(queries):
            l2, r2 = n - 1 - r, n - 1 - l
            # 通过交换参数的位置 简化代码逻辑 这样我们只需要讨论三种情况即可 因为我们已经保证了 l1 < l2
            # 这样的话 我们只有三种情况 第一是区间包含 第二是区间不相交 第三是区间相交
            #
            ans[i] = check(l1, r1, l2, r2, sum_s, sum_t) if l1 < l2 else check(l2, r2, l1, r1, sum_t, sum_s)
        return ans
