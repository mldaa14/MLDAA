n = int(input("Enter number of items: "))

items = []

for i in range(n):
    profit = int(input("Enter profit: "))
    weight = int(input("Enter weight: "))
    ratio = profit / weight
    items.append([profit, weight, ratio])

capacity = int(input("Enter knapsack capacity: "))

items.sort(key=lambda x: x[2], reverse=True)

total_profit = 0

for profit, weight, ratio in items:
    if capacity >= weight:
        capacity -= weight
        total_profit += profit
    else:
        total_profit += ratio * capacity
        capacity = 0
        break

print("Maximum Profit:", total_profit)