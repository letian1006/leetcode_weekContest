from ast import List
from collections import defaultdict
from sortedcontainers import SortedList

# 链接https://leetcode.cn/problems/find-x-sum-of-all-k-long-subarrays-ii/description/
# 两个有序集合 或者两个堆倒来倒去 来实现这个效果

class Solution:
    def findXSum(self, nums: List[int], k: int, x: int) -> List[int]:

        l, r = SortedList(), SortedList()
        r_sum = 0 # R集合中的元素 谁更大一些 里面保存的是一个pair (cit[num], num)
        cnt = defaultdict(int)

        def add(in_):
            if cnt[in_] == 0:
                return
            p = (cnt[in_], in_) # 待加入的pair 分别是频率和数字
            if r and p > r[0]:  # 新加入的pair大于r的最小值 因此我们直接加入r集合  注意在这里先不考虑维护r集合的size大小问题 这个问题给r2l 和l2r函数去解决
                nonlocal r_sum
                r_sum += p[0] * p[1]
                r.add(p)
            else:  # 否则加入l集合
                l.add(p)
        
        # 只管添加或者删除一个元素 不做其他的事情
        def remove(out):
            if cnt[out] == 0:
                return
            p = (cnt[out], out)
            if p in r:
                nonlocal r_sum
                r_sum -= p[0] * p[1]
                r.remove(p)
            else:
                l.remove(p)
        
        def r2l():
            nonlocal r_sum
            p = r[0]
            r_sum -= p[0] * p[1]
            r.remove(p)
            l.add(p)
        
        def l2r():
            nonlocal r_sum
            p = l[-1]
            r_sum += p[0] * p[1]
            l.remove(p)
            r.add(p)
        
        ans = []
        for i, c in enumerate(nums):
            remove(c)  # 新剔除的pair
            cnt[c] += 1
            add(c)  # 新加入的pair

            if i - k + 1 < 0:
                continue  # 数字不够
            # 新加进来的数字 需要维持两个集合的平衡 
            # 保证加进来的数字 r集合维护较大的x个pair
            # l集合做预备役 在r集合pair数不够用的情况下 补充到r集合中
            while l and len(r) < x:
                l2r()
            while r and len(r) > x:
                r2l()
            ans.append(r_sum)
            remove(nums[i - k + 1])  # 新剔除的pair
            cnt[nums[i - k + 1]] -= 1
            add(nums[i- k + 1])  # 新加入的pair 
            
        
        return ans
