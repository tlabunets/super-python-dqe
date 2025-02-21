# 1.create list of 100 random numbers from 0 to 1000
import random # standard module is generating random numbers

random_numbers = [random.randint(0, 1000) for _ in range(100)]  # create list due call function of random module
#random.randint(a, b) — generate random integer from a to b
#for _ in range(100) - loop for 100 times

print(f"List of 100 random numbers from 0 to 1000: {random_numbers}") #print list in result view

# 2. sort list from min to max (without using sort())
def selection_sort(lst):
    n = len(lst) #idetify length of list
    for i in range(n): #go through all the elements of the list
        min_index = i #suppose current element is min
        for j in range(i + 1, n): #find min value among next elements
            if lst[j] < lst[min_index]: #if less value was found
                min_index = j #remind it
        lst[i], lst[min_index] = lst[min_index], lst[i]  # Swap the elements
    return lst

sorted_numbers = selection_sort(random_numbers) #call function described abow
print(f"Sorted list from min to max: {sorted_numbers}") #print result

# 3. calculate average for even and odd numbers
#numbers = [1, 7, 4, 2, 5, 0]

# divide the numbers into even and odd
even_numbers = [num for num in random_numbers if num % 2 == 0]  # even
odd_numbers = [num for num in random_numbers if num % 2 != 0]   # odd

# calculate average for even and odd numbers
average_even = sum(even_numbers) / len(even_numbers) if even_numbers else 0
average_odd = sum(odd_numbers) / len(odd_numbers) if odd_numbers else 0

# Derive the result
print(f"average for even numbers: {average_even}")
print(f"average for odd numbers: {average_odd}")