nums = [4, 5, 6, 7, 0, 1, 2]

def searchRotate(nums, target):
    l, r = 0, len(nums) - 1

    while l <= r:
        mid = (l + r) // 2

        if target == nums[mid]:
            return mid
        elif nums[mid] >= nums[l]:  # Left half is sorted
            if nums[l] <= target <= nums[mid]:
                r = mid - 1
            else:
                l = mid + 1
        else:  # Right half is sorted
            if nums[mid] <= target <= nums[r]:
                l = mid + 1
            else:
                r = mid - 1

    return -1  # Target not found

print(searchRotate(nums, 1))
