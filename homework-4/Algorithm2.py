class Solution(object):
    def twoSum(self, nums, target):
        copy = []
        for i in range(len(nums)):
            copy.append(nums[i])

        copy.sort()
        for i in range(len(copy)):
            a = 0
            b = len(nums) - 1
            diff = target - copy[i]
            res = []
            while a <= b:
                m = (a + b) // 2
                if diff < copy[m]:
                    b = m - 1
                elif diff > copy[m]:
                    a = m + 1
                elif diff == copy[m] and m != i:
                    res = [nums.index(copy[i]), len(nums) - nums[::-1].index(diff) - 1]
                    break
                else:
                    break
            if res != []:
                return min(res), max(res)