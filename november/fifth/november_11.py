from functools import lru_cache

MOD = 10 ** 9 + 7


class Solution:
    """
    给你两个正整数 n 和 limit
    请你将 n 颗糖果分给 3 位小朋友，确保没有任何小朋友得到超过 limit 颗糖果，请你返回满足此条件下的 总方案数
    链接:https://leetcode.cn/contest/biweekly-contest-117/problems/distribute-candies-among-children-ii/
    """

    def distributeCandies(self, n: int, limit: int) -> int:
        # 这个题目还可以通过容斥原理来做
        # 首先想到隔板法，由于允许给小朋友分配0颗糖果 所以是在n+2个位置中选2个位置来放隔板 从而得到三堆糖果
        # 不考虑limit的情况下 一共有C(n+2, 2)种情况
        # a小朋友超过limit A C(n-(limit+1)+2, 2) 我们先选择limit加1颗糖果给a小朋友 然后剩下的使用隔板法即可 下面同理
        # b小朋友超过limit B C(n-(limit+1)+2, 2)
        # c小朋友超过limit C C(n-(limit+1)+2, 2)
        # a和b超过limit AB C(n-2*(limit+1)+2, 2)
        # a和c超过limit AC C(n-2*(limit+1)+2, 2)
        # b和c超过limit BC C(n-2*(limit+1)+2, 2)
        # a和b和c都超过limit ABC C(n-3*(limit+1)+2, 2)
        # 结果是 C(n+2, 2) - A - B - C + AB + AC + BC - ABC
        # 即 C(n+2, 2) - 3 * C(n-(limit+1)+2, 2) + 3 * C(n-2*(limit+1)+2, 2) - C(n-3*(limit+1)+2, 2)

        ans = 0
        # 枚举一个人拿多少
        for i in range(min(limit + 1, n + 1)):
            # 剩下两个人拿的总数就是rest个
            rest = n - i
            if rest <= limit:
                # 此时一个小朋友拿0-rest个糖果都是可以的
                ans += rest + 1
            elif rest <= 2 * limit:
                # 这个时候想x + y = rest 且 x <= limit y <= limit的图像整数点的个数
                # 也就是x 从limit到rest-limit这之间的整数点的个数
                ans += limit - (rest - limit) + 1
        return ans

    """
    给你一个整数 n
    如果一个字符串s只包含小写英文字母，且将s的字符重新排列后，新字符串包含子字符串 "leet" ，那么我们称字符串s是一个好字符串
    比方说:
    字符串 "lteer" 是好字符串，因为重新排列后可以得到 "leetr" 。
    "letl" 不是好字符串，因为无法重新排列并得到子字符串 "leet" 。
    请你返回长度为n的好字符串总数目。
    由于答案可能很大，将答案对1e9 + 7取余后返回。
    子字符串是一个字符串中一段连续的字符序列。
    链接:https://leetcode.cn/problems/number-of-strings-which-can-be-rearranged-to-contain-substring/description/
    """

    def stringCount(self, n: int) -> int:
        """
        这个题目还可以使用容斥原理 也就是上面的方法来做 也就是合法的方案数目减去不合法的方案数目
        具体的A B C集合的定义 以及最后的结果的计算方式和上面的题目是一样的
        """

        # 其实是分组背包的题目 每个下标至少选一个字符 最后的结果至少包含一个l 两个e 一个t
        # 这样的方案数是多少 分组背包 一个下标就是一个组
        @lru_cache(None)
        def dfs(i, l, e, t):
            if i == 0:
                return 1 if l == e == t == 0 else 0
            res = dfs(i - 1, 0, e, t)  # 选l
            res += dfs(i - 1, l, max(e - 1, 0), t)  # 选e
            res += dfs(i - 1, l, e, 0)  # 选t
            res += dfs(i - 1, l, e, t) * 23  # 选其他
            return res % MOD
        # 递归的入口 从后往前递推 递推n步 所以i==0的时候就退出了递归
        ans = dfs(n, 1, 2, 1)
        dfs.cache_clear()
        return ans
