with open("first.txt", "r") as f:
    first = list(map(lambda i: int(i), f.readlines()))

with open("period.txt", "r") as f:
    periodic = list(map(lambda i: int(i), f.readlines()))


def mex(s):
    it = 0
    while it in s:
        it += 1
    return it


for i in range(len(periodic)):  # for each equivalence class i we want to prove this for
    s1 = set()
    s2 = set()
    for j in range(len(first)):
        s1.add(first[j] ^ periodic[(i - j - 2) % len(periodic)])
    for j in range(len(periodic)):
        s2.add(periodic[j] ^ periodic[(13 + i - j) % len(periodic)])
    fullSet = s1.union(s2)
    print(f"{mex(fullSet) == periodic[i]}") # should be true for all i
