def cost(N, n, p, t, z):
    counter = 0
    if z == 0:
        counter += 1
    if z >= 2:
        for i in range(z - 1):
            i += 1
            counter += ((t ** i) / n) * (1 - (1 - p) ** (n / (t ** (i - 1))))
    if z >= 1:
        counter += (1 / n)
        counter += (1 - (1 - p) ** (n / (t ** (z - 1))))
    counter = counter * N
    return counter


def cost_optimised(N, n, p, t, z):
    counter = 0

    if z == 0:
        counter += 1
    if z >= 2:
        for i in range(z - 1):
            i += 1
            counter += ((t ** i) / n) * (1 - (1 - p) ** (n / (t ** (i - 1))))
            counter -= ((t ** (i - 1)) / n) * (((1 - p) ** (n / (t ** i))) ** (t - 1)) * (1 - (1 - p) ** (n / (t ** i)))

    if z >= 1:
        counter += (1 / n)
        counter += (1 - (1 - p) ** (n / (t ** (z - 1))))
        counter -= ((t ** (z - 1)) / n) * ((1 - p) ** ((n / (t ** (z - 1))) - 1)) * p

    counter = counter * N
    return counter



