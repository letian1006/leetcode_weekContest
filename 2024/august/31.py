from collections import Counter
pow10 = [1]
fac = [1]
for i in range(10):
    pow10.append(pow10[-1] * 10)  # 10的幂次
    fac.append(fac[-1] * (i + 1))  # 阶乘



class Solution:
    """
    链接: https://leetcode.cn/problems/find-the-count-of-good-integers/description/

    描述:
    给你两个 正 整数 n 和 k 。
    如果一个整数 x 满足以下条件，那么它被称为 k 回文 整数 。
    x 是一个 回文整数 。x 能被 k 整除。
    如果一个整数的数位重新排列后能得到一个 k 回文整数 ，那么我们称这个整数为 好 整数。比方说，k = 2 ，
    那么 2020 可以重新排列得到 2002 ，2002 是一个 k 回文串，所以 2020 是一个好整数。而 1010 无法重新排列数位得到一个 k 回文整数。
    请你返回 n 个数位的整数中，有多少个 好 整数。
    注意 ，任何整数在重新排列数位之前或者之后 都不能 有前导 0 。比方说 1010 不能重排列得到 101 。

    提示:
    1 <= n <= 10
    1 <= k <= 9
    """
    def countGoodIntegers(self, n: int, k: int) -> int:
        vis = set()
        # 枚举回文数 看看是不是符合要求的
        if n == 1:
            return 9 // k

        def get(cnt):
            # cnt为数字出现的哈希表 比如1200就是cnt[0] = 2, cnt[1] = 1, cnt[2] = 1
            # 这里的计算方法就是 第一位不能是0 所以是(n - cnt['0']) * (fac[n - 1]) 第一部分代表从不是0的数字里面选取一位 后面表示去掉第一位之后剩下的数字可以全排列
            # 然后需要去掉重复的数字 这里的策略就是除以各个数字的个数的全排列数 
            # 假设1有两个 因为1,1 和1，1是一样的 所以需要除以2(1的个数的阶乘) 也就是fac[v] v为1的个数 后面就是所有数字的个数的阶乘
            duplicate = 1
            for v in cnt.values():
                duplicate *= fac[v]
            return (n - cnt['0']) * fac[n - 1] // duplicate

        ans = 0
        half = n // 2
        for ele in range(pow10[half - 1], pow10[half]):
            # 暴力枚举其中的一半
            cur = None
            if n & 1:
                for mid in range(10):
                    cur = str(ele) + str(mid) + str(ele)[::-1]
                    tmp = ''.join(sorted(list(cur)))
                    if tmp in vis or int(cur) % k != 0: # 不重复统计  通过添加排序后的数字来进行去重 之后需要数位完全相同的数字直接跳过就好
                        continue
                    vis.add(tmp)
                    ans += get(Counter(cur))
            else:
                cur = str(ele) + str(ele)[::-1]
                tmp = ''.join(sorted(list(cur)))
                if tmp in vis or int(cur) % k != 0: # 不重复统计
                    continue
                vis.add(tmp)
                ans += get(Counter(cur))
        return ans

res = {}

for n in range(1, 11):
    for k in range(1, 10):
        res[(n, k)] = Solution().countGoodIntegers(n, k)
print(res)