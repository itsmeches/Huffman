import heapq
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class HuffmanNode:
    def __init__(self, char=None, freq=None, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

    def is_leaf(self):
        return not (self.right or self.left)

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(text):
    frequencies = Counter(text)
    heap = [HuffmanNode(char=c, freq=f) for c, f in sorted(frequencies.items(), key=lambda item: item[1])]

    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)

        # Create a new node with left and right children
        node = HuffmanNode(left=lo, right=hi, freq=lo.freq + hi.freq)
        heapq.heappush(heap, node)

    return heap[0]

def encode(node, code='', mapping=None):
    if mapping is None:
        mapping = {}

    if node.is_leaf():
        mapping[node.char] = code
    else:
        encode(node.left, code + '0', mapping)
        encode(node.right, code + '1', mapping)

    return mapping

def huffman_encoding(text):
    if not text:
        return '', None  # Handle empty input

    root = build_huffman_tree(text)
    result = encode(root)
    encoded_text = ''.join([result[char] for char in text])
    return encoded_text, result, root

def huffman_decoding(encoded_text, root):
    if not encoded_text or not root:
        return ''

    result = ''
    current_node = root

    for bit in encoded_text:
        if bit == '0':
            current_node = current_node.left
        else:
            current_node = current_node.right

        if current_node.is_leaf():
            result += current_node.char
            current_node = root

    return result

def visualize_tree(root, width=300, height=300):
    def plot_node(node, x, y, size):
        plt.gca().add_patch(
            patches.Rectangle(
                (x - size / 2, y - size / 2),
                size,
                size,
                facecolor="white" if node.is_leaf() else "none",
                edgecolor="black",
                hatch='x' if node.is_leaf() else ''
            )
        )

        text = node.char if node.is_leaf() else f"({node.freq})"
        plt.text(
            x,
            y,
            text,
            ha='center',
            va='center',
            fontsize=12
        )

    def position_node(node, x, y, size):
        node.position = (x, y)
        if node.is_leaf():
            return size / 2
        else:
            return max(
                position_node(node.left, x - size / 4, y - size / 4, size / 2),
                position_node(node.right, x + size / 4, y - size / 4, size / 2)
            )

    plot_node(root, width / 2, height / 2, width / 2)
    position_node(root, width / 2, height / 2, width / 2)

    queue = [(root,)]
    while queue:
        path = queue.pop(0)
        node = path[-1]
        if node.left:
            queue.append(path + (node.left,))
        if node.right:
            queue.append(path + (node.right,))

        if len(path) > 1:
            parent = path[-2]
            x_offset = 0.1 * (width / 2)
            y_offset = 0.1 * (height / 2)
            x = (node.position[0] + parent.position[0]) / 2 + x_offset
            y = (node.position[1] + parent.position[1]) / 2 + y_offset
            size = ((parent.position[0] - node.position[0]) ** 2 +
                    (parent.position[1] - node.position[1]) ** 2) ** 0.5
            plot_node(parent, x, y, size)

    plt.axis('equal')
    plt.axis('off')
    plt.show()

user_input = input("Enter a text to encode and decode using Huffman coding: ")

# Check for single character input
if len(user_input) == 1:
    char_encoding, huffman_code, huffman_tree = huffman_encoding(user_input)
    print(f"\nHuffman Encoding for {user_input}: {char_encoding}")
    print("\nHuffman Code:")
    for char, code in huffman_code.items():
        print(f"{char}: {code}")
    print("\nHuffman Tree:")
    visualize_tree(huffman_tree)
else:
    # Encoding
    encoded_text, huffman_code, huffman_tree = huffman_encoding(user_input)

    # Display Results
    print("\nOriginal Data:", user_input)
    # Display Huffman Code
    print("\nHuffman Code:")
    for char, code in huffman_code.items():
        print(f"{char}: {code}")
    print("Encoded Data:", encoded_text)

    # Decoding
    decoded_text = huffman_decoding(encoded_text, huffman_tree)
    print("\nDecoded Data:", decoded_text)

    # Display Huffman Tree
    print("\nHuffman Tree:")
    visualize_tree(huffman_tree)
