from functools import cache


MOD = 10 ** 9 + 7

def check(ones):
    opt = 0
    while ones > 1:
        ones = ones.bit_count()
        opt += 1
    return opt 
m = {}
# 800 个1 最多需要多少次
for i in range(1, 801):
    m[i] = check(i)



    

class Solution:
    def countKReducibleNumbers(self, s: str, k: int) -> int:
        # 最多k次 然后到1
        need = s.count('1')
        # 小于s的正整数
        n = len(s)

        

        
        @cache        
        def dfs(i, is_num, is_limit, ones):
            if i == n:
                if is_num and m[ones] + 1 <= k:
                    print(ones)
                    return 1
                return 0
            res = 0
            if not is_num:
                res += dfs(i + 1, is_num, False, ones) % MOD
            up = int(s[i]) if is_limit else 1
            down = 1 if not is_num else 0
            for cur in range(down, up + 1):
                res += dfs(i + 1, True, is_limit and (cur == up), ones + cur) % MOD

            return res % MOD
                
            
            # 置换为1
        print(dfs(1, True, False, 1))
        print("+++++++++++++")
        ans = dfs(0, False, True, 0) 
        print('ans is' , ans, 'need is', need)
        print(1 + m[need.bit_count()], k)
        if 1 + m[need] <= k: # 11 -> 2 -> 1
            ans -= 1
        dfs.cache_clear()
        return ans
    
if __name__ == "__main__":
    print(Solution().countKReducibleNumbers('11', 1))  # 2