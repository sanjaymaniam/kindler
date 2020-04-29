from collections import Counter

path = 'test.txt'
file = open(path, 'r', encoding='utf-8-sig')

types = []

for line in file:
    listline = line.split()
    types.append(listline[4])
print(Counter(types))
