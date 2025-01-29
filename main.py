from collections import defaultdict


def main():
    mapping = defaultdict(int)
    file_path = input("Enter the file path: ")
    with open(file_path, "r") as file:
        content = file.read()
        content = content.replace("\n", " ")
        words = [word for word in content.split(" ") if word != ""]

        for word in words:
            for character in word:
                mapping[character] += 1

        for key, value in mapping.items():
            print(f"There are {value} occurrences for {key}")


if __name__ == "__main__":
    main()
