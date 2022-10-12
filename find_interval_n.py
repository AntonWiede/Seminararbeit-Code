import calculation

N = 100  # doesn´t matter
p_list = [0.01, 0.05, 0.1, 0.15, 0.2, 0.3, 0.4]
n_list = list(range(2, 33))
z = 1  # single stage pool test
t = 1

for p in p_list:
    dict = {}
    for n in n_list:
        value = calculation.cost(N, n, p, t, z)
        if value <= N:
            dict[n] = value
    els = list(dict.items())
    print("p: " + str(p), "n: [" + str(els[0][0]) + ";" + str(els[-1][0]) + "]")






