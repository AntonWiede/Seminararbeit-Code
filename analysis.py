from tkinter import *
from tkinter import ttk
import calculation
import simulation
import pandas as pd

# standards
dif_p = 7  # number of different p values
p_standards = [0.001, 0.01, 0.05, 0.1, 0.2, 0.3, 0.4]  # standard p values
min_z_standard = 1
max_z_standard = 5
min_n_standard = 2
max_n_standard = 32
min_t_standard = 2
max_t_standard = 10
is_optimization = False  # default button settings
is_limited_Definition = False


def change_opt_bool(self):  # opt button change
    global is_optimization
    if is_optimization:
        is_optimization = False
        self.config(relief=RAISED)
    else:
        is_optimization = True
        self.config(relief=SUNKEN)


def change_lim_bool(self):  # lim button change
    global is_limited_Definition
    if is_limited_Definition:
        self.config(relief=RAISED)
        is_limited_Definition = False
    else:
        is_limited_Definition = True
        self.config(relief=SUNKEN)


def find_optimum(N, min_n, max_n, p, min_z, max_z, min_t, max_t, optimization,
                 is_limited_definition, method):  # calculate all values for one value p
    progressbar['value'] = 0
    root.update_idletasks()
    z_list = list(range(min_z, max_z + 1))
    t_list = list(range(min_t, max_t + 1))
    data = [N * 10, 32, 1, 2]  # store optimal values 1: tests; 2: optimal n; 3 = optimal z, 4:optimal_t
    steps = 0
    for z in z_list:  # all possible combinations of t and z
        if z == 1:
            steps += max_n - min_n + 1
        else:
            for t in t_list:
                n_list = list(range(min_n, max_n + 1))
                for n in n_list:
                    if is_limited_definition:
                        if n % (t ** (z - 1)) == 0 and ((n / (t ** (z - 1))) != 1):
                            steps += 1  # max progressbar
                    if not is_limited_definition:
                        if t ** (z - 1) <= n:
                            steps += 1
    step_size = 1 / steps  # ln49-62 progressbar step_size

    for z in z_list:
        t_list = list(range(min_t, max_t + 1))
        if z == 1:  # no different t values for z = 1
            t_list = [1]
        for t in t_list:
            n_list = list(range(min_n, max_n + 1))  # create list with all possible values for n
            erase_list = []
            if is_limited_definition:
                for n in n_list:
                    if ((n / (t ** (z - 1))) % 1) != 0 or ((n / (t ** (z - 1))) == 1):  # all n not included in lim def
                        erase_list.append(n)
            if not is_limited_definition:  # all impossible n 
                for n in n_list:
                    if t ** (z - 1) > n or ((n / (t ** (z - 1))) == 1):
                        erase_list.append(n)
            for n in erase_list:  # create final n list
                n_list.remove(n)
            for n in n_list:  # list ist completed
                progressbar['value'] += step_size * 100
                root.update_idletasks()  # update progessbar
                if method == "calc":
                    if not optimization:
                        value = calculation.cost(N, n, p, t, z)
                    if optimization:
                        value = calculation.cost_optimised(N, n, p, t, z)
                if method == "sim":
                    if not optimization:
                        value = simulation.simulation(N, n, p, t, z, optimization)
                    if optimization == 1:
                        value = simulation.simulation(N, n, p, t, z, optimization)
                if value < data[0]:  # insert new optimum
                    data[0] = value
                    data[1] = n
                    data[2] = z
                    data[3] = t
        if data[0] >= N and min_n <= 1 and min_z <= 1:  # no optimum found
            data[0] = N
            data[1] = 1
            data[2] = 0
            data[3] = 0
    return data


def read_and_fill(
        method):  # method[0]: "calc" = calculate; "sim" = simulate; method[1]: window = normal output; csv = csv output
    global is_limited_Definition, optimum_value, is_optimization
    N = int(e_N.get())
    min_z = int(e_min_z.get())
    max_z = int(e_max_z.get())
    min_n = int(e_min_n.get())  # draw all values from entries
    max_n = int(e_max_n.get())
    min_t = int(e_min_t.get())
    max_t = int(e_max_t.get())
    p = []
    for i in range(dif_p):
        p.append(float(ir_entries[i].get()))

    if method[1] == "window":
        for x in range(dif_p):
            p2 = p[x]
            if method[0] == "calc":
                optimum_value = find_optimum(N, min_n, max_n, p2, min_z, max_z, min_t, max_t, is_optimization,
                                             is_limited_Definition, "calc")
            if method[0] == "sim":
                optimum_value = find_optimum(N, min_n, max_n, p2, min_z, max_z, min_t, max_t, is_optimization,
                                             is_limited_Definition, "sim")
            # calculate optimal value from calculation.py or simulation.py
            optimum_text = "n = " + str(optimum_value[1]) + " / z = " + str(optimum_value[2]) + " / t = " + str(
                optimum_value[3])  # combine optimums to one string

            optimum_entries[x].delete(0, END)  # insert optimums
            optimum_entries[x].insert(0, optimum_text)
            test_entries[x].delete(0, END)  # insert t(n) values
            test_entries[x].insert(0, str(round(optimum_value[0])))

            saving1 = 1 - (optimum_value[0] / N)  # round up and insert savings
            saving2 = str(round(saving1 * 100, 1)) + "%"
            savings_entries[x].delete(0, END)
            savings_entries[x].insert(0, saving2)
    if method[1] == "csv":
        data = []
        all_p = []
        small_p = list(range(1, 10))
        for x in small_p:
            all_p.append(x / 1000)  # create list of all p's
        normal_p = list(range(1, 51))
        for x in normal_p:
            all_p.append(x / 100)
        for p in all_p:

            if method[0] == "calc":
                optimum_value = find_optimum(N, min_n, max_n, p, min_z, max_z, min_t, max_t, is_optimization,
                                             is_limited_Definition, "calc")
            if method[0] == "sim":
                optimum_value = find_optimum(N, min_n, max_n, p, min_z, max_z, min_t, max_t, is_optimization,
                                             is_limited_Definition, "sim")
            optimum_text = "n = " + str(optimum_value[1]) + " / z = " + str(optimum_value[2]) + " / t = " + str(
                optimum_value[3])  # combine optimums to one string
            savings = 1 - optimum_value[0] / N
            savings2 = savings * 100
            savings3 = str(round(savings2, 1)) + "%"
            data.append(
                [p, int(round(optimum_value[0], 0)), savings3, optimum_value[1], optimum_value[2], optimum_value[3]])
        df = pd.DataFrame(data)

        #        df[1] = pd.to_numeric(df[1])
        df.to_csv("data_multistage_opt.csv", index=False)


root = Tk("Pool Tests")  # user interface ln. 174-270

root.geometry("1000x300")

l_N = Label(root, text="N")  # entry for N
l_N.grid(row=0, column=0)
e_N = Entry(root)
e_N.grid(row=0, column=1)
e_N.insert(0, "10000")

l_min_n = Label(root, text="min_n")  # entry for min n
l_min_n.grid(row=0, column=2)
e_min_n = Entry(root)
e_min_n.grid(row=0, column=3)
e_min_n.insert(0, min_n_standard)
l_max_n = Label(root, text="max_n")  # entry for max_n
l_max_n.grid(row=1, column=2)
e_max_n = Entry(root)
e_max_n.grid(row=1, column=3)
e_max_n.insert(0, max_n_standard)

l_min_z = Label(root, text="min_z")  # entry for min n
l_min_z.grid(row=1, column=0)
e_min_z = Entry(root)
e_min_z.grid(row=1, column=1)
e_min_z.insert(0, min_z_standard)
l_max_z = Label(root, text="max_z")  # entry for max_z
l_max_z.grid(row=2, column=0)
e_max_z = Entry(root)
e_max_z.grid(row=2, column=1)
e_max_z.insert(0, max_z_standard)

place_holder = Label(root, text="")
place_holder.grid(row=3, column=0)

progressbar = ttk.Progressbar(root, orient='horizontal', mode='determinate', length=200)
progressbar.grid(row=2, column=4, columnspan=2)

b_optimization = Button(root, text="optimization", command=lambda: change_opt_bool(
    b_optimization))  # Buttons for selecting optimization and limited area of definition
b_optimization.grid(row=2, column=2)
b_lim_d = Button(root, text="limited D", command=lambda: change_lim_bool(b_lim_d))
b_lim_d.grid(row=2, column=3)

l_min_t = Label(root, text="min_t")  # entry for t
l_min_t.grid(row=0, column=4)
e_min_t = Entry(root)
e_min_t.grid(row=0, column=5)
e_min_t.insert(0, min_t_standard)
l_max_t = Label(root, text="max_t")  # entry for t
l_max_t.grid(row=1, column=4)
e_max_t = Entry(root)
e_max_t.grid(row=1, column=5)
e_max_t.insert(0, max_t_standard)

l_infection_rate = Label(root, text="p     ")  # Label left side
l_infection_rate.grid(row=4, column=0)
l_optimum = Label(root, text="optimum")
l_optimum.grid(row=5, column=0)
l_tests = Label(root, text="tests")
l_tests.grid(row=6, column=0)
l_savings = Label(root, text="savings")
l_savings.grid(row=7, column=0)

ir_entries = []  # ir = infection rate
for i in range(dif_p):
    e = Entry(root)
    e.grid(row=4, column=i + 1)
    e.insert(0, str(p_standards[i]))
    ir_entries.append(e)

# toggle buttons lim_def and reduced


b_calculate = Button(root, text="calculate", command=lambda: read_and_fill(["calc", "window"]))
b_calculate.grid(row=0, column=6)
b_simulate = Button(root, text="simulate", command=lambda: read_and_fill(["sim", "window"]))
b_simulate.grid(row=1, column=6)
b_create_csv_calc = Button(root, text="csv calc", command=lambda: read_and_fill(["calc", "csv"]))
b_create_csv_calc.grid(row=0, column=7)
b_create_csv_sim = Button(root, text="csv sim", command=lambda: read_and_fill(["sim", "csv"]))
b_create_csv_sim.grid(row=1, column=7)

optimum_entries = []
for i in range(dif_p):  # optimum entries
    e = Entry(root)
    e.grid(row=5, column=i + 1)
    optimum_entries.append(e)

test_entries = []
for i in range(dif_p):  # test value entries
    e = Entry(root)
    e.grid(row=6, column=i + 1)
    test_entries.append(e)

savings_entries = []
for i in range(dif_p):  # saving value entries
    e = Entry(root)
    e.grid(row=7, column=i + 1)
    savings_entries.append(e)

root.mainloop()
