import os

day = int(input('what day? '))
FOLDER = f'day{day}'

os.mkdir(f'day{day}')

open(f'{FOLDER}/{FOLDER}_part1.py', 'w').close()
open(f'{FOLDER}/{FOLDER}_part2.py', 'w').close()
open(f'{FOLDER}/data.txt', 'w').close()

print(f'created folder! {FOLDER}')
