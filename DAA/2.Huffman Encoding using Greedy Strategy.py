import heapq

n = int(input("Enter number of characters: "))
heap = []

for i in range(n):
    ch = input("Enter character: ")
    freq = int(input("Enter frequency: "))
    node = (freq, ch, None, None)
    heap.append((freq, i, node))

heapq.heapify(heap)

count = n

while len(heap) > 1:
    a = heapq.heappop(heap)
    b = heapq.heappop(heap)

    new_freq = a[0] + b[0]
    new_node = (new_freq, None, a[2], b[2])

    heapq.heappush(heap, (new_freq, count, new_node))
    count += 1

codes = {}

def huffman(tree, code=""):
    freq, ch, left, right = tree

    if ch is not None:
        codes[ch] = code if code else "0"
        return

    huffman(left, code + "0")
    huffman(right, code + "1")

def print_tree(tree, prefix="", branch=""):
    freq, ch, left, right = tree

    if ch is not None:
        print(prefix + branch + ch + " (" + str(freq) + ")")
    else:
        print(prefix + branch + str(freq))
        print_tree(left, prefix + "   ", "0-- ")
        print_tree(right, prefix + "   ", "1-- ")

if len(heap) > 0:
    root = heap[0][2]

    print("\nHUFFMAN TREE:")
    print_tree(root)

    huffman(root)

    print("\nHUFFMAN CODES:")
    for ch, code in codes.items():
        print(ch, ":", code)

print("\nTime Complexity: O(n log n)")
print("Space Complexity: O(n)")