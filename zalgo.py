#!/usr/bin/env python

# standard imports
import argparse
import random


def zalgo_char(n: int) -> str:
    return "".join(chr(random.randrange(768, 879)) for _ in range(n))


def zalgo_text(text: str, n: int) -> str:
    return "".join(c + zalgo_char(n) for c in text)


def main() -> None:
    print(zalgo_text("For I am become death, destroyer of worlds!", 5))


if __name__ ==  "__main__":
    main()