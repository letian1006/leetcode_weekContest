"""
三题选手 t4是一个分类中位数贪心的好题 前提是需要进行特判
题目链接:https://leetcode.cn/problems/minimum-moves-to-pick-k-ones/

题目描述:
给你一个下标从 0 开始的二进制数组 nums，其长度为 n ；另给你一个 正整数 k 以及一个 非负整数 maxChanges 。
灵茶山艾府在玩一个游戏，游戏的目标是让灵茶山艾府使用 最少 数量的 行动 次数从 nums 中拾起 k 个 1 。游戏开始时，
灵茶山艾府可以选择数组 [0, n - 1] 范围内的任何索引index 站立。如果 nums[index] == 1 ，灵茶山艾府就会拾起一个 1 ，
并且 nums[index] 变成0（这 不算 作一次行动）。之后，灵茶山艾府可以执行 任意数量 的 行动（包括零次），在每次行动中灵茶山艾府必须 恰好 执行以下动作之一：
选择任意一个下标 j != index 且满足 nums[j] == 0 ，然后将 nums[j] 设置为 1 。这个动作最多可以执行 maxChanges 次。
选择任意两个相邻的下标 x 和 y（|x - y| == 1）且满足 nums[x] == 1, nums[y] == 0 ，
然后交换它们的值（将 nums[y] = 1 和 nums[x] = 0）。如果 y == index，在这次行动后灵茶山艾府拾起一个 1 ，并且 nums[y] 变成 0 。
返回灵茶山艾府拾起 恰好 k 个 1 所需的 最少 行动次数。

示例:
输入：nums = [1,1,0,0,0,1,1,0,0,1], k = 3, maxChanges = 1
输出：3
解释：如果游戏开始时灵茶山艾府在 index == 1 的位置上，按照以下步骤执行每个动作，他可以利用 3 次行动拾取 3 个 1 ：
游戏开始时灵茶山艾府拾取了一个 1 ，nums[1] 变成了 0。此时 nums 变为 [1,0,0,0,0,1,1,0,0,1] 。
选择 j == 2 并执行第一种类型的动作。nums 变为 [1,0,1,0,0,1,1,0,0,1]
选择 x == 2 和 y == 1 ，并执行第二种类型的动作。nums 变为 [1,1,0,0,0,1,1,0,0,1] 。由于 y == index，灵茶山艾府拾取了一个 1 ，nums 变为  [1,0,0,0,0,1,1,0,0,1] 。
选择 x == 0 和 y == 1 ，并执行第二种类型的动作。nums 变为 [0,1,0,0,0,1,1,0,0,1] 。由于 y == index，灵茶山艾府拾取了一个 1 ，nums 变为  [0,0,0,0,0,1,1,0,0,1] 。
请注意，灵茶山艾府也可能执行其他的 3 次行动序列达成拾取 3 个 1
"""

"""
整个题目的意思理解如下
两种操作 第一种操作是将一个数据点为1 的位置通过邻项交换得到1
第二种操作就是将原本为0的一个数据点变成1 
如果只有第一种操作 那么这就是一个货仓选址问题 即选择一个地点 到k个1的距离之和最短
但是如果有第二种操作 那么我们就要先进行特判 因为这个操作可以选择最近的0 将其变成1 也就是通过两次操作就可以获得一个1
"""

class Solution:
    def minimumMoves(self, nums: List[int], k: int, maxChanges: int) -> int:
        c = 0
        i = 0
        n = len(nums)
        idx = []
        while i < n:
            if nums[i] == 0:
                i += 1
                continue
            idx.append(i)
            i += 1
            cur = 1
            while i < n and nums[i] == 1:
                idx.append(i)
                cur += 1
                i += 1
            # 最多有多少个连续的1
            if cur > 2:
                # 如果有三个连续的1 那么我们选择中间的那个1作为初始点
                c = 3
            elif cur == 2:
                # 如果只有两个连续的1 那么我们选择这两个相邻的点 左边或者右边都可以 这是没关系的
                c = max(2, c)
            else:
                c = max(1, c)
        if c + maxChanges >= k:
            # 如果剩下的1可以由操作2完成 那么我们使用操作2来获取剩下的1 这样是最方便的
            if c >= k:
                # 如果选择的初始点的周围已经可以满足找到k个1了 那么我们只需要进行k-1次操作1即可
                # 比如连续三个1 111 k也是3 那么我们选择中间的1 作为开始点 那么就只需要进行两次操作一就可以得到三个1
                # 因为一开始选择的位置上如果有1 那么直接就可以获得 且不算是一次操作
                return k - 1
            else:
                # 看看c是不是一个正数 如果是一个正数 我们就可以定这个位置为开始点 否则我们只能选择全部使用操作2来获取1
                # 但是操作二不能选择一开始选定的位置 因此我们只能选择开始位置的旁边一个位置 将其转换为1 然后再通过操作1 交换过去
                # 也就是两次操作才可以
                return (c - 1 if c else 0) + (k - c) * 2
        
        # 如果上面的c + maxchanges不能找到所有的1 那么剩下的就需要通过操作1 也就是邻项交换得到其他的1 这就是一个货仓选址问题
        # 后面就是货仓选址问题 使用中位数贪心策略即可
        # 长度为k-maschanges的窗口中 选择一个位置 到各个1的距离最短即可 其他的1使用操作2完成即可
        size = k - maxChanges 
        pre_sm = list(accumulate(idx, initial=0))
        ans = inf
        for r in range(size, len(idx) + 1):
            # 左边闭合右边开放的区间 在这个区间选择一个数字 到达其他位置的距离最短 我们选择中位数位置
            l = r - size
            mid = (l + r) >> 1
            left = (mid - l) * idx[mid] - (pre_sm[mid] - pre_sm[l])  # 中点位置到左半部分的距离
            right = (pre_sm[r] - pre_sm[mid]) - (r - mid) * idx[mid]  # 中点位置到右半部分的距离
            ans = min(ans, left + right)
        return maxChanges * 2 + ans






