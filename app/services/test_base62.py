from app.services.base62 import encode


def main():
    test_numbers = [0, 1, 9, 10, 61, 62, 125, 1187]

    for number in test_numbers:
        print(number, "->", encode(number))


if __name__ == "__main__":
    main()