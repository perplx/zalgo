#!/usr/bin/env python

"""Zalgo text generator."""

# standard imports
import argparse
import random
import sys
import unicodedata
from io import TextIO
from typing import Iterator, List, Tuple


# global constants
COMBINING_CLASSES = {
    202: "Attached Below",
    214: "Attached Above",
    216: "Attached Above Right",
    218: "Below Left",
    220: "Below",
    222: "Below Right",
    224: "Left",
    226: "Right",
    228: "Above Left",
    230: "Above",
    232: "Above Right",
    233: "Double Below",
    234: "Double Above",
    240: "Iota Subscript",
}


def load_combining() -> Tuple[List[str]]:
    """Load combining characters from the `unicodedata` module into 3 classes:
    - `above` for the combining characters that go above the base characters
    - `below` for the combining characters that go below the base characters
    - `other` for the other combining characters

    Determines which by checking for 'above' or 'below' in the name of the combining class.
    """

    above = []
    below = []
    other = []
    for i in range(768, 879):
        c = chr(i)
        combining = unicodedata.combining(c)
        class_name = COMBINING_CLASSES.get(combining, "")
        if "Above" in class_name:
            above.append(c)
        elif "Below" in class_name:
            below.append(c)
        else:
            other.append(c)
    return above, below, other


ABOVE, BELOW, OTHER = load_combining()


def zalgo_choice(choices: List[str], n: int) -> Iterator[str]:
    """Generate between 0 and `n` characters from the given `choices` of combininc characters."""
    num_choices = int(n * random.random()) # random number between 0 and n
    yield from (random.choice(choices) for _ in range(num_choices))


def zalgo_gen(text: str, num_above: int, num_below: int, num_other: int) -> Iterator[str]:
    for c in text:
        yield c
        yield from zalgo_choice(ABOVE, num_above)
        yield from zalgo_choice(BELOW, num_below)
        yield from zalgo_choice(OTHER, num_other)


def zalgo_text_param(text: str, num_above: int, num_below: int, num_other: int) -> str:
    return "".join(zalgo_gen(text, num_above, num_below, num_other))


def zalgo_char(n: int) -> str:
    return "".join(chr(random.randrange(768, 879)) for _ in range(n))


def zalgo_text_simple(text: str, n: int) -> str:
    return "".join(c + zalgo_char(n) for c in text)


def main() -> None:
    # read command-line parameters
    arg_parser = argparse.ArgumentParser(description=__doc__)
    arg_parser.add_argument("input_text")
    arg_parser.add_argument("-a", "--num-above", type=int, default=0)
    arg_parser.add_argument("-b", "--num-below", type=int, default=0)
    arg_parser.add_argument("-o", "--num-other", type=int, default=0)
    args = arg_parser.parse_args()

    # zalgo the input text
    text = zalgo_text_param(args.input_text, args.num_above, args.num_below, args.num_other)
    if isinstance(sys.stdout, TextIO):
        sys.stdout.reconfigure(encoding='utf-8')  # FIXME cant > to file otherwise
        sys.stdout.write(text)


if __name__ ==  "__main__":
    main()
