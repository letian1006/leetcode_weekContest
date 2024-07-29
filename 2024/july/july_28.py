"""
周赛t3 和t4 没有做出 给出如下解答
周赛链接: https://leetcode.cn/contest/weekly-contest-408/
"""

from typing import List

class Solution:
    """
    链接: https://leetcode.cn/problems/count-the-number-of-substrings-with-dominant-ones/description/

    描述: 
    给你一个二进制字符串 s。请你统计并返回其中 1 显著 的 子字符串的数量。
    如果字符串中 1 的数量 大于或等于 0 的数量的 平方，则认为该字符串是一个 1 显著 的字符串 。

    示例:
    输入: s = "00011"
    输出: 5
    i	j	s[i..j]	0 的数量	1 的数量
    3	3	1	    0	        1
    4	4	1	    0	        1
    2	3	01	    1	        1
    3	4	11	    0	        2
    2	4	011	    1	        2
    数据范围 1 <= s.length <= 4 * 104
            s 仅包含字符 '0' 和 '1'。
    """
    def numberOfSubstrings(self, s: str) -> int:
        # 通过数据范围猜测复杂度 可能在O(n) O(nlogn) o(nsqrt(n)) o(nlog^2(n))等
        
        n = len(s)
        zero_id = [i for i, c in enumerate(s) if c == '0']
        tot1 = n - len(zero_id)  # 除去字符串s中的0，目前还剩多少个1
        zero_id.append(n)  # 哨兵方便处理011111的这种情况
        ans = i = 0 
        for left, c in enumerate(s):
            # 以left为子串左端点 枚举右边0的位置
            for k in range(i, len(zero_id) - 1):
                
                cnt0 = k - i + 1
                if cnt0 * cnt0 > tot1:
                    break
                p = zero_id[k]  # left右边第一个0的下标
                q = zero_id[k+1]  # left右边第二个0的下标 这个时候就是哨兵发挥作用的时候 如果是形如101111的这种情况 没有第二个0我们也可以用n来当作第二个0的位置
                cnt1 = zero_id[k] - left + 1 - cnt0
                if cnt0 * cnt0 <= cnt1:  # 核心优化 如果0的个数的平方 已经超过剩余1的个数 可以提前退出 这就保证了整个时间复杂度是n*sqrt(n)
                    ans += q - p  # 这个时候p 和 q直接的位置都是合法的
                else:
                    # 这个时候需要补充1的个数 从p到q下标中扣除不足的部分 这样cnt1的数量才能大于等于cnt0的平方
                    # 注意要与0做大小比较 这个是因为p和q之间的1就算全部补充上也可能不够 也就是从p位置到q位置 没有一个是合法的
                    # 这个时候ans不变
                    ans += max(0, q - p - (cnt0 * cnt0 - cnt1))
            
            # 最后处理全部是1的这种情况
            if c == '0':
                # left位置上的数字是0 以这个地方为左端点不可能出现全是1的子串
                # 后续枚举left时候 这个位置上的0跑到了left的左边 我们不再考虑 因此将i += 1 i表示的是zero_id此时枚举到的位置
                i += 1
            else:
                ans += zero_id[i] - left  # 这个位置上是1 所以从left 到 zero_id[i]位置的下标都是合法的 全部是1
                # 即11110这种情况 left枚举到0位置 zero_id[i]等于4 此时以0下标为左端点的全1合法子串包括 1 11 111 1111正好4个(4 - 0 即 zero_id[i] - left)
                tot1 -= 1 # 消耗掉一个1
        return ans
    
    """
    链接: https://leetcode.cn/problems/check-if-the-rectangle-corner-is-reachable/
    """
    def canReachCorner(self, X: int, Y: int, circles: List[List[int]]) -> bool:
        n = len(circles)
        fa = list(range(n + 2))
        # 注意这个题目需要加上前提 所有圆的圆心都要在矩形内
        # 矩形的左边和上边看作一个集合 右边和下边看作一个集合 每个圆看作一个集合
        # 最后经过并查集合并看看 左边和上边代表的集合和右边和下边所在的集合是不是联通的
        # 如果是联通的 那么从左下角到右上角之间是不存在路径符合题意的

        def find(i):
            if fa[i] != i:
                fa[i] = find(fa[i])
            return fa[i]
        
        def union(i, j):
            fi, fj = find(i), find(j)
            if fi != fj:
                fa[fi] = fj

        for i, (x, y, r) in enumerate(circles):
            if x <= r or y + r >= Y:
                union(i, n)
            if y <= r or x + r >= X:
                union(i, n + 1)
            for j in range(i + 1, n):
                xj, yj, rj = circles[j]
                # 圆心之间的距离小于半径之和
                if (x - xj) ** 2 + (y - yj) ** 2 <= (r + rj) ** 2:
                    union(i, j)
            if find(n) == find(n + 1):
                return False

        return True