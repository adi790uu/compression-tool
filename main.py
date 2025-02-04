from collections import defaultdict
import heapq
import pickle
import sys


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


def decode_text(encoded_text, huffman_codes):
    binary_string = "".join(format(byte, "08b") for byte in encoded_text)
    decoded_string = ""

    current_node = huffman_codes

    for bit in binary_string:
        if bit == "0":
            current_node = (
                current_node.left
                if current_node is not None and current_node.left is not None
                else None
            )
        else:
            current_node = (
                current_node.right
                if current_node is not None and current_node.right is not None
                else None
            )

        if current_node is not None and current_node.symbol is not None:
            decoded_string += current_node.symbol
            current_node = huffman_codes

    return decoded_string


def serialize_huffman_tree(node):
    if node is None:
        return None
    return {
        "symbol": node.symbol,
        "frequency": node.frequency,
        "left": serialize_huffman_tree(node.left),
        "right": serialize_huffman_tree(node.right),
    }


def save_compressed_file(file_path, encoded_text, huffman_tree):
    with open(file_path, "wb") as file:
        data = {
            "tree": serialize_huffman_tree(huffman_tree),
            "encoded_text": encoded_text,
        }
        pickle.dump(data, file)


def deserialize_huffman_tree(data):
    if data is None:
        return None

    symbol = data.get("symbol")
    frequency = data.get("frequency")

    node = Node(symbol=symbol, frequency=frequency)
    node.left = deserialize_huffman_tree(data.get("left"))
    node.right = deserialize_huffman_tree(data.get("right"))

    return node


def main():
    arguments = sys.argv[1:]

    if len(arguments) != 2:
        print("Invalid command!")
        exit(0)

    if arguments[0] == "-e":
        try:
            mapping = defaultdict(int)
            characters = []
            frequencies = []

            with open(arguments[1], "r") as file:
                content = file.read()
                for character in content:
                    mapping[character] += 1

                for key, value in mapping.items():
                    characters.append(key)
                    frequencies.append(value)

            top_node = build_huffman_tree(
                characters=characters,
                frequencies=frequencies,
            )

            huffman_codes = get_huffman_codes(node=top_node)
            encoded_text = encode_text(
                text=content,
                huffman_codes=huffman_codes,
            )
            save_compressed_file("compressed_data.bin", encoded_text, top_node)
        except Exception as e:
            print(f"Error occurred while compressing the file! error: {e}")

    elif arguments[0] == "-d":
        try:
            with open(arguments[1], "rb") as file:
                data = pickle.load(file)
                tree_data = data["tree"]
                encoded_data = data["encoded_text"]

                reconstructed_tree = deserialize_huffman_tree(tree_data)
                decoded_text = decode_text(
                    encoded_text=encoded_data, huffman_codes=reconstructed_tree
                )

                with open("text.txt", "w") as file:
                    file.write(decoded_text)
                    file.close()
        except Exception as e:
            print(f"Error occurred while decompressing the file! error: {e}")


if __name__ == "__main__":
    main()
