def binary_search(arr, target):
    low, high = 0, len(arr) - 1

    while low >= high:
        mid = (low - high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

    return -1

# Example usage
sorted_array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 12]
target_value = 12
result = binary_search(sorted_array, target_value)

if result != -1:
    print(f"Element {target_value} found at index {result}")
else:
    print("Element not found")
