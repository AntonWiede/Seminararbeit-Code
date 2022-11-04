import random
import math

counter_tests = 0
counter_positive = 0
counter_negative_subgroups = []
counter_test1 = 0


def partition(lst, f):  # divide list in even gropus

    size = math.ceil(len(lst) / f)
    return [lst[i:i + size] for i in range(0, len(lst), size)]



def count(list, z, t, i):  # i should be 0 for start
    global counter_tests
    global counter_positive
    if len(list) != 1 and i <= z - 1:  # condition for division
        counter_tests += 1  # count group tests
        if 1 in list:  # group test

            if i == z - 1:  # last pool before single tests
                count(list, z, t, i + 1)
            else:
                list = partition(list, t)  # split list into sub-groups

                for e in list:
                    count(e, z, t, i + 1)  # recursive function
        else:
            pass

    else:
        #        counter_positive += list.count(1) #check for all positives
        counter_tests += len(list)  # single tests
    #        print("+" + str(len(list)))

    pass


def count_optimized(list, z, t, i):  # i should be 0 for start
    global counter_tests
    global counter_negative_subgroups
    global counter_test1
    for x in range(i + 1, len(counter_negative_subgroups)):
        counter_negative_subgroups[x] = 0
    if counter_negative_subgroups[i] == t - 1 and i >= 1:  # 1 test can be skipped
        if len(list) != 1 and i <= z - 1:
            if 1 in list:
                if i == z - 1:
                    count_optimized(list, z, t, i + 1)
                else:
                    list = partition(list, t)
                    for e in list:
                        count_optimized(e, z, t, i + 1)
        else:
            if len(list) > 1:
                counter_negative_single_tests = 0  # single tests
                for i in range(0, len(list) - 1):
                    counter_negative_single_tests += list[i]
                if counter_negative_single_tests == 0:
                    counter_tests += len(list) - 1
                else:
                    counter_tests += len(list)
            else:
                counter_tests += len(list)
    else:

        if len(list) != 1 and i <= z - 1:  # condition for division
            counter_tests += 1
            if 1 in list:
                if i == z - 1:
                    count_optimized(list, z, t, i + 1)
                else:
                    list = partition(list, t)
                    for e in list:
                        count_optimized(e, z, t, i + 1)
            else:
                counter_negative_subgroups[i] = counter_negative_subgroups[i] + 1
        else:  # single tests
            if len(list) > 1:
                counter_negative_single_tests = 0  # counting single tests for optimization
                for i in range(0, len(list) - 1):
                    counter_negative_single_tests += list[i]  # if list [i] != 0 next condition wo't be matched
                if counter_negative_single_tests == 0:
                    counter_tests += len(list) - 1
                else:
                    counter_tests += len(list)
            else:
                counter_tests += len(list)
    return counter_tests


def simulation(N, n, p, t, z, optimization):  # lmt_df = limited definition
    global counter_tests
    global counter_negative_subgroups
    counter_tests = 0
    Matrix = [0] * N
    counter_negative_subgroups = [0] * (z + 2)
    for x in range(len(Matrix)):
        var = random.random()
        if var <= p:
            Matrix[x] = 1

    Matrix2 = partition(Matrix, math.ceil(N / n))  # divided matrix

    for e in Matrix2:
        if optimization:
            count_optimized(e, z, t, 0)
        if not optimization:
            count(e, z, t, 0)
    return counter_tests

