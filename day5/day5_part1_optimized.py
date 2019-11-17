from collections import deque


def solve_part_1():
    data = deque(read_data())
    while True:
        for _ in range(len(data) + 2):
            a, b = data.popleft(), data.popleft()
            if a.lower() == b.lower() and a.islower() ^ b.islower():
                break
            data.extend((a, b))
        else:
            break
    return len(data)


def read_data():
    with open('data.txt') as f:
        return f.read()


# solve_part_1()


def test_part_1_is_correct():
    ret = solve_part_1()
    assert ret == 9386, f'day 5 part 1 answer should be 9386, actual {ret}'
