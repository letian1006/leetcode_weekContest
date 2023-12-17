class Solution:
    def countCompleteSubstrings(self, word: str, k: int) -> int:
        # 完全字符串 从头到尾 恰好出现k次
        n = len(word)
        i = ans = 0
        for st in range(n):
            i = st + 1
            cnt = [0] * 26
            cnt[ord(word[st]) - ord('a')] += 1
            while i < n and ord(word[i]) - ord(word[i-1]) < 3:
                index = ord(word[i]) - ord('a')
                cnt[index] += 1
                if cnt[index] > k:
                    break
                if all(ele == k or ele == 0 for ele in cnt):
                    ans += 1
        return ans

if __name__ == '__main__':
    s = Solution().countCompleteSubstrings("igigee", 2)
    print(s)
