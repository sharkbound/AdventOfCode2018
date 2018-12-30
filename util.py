import re


def get_all_numbers(text):
    return [int(x) for x in re.findall(r'\b\d+\b', text)]
