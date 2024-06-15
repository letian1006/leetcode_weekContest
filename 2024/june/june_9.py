"""
链接：https://leetcode.cn/problems/maximum-total-reward-using-operations-ii/description/
描述：
给你一个整数数组 rewardValues，长度为 n，代表奖励的值。
最初，你的总奖励 x 为 0，所有下标都是 未标记 的。你可以执行以下操作 任意次 ：
从区间 [0, n - 1] 中选择一个 未标记 的下标 i。
如果 rewardValues[i] 大于 你当前的总奖励 x，则将 rewardValues[i] 加到 x 上（即 x = x + rewardValues[i]），并 标记 下标 i。
以整数形式返回执行最优操作能够获得的 最大 总奖励。
示例：
输入：rewardValues = [1,1,3,3]

输出：4

解释：

依次标记下标 0 和 2，总奖励为 4，这是可获得的最大值。
"""
class Solution:
    def maxTotalReward(self, rewardValues: List[int]) -> int:
        # f[i][j] 表示前i个数 能够构造出j奖励的可能性 f[0][0] = True 则表示第0个数可以构造出最大总奖励为0
        # 如果f[i][j] = False 则表示前i个数不能构造出总奖励为j 我们从大到小枚举这个rewardValues中的数据
        # 我们压缩掉第一个维度 并且使用一个二进制数字来代表这个每个f[i]的所在的布尔数组
        # 因此可以做如下状态转移 即选或者不选当前数字v 可以表示
        # f[i][j] = f[i-1][j]
        # 然后f[i][j] = f[i-1][j-v] 其中j-v < v 
        # 其中j-v表示之前的总奖励 v表示当前枚举到的数字 
        # 所以f[i][j] 就是低v位能够左移v位构造出相应位置上的答案 加上之前我们可以构造出的答案
        # f[i] = f[i-1] | ((mask & f[i-1]) << v)
        f = 1
        for v in sorted(set(rewardValues)):
            mask = (1 << v) - 1
            f |= (mask & f) << v
        return f.bit_length() - 1  # 返回最高位的所在的位置即可
