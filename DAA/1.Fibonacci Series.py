n = int(input("Enter the number of terms: "))
a = 0
b = 1
step_count = 0
print("Fibonacci Series:")
for i in range(n):
 print(a, end=" ")
 step_count += 1 
 c = a + b
 step_count += 1
 a = b
 step_count += 1
 b = c
 step_count += 1
print("\nStep Count:", step_count)