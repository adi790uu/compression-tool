from collections import defaultdict
import heapq


class Node:
    def __init__(self, symbol=None, frequency=None):
        self.symbol = symbol
        self.frequency = frequency
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.frequency < other.frequency


def build_huffman_tree(characters, frequencies):
    priority_queue = [
        Node(symbol=character, frequency=frequency)
        for character, frequency in zip(characters, frequencies)
    ]
    heapq.heapify(priority_queue)
    while len(priority_queue) > 1:
        left_child = heapq.heappop(priority_queue)
        right_child = heapq.heappop(priority_queue)

        merged_node = Node(
            frequency=left_child.frequency + right_child.frequency,
        )
        merged_node.left = left_child
        merged_node.right = right_child

        heapq.heappush(priority_queue, merged_node)

    return priority_queue[0]


def get_huffman_codes(node, code="", huffman_codes={}):
    if node is None:
        return huffman_codes

    if node.symbol is not None:
        huffman_codes[node.symbol] = code

    get_huffman_codes(node.left, code=code + "0", huffman_codes=huffman_codes)
    get_huffman_codes(node.right, code=code + "1", huffman_codes=huffman_codes)

    return huffman_codes


def encode_text(text, huffman_codes):
    encoded_string = ""
    for character in text:
        encoded_string += huffman_codes.get(character, "")

    byte_array = bytearray()
    for i in range(0, len(encoded_string), 8):
        byte = encoded_string[i : i + 8]
        if len(byte) < 8:
            byte = byte.ljust(8, "0")
        byte_array.append(int(byte, 2))

    return byte_array


def main():
    mapping = defaultdict(int)
    characters = []
    frequencies = []

    file_path = input("Enter the file path: ")
    with open(file_path, "r") as file:
        content = file.read()
        content = content.replace("\n", " ")

        words = [word for word in content.split(" ") if word != ""]

        for word in words:
            for character in word:
                mapping[character] += 1

        for key, value in mapping.items():
            characters.append(key)
            frequencies.append(value)

    top_node = build_huffman_tree(
        characters=characters,
        frequencies=frequencies,
    )

    huffman_codes = get_huffman_codes(node=top_node)
    encoded_text = encode_text(text=content, huffman_codes=huffman_codes)
    print(encoded_text)


if __name__ == "__main__":

    main()
