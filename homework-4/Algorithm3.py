class Solution(object):
    def twoSum(self, nums, target):
        indexes = {}
        for i, n in enumerate(nums):
            diff = target - n
            if diff in indexes:
                return i, indexes[diff]
            else:
                indexes[n] = i