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


def calc_optimum(N, min_n, max_n, p, max_z, min_t, max_t, optimization,
                 # not used for "analysis.py" only "find_interval_n.py"
                 is_limited_definition):  # calculate all values for one value p

    t_list = list(range(min_t, max_t + 1))
    z_list = list(range(1, max_z + 1))
    data = [N, 32, 1, 2]  # store optimal values 1: tests; 2: optimal n; 3 = optimal z, 4:optimal_t
    steps = len(t_list) * len(z_list)  # progress bar max
    step_size = 1 / steps
    progress = 0
    t_counter = 0

    for t in t_list:
        z_counter = 0
        t_counter += 1
        for z in z_list:
            n_counter = 0
            z_counter += 1
            n_list = list(range(min_n, max_n + 1))  # create list with all possible values for n
            erase_list = []
            if is_limited_definition:
                for n in n_list:
                    if ((n / (t ** z)) % 1) != 0:
                        erase_list.append(n)
                for n in erase_list:
                    n_list.remove(n)
            for n in n_list:  # list ist completed
                n_counter += 1
                progress += step_size / len(n_list)
                if not optimization:
                    value = cost(N, n, p, t, z)
                if optimization:
                    value = cost_optimised(N, n, p, t, z)
                if value < data[0]:
                    data[0] = value
                    data[1] = n
                    data[2] = z
                    data[3] = t
    if data[0] >= N:
        data[1] = 1
        data[2] = 0
        data[3] = 0
    return data
