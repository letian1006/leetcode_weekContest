from typing import List



class Trie:
    # 0 - 1bit字典树
    def __init__(self):
        self.children = [None] * 2
        self.cnt = 0


class Solution:
    # 链接:https://leetcode.cn/problems/maximum-strong-pair-xor-ii/
    def maximumStrongPairXor(self, nums: List[int]) -> int:
        root = Trie()
        HIGH_BIT = 20

        def insert(num, node):
            for i in range(HIGH_BIT, -1, -1):
                bit = (num >> i) & 1
                if not node.children[bit]:
                    node.children[bit] = Trie()
                node.children[bit].cnt += 1
                node = node.children[bit]

        # 删除一个数字
        def remove(num, node):
            for i in range(HIGH_BIT, -1, -1):
                bit = (num >> i) & 1
                node = node.children[bit]
                node.cnt -= 1

        def get(num, node):
            res = 0
            for i in range(HIGH_BIT, -1, -1):
                # 将符合要求的数字都添加到字典树中
                need = (num >> i & 1) ^ 1
                if node.children[need] and node.children[need].cnt > 0:
                    res |= 1 << i
                    node = node.children[need]
                else:
                    node = node.children[need ^ 1]
            return res

        n = len(nums)
        nums.sort()
        ans = index = 0
        for i, c in enumerate(nums):
            # while条件是为了将此时符合要求的数字添加到字典树中
            while index < n and nums[index] <= c * 2:
                insert(nums[index], root)
                index += 1
            ans = max(ans, get(c, root))
            # 删除当前数字
            remove(c, root)

        return ans
