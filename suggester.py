#!/usr/bin/env python3

from collections import Counter
from difflib import SequenceMatcher
import os
import pprint

# Arbitrary value below which we consider an alias a waste of time
MIN_COMMAND_LENGTH = 14

# Number of repetitions that we need to consider to be significant
REPEAT_THRESHOLD = 5

# Similarity threshold to qualify two commands as being similar
SIMILARITY_THRESHOLD = 0.8

# Verbose
VERBOSE = False

INPUT_FILE = "~/.bash_history"


def load_history(path, format=None):
    """Load a history file"""

    history_lines = []

    with open(path) as history_file:
        for history_line in history_file:
            if history_line.startswith("#"):
                continue

            if len(history_line) < MIN_COMMAND_LENGTH:
                continue

            history_line = history_line.strip()

            history_lines.append(history_line)
    return history_lines


def compare_two(string_one, string_two):
    return SequenceMatcher(None, string_one, string_two).ratio()


def main():
    # TODO load existing aliases
    # TODO accept format string for bash history
    history_data = load_history(os.path.expanduser(INPUT_FILE))

    from collections import Counter

    repeats = dict(Counter(history_data))
    filtered_repeats = {
        command: count
        for (command, count) in repeats.items()
        if count > REPEAT_THRESHOLD
    }

    history_set = iter(sorted(set(history_data)))
    similar_commands = {}

    last = next(history_set)
    for element in history_set:
        value = compare_two(last, element)

        if value > SIMILARITY_THRESHOLD:
            similar_commands[(element, last)] = value

        last = element

    if filtered_repeats:
        print("Found these repetitions that could be candidates for aliases:")
        for command, repetitions in filtered_repeats.items():
            print(f"\t{command}\t({repetitions})")

    if similar_commands:
        print("Found these similar commands that could be candidates for aliases:")
        for (command1, command2), similarity in similar_commands.items():
            print(f"\t* {command1}")
            print(f"\t* {command2} ({similarity})")
            print()


if __name__ == "__main__":
    main()
