def is_safe(board, row, col, n):

    for i in range(row):
        if board[i][col] == "Q":
            return False

    i = row - 1
    j = col - 1

    while i >= 0 and j >= 0:
        if board[i][j] == "Q":
            return False
        i -= 1
        j -= 1

    i = row - 1
    j = col + 1

    while i >= 0 and j < n:
        if board[i][j] == "Q":
            return False
        i -= 1
        j += 1

    return True


def solve(board, row, n):

    if row == n:
        for r in board:
            print(" ".join(r))
        print()
        return

    for col in range(n):

        if is_safe(board, row, col, n):

            board[row][col] = "Q"

            solve(board, row + 1, n)

            board[row][col] = "."


n = int(input("Enter number of queens: "))

board = [["." for i in range(n)] for j in range(n)]

print("\nSolutions:\n")

solve(board, 0, n)