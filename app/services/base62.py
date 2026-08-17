CHARACTERS = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def encode(number: int) -> str:
    if number == 0:
        return CHARACTERS[0]

    result = []

    while number > 0:
        number, remainder = divmod(number, 62)
        result.append(CHARACTERS[remainder])

    return "".join(reversed(result))