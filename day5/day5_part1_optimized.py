from collections import deque


# https://github.com/fogleman/AdventOfCode2018/blob/master/5.py
# i tried making a version that uses a deque, but never worked out
def solve_part_1():
    data = read_data()
    res = ['']

    for c in data:
        if c == res[-1].swapcase():
            res.pop()
        else:
            res.append(c)

    # skip the empty placeholder string
    return ''.join(res[1:])


def read_data():
    with open('data.txt') as f:
        return f.read()


# solve_part_1()
print('actual :', len(solve_part_1()), '\ncorrect:', 9386)

# def test_part_1_is_correct():
#     ret = solve_part_1()
#     assert ret == 9386, f'day 5 part 1 answer should be 9386, actual {ret}'
