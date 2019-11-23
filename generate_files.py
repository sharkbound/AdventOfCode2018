from pathlib import Path


def create_files(base: Path, *files):
    if not base.exists():
        base.mkdir(parents=True)

    for file in files:
        if not (path := base / file).exists():
            open(path, 'w').close()


day = input("what day? ")
day_folder = Path(f'day{day}')
create_files(day_folder, f'day{day}_part1.py', f'day{day}_part2.py', 'data.txt', 'example.txt')
print(f'created folder! {day_folder}')
