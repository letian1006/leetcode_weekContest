"""
386场周赛 一题选手
t4反悔贪心的解法 也许会成为周赛最难的一题 这里给出另外两题的解法
也就是t2和t3的解法 t4稍后会补充上去 一个思维难度非常大的反悔贪心题目
"""
from typing import List


class Solution:
    """
    链接:https://leetcode.cn/problems/find-the-largest-area-of-square-inside-two-rectangles/
    描述:
    在二维平面上存在 n 个矩形。给你两个下标从 0 开始的二维整数数组 bottomLeft 和 topRight，两个数组的大小都是 n x 2 ，
    其中 bottomLeft[i] 和 topRight[i] 分别代表第 i 个矩形的 左下角 和 右上角 坐标。
    我们定义 向右 的方向为 x 轴正半轴（x 坐标增加），向左 的方向为 x 轴负半轴（x 坐标减少）。
    同样地，定义 向上 的方向为 y 轴正半轴（y 坐标增加），向下 的方向为 y 轴负半轴（y 坐标减少）。
    你可以选择一个区域，该区域由两个矩形的 交集 形成。你需要找出能够放入该区域 内 的 最大 正方形面积，并选择最优解。
    返回能够放入交集区域的正方形的 最大 可能面积，如果矩形之间不存在任何交集区域，则返回 0
    示例:
    输入：bottomLeft = [[1,1],[2,2],[3,1]], topRight = [[3,3],[4,4],[6,6]]
    输出：1
    解释：边长为 1 的正方形可以放入矩形 0 和矩形 1 的交集区域，或矩形 1 和矩形 2 的交集区域。因此最大面积是边长 * 边长，即 1 * 1 = 1。
    可以证明，边长更大的正方形无法放入任何交集区域
    """

    def largestSquareArea(self, bottomLeft: List[List[int]], topRight: List[List[int]]) -> int:
        # 思路就是枚举 就是给你两个矩形的左下角和右上角的坐标 求这两个矩形的相交部分面积
        # 同时得到最大的能够放进去的正方形坐标
        n = len(bottomLeft)
        ans = 0
        for i in range(n):
            for j in range(i + 1, n):
                bx1, by1 = bottomLeft[i]  # 第一个矩形的左下角坐标
                tx1, ty1 = topRight[i]  # 第一个矩形的右下角坐标
                bx2, by2 = bottomLeft[j]  # 第二个矩形的左下角坐标
                tx2, ty2 = topRight[j]  # 第二个矩形的右上角坐标
                bx, by = max(bx1, bx2), max(by1, by2)  # 两个矩形相交部分的左下角坐标
                tx, ty = min(tx1, tx2), min(ty1, ty2)  # 两个矩形相交部分的右上角坐标
                size = min(tx - bx, ty - by)  # 两个矩形相交部分的边长 也就是能够放进这个相交部分的最大正方形边长
                if size > 0:
                    ans = max(ans, size * size)
        return ans

    """
    链接: https://leetcode.cn/problems/earliest-second-to-mark-indices-i/description/
    描述:
    给你两个下标从 1 开始的整数数组 nums 和 changeIndices ，数组的长度分别为 n 和 m 。
    一开始，nums 中所有下标都是未标记的，你的任务是标记 nums 中 所有 下标。
    从第 1 秒到第 m 秒（包括 第 m 秒），对于每一秒 s ，你可以执行以下操作 之一 ：
    选择范围 [1, n] 中的一个下标 i ，并且将 nums[i] 减少 1 。
    如果 nums[changeIndices[s]] 等于 0 ，标记 下标 changeIndices[s] 。
    什么也不做。
    请你返回范围 [1, m] 中的一个整数，表示最优操作下，标记 nums 中 所有 下标的 最早秒数 ，如果无法标记所有下标，返回 -1 。
    示例:
    输入：nums = [2,2,0], changeIndices = [2,2,2,2,3,2,2,1]
    输出：8
    解释：这个例子中，我们总共有 8 秒。按照以下操作标记所有下标：
    第 1 秒：选择下标 1 ，将 nums[1] 减少 1 。nums 变为 [1,2,0] 。
    第 2 秒：选择下标 1 ，将 nums[1] 减少 1 。nums 变为 [0,2,0] 。
    第 3 秒：选择下标 2 ，将 nums[2] 减少 1 。nums 变为 [0,1,0] 。
    第 4 秒：选择下标 2 ，将 nums[2] 减少 1 。nums 变为 [0,0,0] 。
    第 5 秒，标记 changeIndices[5] ，也就是标记下标 3 ，因为 nums[3] 等于 0 。
    第 6 秒，标记 changeIndices[6] ，也就是标记下标 2 ，因为 nums[2] 等于 0 。
    第 7 秒，什么也不做。
    第 8 秒，标记 changeIndices[8] ，也就是标记下标 1 ，因为 nums[1] 等于 0 。
    现在所有下标已被标记。
    最早可以在第 8 秒标记所有下标。
    所以答案是 8 。
    """

    def earliestSecondToMarkIndices(self, nums: List[int], changeIndices: List[int]) -> int:

        # 整个过程可以抽象为一个考试模型 nums[i]表示 第i门考试需要多少天复习
        # changeIndices[i]表示第i门考试的考试时间 如changeIndices[5] = 3 表示第五天可以进行第三门考试 前提是这门课已经复习好了
        # 也就是nums[2] == 0(下标从0开始 nums[2]代表第三门考试需要的复习时间) 因此我们可以二分答案 因为留给我们的时间越长
        # 我们就越能将所有的考试完成

        n, m = len(nums), len(changeIndices)
        l, r = 1, m
        ans = -1

        def check(mx):
            # mx表示在mx天内能不能完成所有的考试
            last_day = [-1] * n  # 记录每门课的最后一次考试时间 我们越后面考试越好 这样我们就有充足的时间复习
            for i, c in enumerate(changeIndices[:mx]):
                last_day[c - 1] = i
            # 有的考试在mx天内无法进行 所有不可能完成所有考试
            if -1 in last_day:
                return False
            cnt = 0

            for i, c in enumerate(changeIndices[:mx]):
                if i == last_day[c - 1]:
                    # 最后一天考试时间了
                    if cnt < nums[c - 1]:
                        # 如果累积的复习天数不能支持这门考试的复习完成 我们就无法完成所有考试 返回False 
                        return False
                    cnt -= nums[c - 1]  # 消耗之前累积的复习天数 
                else:
                    cnt += 1  # 不是最后一天 我们就复习考试 相当于累积可供复习的天数 供最后的考试截止时间消耗
            return True

        while l <= r:
            mid = l + r >> 1
            if check(mid):
                ans = mid
                r = mid - 1
            else:
                l = mid + 1
        return ans
