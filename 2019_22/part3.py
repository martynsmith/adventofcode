D = 119315717514047
X = 2020  # i
Y = 95589349674159  # f(i)
Z = 9414091377132  # f(f(i))
n = 101741582076661


def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)


def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m


A = (Y - Z) * modinv(X - Y + D, D) % D
B = (Y - A * X) % D
print(A, B)

def f(i):
    return (A * i + B) % D

print(X)
print()
print(Y)
print(f(X))
print()
print(Z)
print(f(f(X)))

print()

print((pow(A, n, D)*X + (pow(A, n, D)-1) * modinv(A-1, D) * B) % D)
