


from bisect import bisect_left


class Solution:
    """
    链接: https://leetcode.cn/problems/find-the-largest-palindrome-divisible-by-k/description/
    描述:  
        给你两个 正整数 n 和 k。
        如果整数 x 满足以下全部条件，则该整数是一个 k 回文数：
        x 是一个回文数。
        x 可以被 k 整除。
        以字符串形式返回 最大的  n 位 k 回文数。
        注意，该整数 不 含前导零。
    提示:
        1 <= n <= 105
        1 <= k <= 9
    """
    def largestPalindrome(self, n: int, k: int) -> str:
        # 只需要在每个位置上填数字的时候注意模k减少状态个数即可解决这个问题
        pow10 = [1]
        for i in range(1, n + 1):
            pow10.append(pow10[-1] * 10 % k)
        vis = [[False] * (k + 1) for _ in range(n + 1)]  # 状态访问记录表
        m = (n + 1) // 2 # 上取整作为上界 比如n长度为4 需要枚举到下标2 长度为奇数5的话需要枚举到下标3 枚举一半即可
        ans = [''] * n
        # 类似于图的遍历
        def dfs(i, j):
            if i == m:
                return j == 0
            vis[i][j] = True  # 标记访问
            for cur in range(9, -1, -1):
                # 枚举第i位 以及n-i-i位置上的数字
                j2 = None
                if n % 2 and i == m - 1:  # 如果是正中间
                    j2 = (j + cur * pow10[i]) % k
                else:
                    j2 = (j + cur * pow10[i] + cur * pow10[n-1-i]) % k

                if not vis[i+1][j2] and dfs(i + 1, j2):  # 贪心枚举
                    if n % 2 and i == n // 2:
                        ans[i] = str(cur)
                    else:
                        ans[i] = ans[n-1-i] = str(cur)  # 记录答案
                    return True
            return False
        
        dfs(0, 0)
        return ''.join(ans)
    
    """
    链接: https://leetcode.cn/problems/count-substrings-that-satisfy-k-constraint-ii/
    描述:
        给你一个 二进制 字符串 s 和一个整数 k。
        另给你一个二维整数数组 queries ，其中 queries[i] = [li, ri] 。
        如果一个 二进制字符串 满足以下任一条件，则认为该字符串满足 k 约束：
        字符串中 0 的数量最多为 k。字符串中 1 的数量最多为 k。
        返回一个整数数组 answer ，其中 answer[i] 表示 s[li..ri] 中满足 k 约束 的 
        子字符串的数量。
    提示:
        1 <= s.length <= 105
        s[i] 是 '0' 或 '1'
        1 <= k <= s.length
        1 <= queries.length <= 105
        queries[i] == [li, ri]
        0 <= li <= ri < s.length
        所有查询互不相同
    """
    def countKConstraintSubstrings(self, s: str, k: int, queries: List[List[int]]) -> List[int]:

        """
        前缀和加上二分加上滑动窗口
        1.对于这个题目 每个下标记作r 都有一个最远的l下标，这中间的下标对于r都是合法的子串
        2.可以通过滑动窗口的方式计算每个r下标对应的l下标 
        3.回答询问L-R区间有多少符合要求的子串，分为两个部分，第一个是l小于L的，可以通过等差数列求和的方式得到这部分答案
        4.对于另一部分，可以通过前缀和每个下标计算一个前缀和数组，计算r-l的前缀和，这就是后面那部分的数组
        5.由于l是一个单调的数组 因此可以直接二分得到这个位置
        """
        n = len(s)
        left = [-1] * n
        pre = [0]  # 前缀和数组
        l, r = 0, 0  # 左右指针
        cnt = [0, 0]
        while r < n:
            cnt[ord(s[r]) & 1] += 1
            while cnt[0] > k and cnt[1] > k:
                cnt[ord(s[l]) & 1] -= 1
                l += 1
            left[r] = l
            pre.append(pre[-1] + (r - l + 1))  # r位置对应的合法位置l 再往左就不合法了
            r += 1
        ans = []
        for L, R in queries:
            index =  bisect_left(left, L, L, R + 1)  # L-R范围内第一个小于L的位置
            ans.append((index - L + 1) * (index - L) // 2 + (pre[R + 1] - pre[index]))
        return ans
 
