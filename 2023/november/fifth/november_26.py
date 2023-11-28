"""
11-26的周赛 两题选手 t3 和 t4
链接：https://leetcode.cn/contest/weekly-contest-373/
代码如下
"""
from collections import Counter
from itertools import count

from typing import List


class Solution:
    """
    链接：https://leetcode.cn/problems/make-lexicographically-smallest-array-by-swapping-elements/
    给你一个下标从 0 开始的 正整数 数组 nums 和一个 正整数 limit 。
    在一次操作中，你可以选择任意两个下标 i 和 j，如果 满足 |nums[i] - nums[j]| <= limit ，则交换 nums[i] 和 nums[j] 。
    返回执行任意次操作后能得到的 字典序最小的数组 。
    如果在数组 a 和数组 b 第一个不同的位置上，数组 a 中的对应字符比数组 b 中的对应字符的字典序更小，则认为数组 a 就比数组 b 字典序更小。例如，数组 [2,10,3] 比数组 [10,2,3]
    字典序更小，下标 0 处是两个数组第一个不同的位置，且 2 < 10 。
    """

    def lexicographicallySmallestArray(self, nums: List[int], limit: int) -> List[int]:
        # 贪心的思考 nums能不能排列成排序之后的样子 那样的话就是最小的字典序
        # 每一个差距小于limit的数字都是一个联通块 可以随意交换 这样可以按照排序后的数字 依次填到他们原来的位置上
        # 比如limit = 2 数组为 4 3 2 1 32 34 33 5
        # 就可以排列成 1 2 3 4 32 33 34 5的最小字典序数组 1 2 3 4 5是一个连通块 可以按照顺序排列然后按照顺序排列在下标 0 1 2 3 7上
        # 另一个连通块同理 注意这里写一个分组循环 分别做不同的是
        n = len(nums)
        data = sorted(zip(nums, range(n)))
        ans = [0] * n
        i = 0
        while i < n:
            st = i
            i += 1
            while i < n and data[i][0] - data[i - 1][0] <= limit:
                i += 1
            idx = sorted(i for _, i in data[st:i])
            for index, (x, _) in zip(idx, data[st:i]):
                ans[index] = x
        return ans

    """
    链接：https://leetcode.cn/problems/count-beautiful-substrings-ii/description/
    给你一个字符串 s 和一个正整数 k 。
    用 vowels 和 consonants 分别表示字符串中元音字母和辅音字母的数量。
    如果某个字符串满足以下条件，则称其为 美丽字符串 ：
    vowels == consonants，即元音字母和辅音字母的数量相等。
    (vowels * consonants) % k == 0，即元音字母和辅音字母的数量的乘积能被 k 整除。
    返回字符串 s 中 非空美丽子字符串 的数量。
    子字符串是字符串中的一个连续字符序列。
    英语中的 元音字母 为 'a'、'e'、'i'、'o' 和 'u' 。
    英语中的 辅音字母 为除了元音字母之外的所有字母。
    """

    def beautifulSubstrings(self, s: str, k: int) -> int:
        """
        考虑题目要求 即长度为L的字符串若是能够满足要求的话 那么L * L = 4 * k
        假设d为L的最小因子 即L = d * x 那么d * x * d * x = 4 * k
        所以d应该满足 d * d = 4 * k 因为k比较小 我们可以枚举出这个d
        就可以得到 L%d == 0的长度才可以满足要求
        """
        for i in count(1):
            if i * i % (4 * k) == 0:
                k = i
                break
        ans = 0
        # 现在需要满足两个要求
        # 考虑下标i和j 那么s[i]到s[j]的元音辅音数量相等
        # 以及(j - i) % k == 0 即i和j关于k同余 因此我们考虑两数之和
        # 即前缀和加哈希表的套路
        pre = [0]
        for c in s:
            x = 1 if c in 'aeiou' else -1
            pre.append(pre[-1] + x)
        cnt = Counter()
        for i, c in enumerate(pre):
            tar = (c, i % k)
            ans += cnt[tar]
            cnt[tar] += 1
        return ans
