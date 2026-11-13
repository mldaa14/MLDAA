n = int(input("Enter number of items: "))

p = []
w = []

for i in range(n):
    p.append(int(input("Enter profit: ")))
    w.append(int(input("Enter weight: ")))

capacity = int(input("Enter capacity: "))

dp = [[0] * (capacity + 1) for i in range(n + 1)]

for i in range(1, n + 1):
    for j in range(capacity + 1):
        if w[i-1] <= j:
            dp[i][j] = max(p[i-1] + dp[i-1][j-w[i-1]], dp[i-1][j])
        else:
            dp[i][j] = dp[i-1][j]

print("Maximum Profit:", dp[n][capacity])