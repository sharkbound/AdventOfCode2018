from collections import deque


# https://github.com/fogleman/AdventOfCode2018/blob/master/5.py
# def solve_part_1():
#     data = read_data()
#     res = ['']
#
#     for c in data:
#         if c == res[-1].swapcase():
#             res.pop()
#         else:
#             res.append(c)
#
#     return len(res) - 1

def solve_part_1():
    data = deque(read_data())
    for _ in range(len(data)):
        a, b = data.popleft(), data.popleft()
        if a == b.swapcase():
            continue
        data.appendleft(b)
        data.append(a)
    return len(data)


def read_data():
    with open('data.txt') as f:
        return f.read()


# solve_part_1()
print('actual :', solve_part_1(), '\ncorrect:', 9386)

# def test_part_1_is_correct():
#     ret = solve_part_1()
#     assert ret == 9386, f'day 5 part 1 answer should be 9386, actual {ret}'
