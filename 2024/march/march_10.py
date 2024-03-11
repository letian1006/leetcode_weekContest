"""
划分型dp的套路 
定义二维状态f[i][j]代表前j个数字(nums[0] 到 nums[j-1]这j个数字) 分成i段能够得到的最大能量值
因此f[k][n] 就是答案 即整个数组 划分为k段能够得到的最大能量值
"""
class Solution:
    """
    链接:https://leetcode.cn/problems/maximum-strength-of-k-disjoint-subarrays/submissions/510598942/
    描述:
    给你一个长度为 n 下标从 0 开始的整数数组 nums 和一个 正奇数 整数 k 。
    x 个子数组的能量值定义为 strength = sum[1] * x - sum[2] * (x - 1) + sum[3] * (x - 2) - sum[4] * (x - 3) + ... + sum[x] * 1 ，
    其中 sum[i] 是第 i 个子数组的和。更正式的，能量值是满足 1 <= i <= x 的所有 i 对应的 (-1)i+1 * sum[i] * (x - i + 1) 之和。
    你需要在 nums 中选择 k 个 不相交子数组 ，使得 能量值最大 。
    请你返回可以得到的 最大能量值。
    注意，选出来的所有子数组不需要覆盖整个数组。
    示例:
    输入：nums = [1,2,3,-1,2], k = 3
    输出：22
    解释：选择 3 个子数组的最好方式是选择：nums[0..2] ，nums[3..3] 和 nums[4..4] 。能量值为 (1 + 2 + 3) * 3 - (-1) * 2 + 2 * 1 = 22 。
    """
    def maximumStrength(self, nums: List[int], k: int) -> int:
        n = len(nums)
        s = list(accumulate(nums, initial=0))
        f = [[0 for _ in range(n + 1)] for _ in range(k + 1)]
        # 枚举i
        # f[i][j] = max(f[i][j-1], max(f[i-1][L] + (s[j] - s[L]) * w)) 其中L是划分出的最后一段的最左边的数字的下标
        # 因此最暴力的获得f[i][j]的方法就是 先枚举i 再枚举j 再枚举L(即最后一段的左端点)
        # 但是我们可以经过将公式变形 省去L的枚举行为
        # 括号内的max针对的是L 也就是最后一段的左端点 因此我们将无关的提出去
        # 结果是max(f[i-1][L] - s[L] * w) + s[j] * w
        # 前面一段的max我们可以枚举j的时候直接进行维护即可
        # max(f[i-1][L] - s[L] * w)
        for i in range(1, k + 1):
            # i就是分成多少段
            f[i][i-1] = mx = -inf # 非法方案 i-1个数字分不出i段 定义为负无穷
            wt = (1 if i % 2 else -1) * (k - i + 1) # 能量值的系数
            for j in range(i, n - k + i + 1): # j最小是i 因为你要分出i段 最大是n-k+i 因为要留k-i个数字给后面的k-i段分割使用
                # 如何省去枚举行为呢
                mx = max(mx, f[i-1][j-1] - s[j-1] * wt)
                f[i][j] = max(f[i][j-1], s[j] * wt + mx)
        return f[k][n]
