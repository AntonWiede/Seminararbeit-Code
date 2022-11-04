# Seminararbeit-Code

This program is used to find optimum procedure for every given rate p.


## Installation
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install necessary libraries

```bash
pip install tkinter
pip install pandas
pip install math
pip install random
```


## Usage GUI

entries: input min and max values

max_z = 1 : only singlestage pool-test

min_z = 2 : only multistage pool-test

lim_def : limit domain to all combinations with n/(t^^z-1) % 1 = 0 ("restloses Verfahren")

optimise : reduced tests as described in chapter 3.2

calculate : calculate all n, t, z combinations for each entry p and return lowest result

simulate : simulate all n, t, z combinations for each entry p and return lowest result

csv_calc : calculate all n, t, z in intervals [0.001; 0.01] (stepsize = 0.001) and [0.01; 0.5] (stepsize = 0.01) and export to csv file

sim_calc: calculate all n, t, z in intervals [0.001; 0.01] (stepsize = 0.001) and [0.01; 0.5] (stepsize = 0.01) and export to csv file

estimated simulation time: 180 sec. per value p for N = 1,000,000, standard settings on 3.6 GHz single thread

## Usage Terminal:

```python
import analysis
# N : sample_size, optimization : boolean ("reduziert"/"nicht reduziert"), 
# is_limited_definition : boolean ("restloses Verfahren), method : ["calc"(=calculate)/"sim"(=simulate)]
find_optimum(N, min_n, max_n, p, min_z, max_z, min_t, max_t, optimization,
                 is_limited_definition, method)
# returns optimal procedure in format : [T(n), optimal n, optimal, z, optimal t]
```
