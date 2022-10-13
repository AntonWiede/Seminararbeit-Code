# Seminararbeit-Code

This program is used to find optimum procedure for every given rate p.


## Installation
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install tkinter

```bash
pip install tkinter
```

## Usage

entries: input min and max values

max_z = 1 : only singlestage pool-test

min_z = 2 : only multistage pool-test

lim_def : limit domain to all combinations n/(t^^z-1) % 1 = 0

optimise : reduced tests as described in chapter

calculate : calculate all n, t, z combinations for each entry p and return lowest result

simulate : simulate all n, t, z combinations for each entry p and return lowest result

csv_calc : calculate all n, t, z in intervals [0.001; 0.01] (stepsize = 0.001) and [0.01; 0.5] (stepsize = 0.01) and export to csv file

sim_calc: calculate all n, t, z in intervals [0.001; 0.01] (stepsize = 0.001) and [0.01; 0.5] (stepsize = 0.01) and export to csv file

estimated simulation time: 
