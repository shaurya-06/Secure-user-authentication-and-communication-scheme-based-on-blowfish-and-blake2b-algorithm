import random


def generate_salt():
    digits = "0123456789"
    chars = []
    for i in range(random.randint(15, 20)):
        chars.append(random.choice(digits))

    return "".join(chars)
