def mex(s):  # helper mex function
    i = 0
    while i in s:
        i += 1
    return i


def compute_dn(n):  # returns all dn values before and on n
    cache = [0, 0]  # nim values for 1x0 and 1x1
    for i in range(2, n + 1):
        cache.append(mex(set([cache[j] ^ cache[i-j-2] for j in range(i // 2)])))
    return cache

# compare with:
def g1ncram(x):
    first = [0, 0, 1, 1, 2, 0, 3, 1, 1, 0, 3, 3, 2, 2, 4, 0, 5, 2, 2, 3, 3, 0,
             1, 1, 3, 0, 2, 1, 1, 0, 4, 5, 2, 7, 4, 0, 1, 1, 2, 0, 3, 1, 1, 0, 3, 3, 2, 2, 4, 4, 5, 5, 2]
    periodic = [3, 3, 0, 1, 1, 3, 0, 2, 1, 1, 0, 4, 5, 3, 7, 4, 8, 1, 1, 2, 0, 3, 1, 1, 0, 3, 3, 2, 2, 4, 4, 5, 5, 9]
    if x < len(first):
        return first[x]
    else:
        return periodic[(x - len(first)) % len(periodic)]


if __name__ == "__main__":
    n = 1000
    cache1 = compute_dn(n)
    for i in range(n):
        # print(cache[i])
        print(f"{cache1[i]}")
        assert cache1[i] == g1ncram(i)
