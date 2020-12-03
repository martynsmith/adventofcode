range_start = 124075
range_end = 580769


def has_double(n):
    n = str(n)
    for i, c in enumerate(n):
        if i < len(n) - 1 and c == n[i+1]:
            if i == 0 or n[i-1] != c:  # behind
                if i == len(n) - 2 or n[i+2] != c: # ahead
                    return True
    return False


def is_incrementing(n):
    min = 0

    for c in str(n):
        if int(c) < min:
            return False
        min = int(c)

    return True


count = 0
for i in range(range_start, range_end):
    if not is_incrementing(i):
        continue
    if not has_double(i):
        continue
    count += 1

print(f"count = {count}")
