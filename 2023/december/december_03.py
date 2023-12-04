"""
周赛一题选手 后面补上三个题目
"""
from collections import Counter
from itertools import pairwise

from typing import List

MOD = 10 ** 9 + 7
MX = 10 ** 5
fac = [0] * MX
fac_inv = [0] * MX
fac[0] = 1
for i in range(1, MX):
    fac[i] = fac[i - 1] * i % MOD
fac_inv[MX - 1] = pow(fac[MX - 1], MOD - 2, MOD)

for i in range(MX - 2, -1, -1):
    # 逆元的递推 求出最后一个往前递推 也就是求出fac_inv[MX-2] 然后求出fac_inv[MX-3] 以此类推
    fac_inv[i] = fac_inv[i + 1] * (i + 1) % MOD

def comb(n, k):
    return fac[n] * fac_inv[k] % MOD * fac_inv[n - k] % MOD
class Solution:
    """
    链接:https://leetcode.cn/problems/count-complete-substrings/description/
    给你一个下标从 0 开始的整数数组 coins，表示可用的硬币的面值，以及一个整数 target 。
    如果存在某个 coins 的子序列总和为 x，那么整数 x 就是一个 可取得的金额 。
    返回需要添加到数组中的 任意面值 硬币的 最小数量 ，使范围 [1, target] 内的每个整数都属于 可取得的金额 。
    数组的 子序列 是通过删除原始数组的一些（可能不删除）元素而形成的新的 非空 数组，删除过程不会改变剩余元素的相对位置。
    """

    def minimumAddedCoins(self, coins: List[int], target: int) -> int:
        # 归纳法 假设目前已经可以取得[0, s-1]的所有金额
        # 这个时候添加一个新的数字x 可以让我们得到[x, x+s-1]之间的所有金额
        # 我们x进行讨论，看看是否能将这两个区间合并 首先是可以合并的情况 也就是 s-1 >= x-1 即s >= x
        # 否则我们就要添加一个数字 来弥补这个缺口 贪心地思考这个问题 我们可以添加数字 s
        # 这个时候我们可以得到的数字金额范围最大 可以得到[0, 2s-1]的所有金额
        # 我们要让s-1 >= target 也就是说s > target 即可 那么进入循环的条件就是 s <= target
        coins.sort()  # 从大到小添加硬币面值 保证最大的面值最后添加 防止出现遗漏
        i, s = 0, 1
        ans = 0
        while s <= target:
            if i < len(coins) and coins[i] <= s:
                s += coins[i]
                i += 1
            else:
                s *= 2
                ans += 1
        return ans

    """
    https://leetcode.cn/problems/count-complete-substrings/description/
    给你一个字符串 word 和一个整数 k 。
    如果 word 的一个子字符串 s 满足以下条件，我们称它是 完全字符串：
    s 中每个字符 恰好 出现 k 次。
    相邻字符在字母表中的顺序 至多 相差 2 。也就是说，s 中两个相邻字符 c1 和 c2 ，它们在字母表中的位置相差 至多 为 2 。
    请你返回 word 中 完全 子字符串的数目。
    子字符串 指的是一个字符串中一段连续 非空 的字符序列。
    """

    def countCompleteSubstrings(self, word: str, k: int) -> int:
        # 按照题目的意思 有两个条件 第二个条件 也就是相邻字符的差值不超过2
        # 将这个字符串分割为多个段 每个段内只要满足第一个条件即可 也就是每个字符出现k次
        # 第一个条件我们使用分组循环来完成这个任务 后面我们使用滑动窗口来求这个答案 最后累加答案即可
        def get(s):
            # 处理一个子串 其中有多少符合要求的子字符串
            res = 0
            for m in range(1, 27):
                # 代表窗口的大小 我们选取m个字母能够 得到多少答案
                size = m * k
                # 窗口的大小超过字符串的长度 直接返回
                if size > len(s):
                    return res
                cnt = Counter(s[0:size])  # 统计词频
                k_cnt = sum(1 for val in cnt.values() if val == k)
                # 看看是不是有m个字母出现了k次 我们枚举的是m个字母 如果都恰好出现了k次 那么证明这就是一个符合题目要求的子串
                if k_cnt == m:
                    res += 1
                for in_, out in zip(s[size:], s):
                    if cnt[in_] == k:
                        k_cnt -= 1
                    cnt[in_] += 1
                    if cnt[in_] == k:
                        k_cnt += 1
                    if cnt[out] == k:
                        k_cnt -= 1
                    cnt[out] -= 1
                    if cnt[out] == k:
                        k_cnt += 1
                    if k_cnt == m:
                        res += 1
            return res

        n = len(word)
        i = ans = 0
        while i < n:
            st = i
            i += 1
            while i < n and abs(ord(word[i]) - ord(word[i - 1])) < 3:
                i += 1
            ans += get(word[st:i])
        return ans

    """
    链接：https://leetcode.cn/problems/count-the-number-of-infection-sequences/description/
    给你一个整数 n 和一个下标从 0 开始的整数数组 sick ，数组按 升序 排序。
    有 n 位小朋友站成一排，按顺序编号为 0 到 n - 1 。
    数组 sick 包含一开始得了感冒的小朋友的位置。如果位置为 i 的小朋友得了感冒，
    他会传染给下标为 i - 1 或者 i + 1 的小朋友，前提 是被传染的小朋友存在且还没有得感冒。每一秒中， 至多一位 还没感冒的小朋友会被传染。
    经过有限的秒数后，队列中所有小朋友都会感冒。感冒序列 指的是 所有 一开始没有感冒的小朋友最后得感冒的顺序序列。请你返回所有感冒序列的数目。
    由于答案可能很大，请你将答案对 1e9 + 7 取余后返回。
    注意，感冒序列 不 包含一开始就得了感冒的小朋友的下标。
    """
    def numberOfSequence(self, n: int, sick: List[int]) -> int:
        # 这一题牵涉到组合数学和乘法逆元的知识 记得逆元就是pow(a, mod-2, mod)
        # 首先考虑相邻的两个小朋友之间的感染序列有多少个 按照题目的意思 我们可以抽象出一个序列 也就是LRL等
        # 表示这一位是从左边感染呢 还是从右边感染 比如n == 5 初始0 和 4位置已经被感染 那么我们就有三个空位
        # 此时有四种感染序列 也就是 LLR LRR LRL LRR 也就是 2 ^ (3 - 1)种方案
        # 再考虑多个连续的段 这些段之间相互不干扰 完全独立 假设第一段有k1个空位 第二段有k2个空位
        # 我们就有 comb(k1 + k2, k1) * comb(k1, k1) * 2 ^ (k2 - 1) * 2 ^ (k1 - 1)种方案
        # 前两个组合数代表我从中选取k1个空位放置第一段的感染序列 第三个组合数代表我从中选取k2个空位放置第二段的感染序列
        # 然后每段组合数内部又可以有2 ^ (k - 1)种方案
        """
        预处理组合数 也就是阶乘和其逆元
        """
        m = len(sick)
        tot = n - m  # 还剩多少个位置需要感染
        # 两端的小朋友只有一种感染方法 也就是q全部为L或者全部为R 所以只有组合数
        e = 0  # 最后答案2的底数
        ans = comb(tot, sick[0]) * comb(tot - sick[0], n - 1 - sick[-1]) % MOD
        tot -= sick[0] + n - 1 - sick[-1]  # 少了这么多空位
        for p, q in pairwise(sick):
            # p和q之间有多少个空位
            k = q - p - 1
            if k != 0:
                ans = ans * comb(tot, k) % MOD
                e += k - 1
                tot -= k
        return ans * pow(2, e, MOD) % MOD
