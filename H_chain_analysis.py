import sys, os
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

os.environ['MATPLOTLIBRC'] = './config/matplotlibrc'

plt.rcParams['figure.figsize'] = (10,6)
plt.rcParams['lines.markersize'] = 10
plt.rcParams['lines.markeredgewidth'] = 2


def mean_time_slurm_file(input_filename):
    # we want to find the files where the energy evaluation is printed
    data = []
    with open(input_filename) as slurm_file:
        for line in slurm_file:
            if ' Energy evaluation ' in line:
                date_time = datetime.fromisoformat(line.split(',', 1)[0])
                idx = int(line.split(' Energy evaluation ')[1].split(' returned')[0])
                energy = float(line.split(' returned ')[1].strip())
                data.append((idx, energy, date_time))


    total_time = data[-1][2] - data[0][2]
    mean_time = total_time.total_seconds() / (len(data) - 1)

    total_square = 0
    prev = None
    for d in data:
        if prev == None:
            prev = d[2]
        else:
            time = (d[2] - prev).total_seconds()
            total_square += time ** 2
            prev = d[2]

    variance = total_square / (len(data) - 1) - (mean_time ** 2)
    std_dev = np.sqrt(variance)

    return mean_time, std_dev


def real_time_slurm_file(input_filename):
    # we want to find the files where the final 'real (wall) time' is printed
    real_time = 0
    with open(input_filename) as slurm_file:
        for line in slurm_file:
            if 'real\t' in line:
                print(line)
                time_str = line.strip().split('\t', 1)[1]
                time_arr = time_str.split('m') # Split on the m
                minutes = float(time_arr[0])
                seconds = float(time_arr[1][:-1]) # Last char is 's'
                real_time = minutes * 60 + seconds
        if real_time == 0:
            real_time = None
            print('Did not finish')

    return real_time


res_dir = './Data/'
settings_filename = 'H_chain_benchmarks.csv'

# Read the settings
settings_file = open(res_dir + settings_filename, 'r')
settings = []

for line in settings_file:
    setting = line.strip().split(',')
    settings.append(setting)
    print(setting)

mean_times = []
mean_time_std_devs = []
real_times = []

for setting in settings:
    jobid = setting[-1]
    
    try:
        mean_time, std_dev = mean_time_slurm_file(res_dir + 'slurm-' + str(jobid) + '.out')
        real_time = real_time_slurm_file(res_dir + 'slurm-' + str(jobid) + '.out')
        mean_times.append(mean_time)
        mean_time_std_devs.append(std_dev)
        real_times.append(real_time)
        print(f"-n: {setting[1]:>2}, N(H): {setting[0]:>2}, Mean time: {mean_time}, Mean time standard deviation: {std_dev}")
    except FileNotFoundError:
        mean_times.append(None)
        real_times.append(None)
        mean_time_std_devs.append(None)
        print(f'Could not find slurm file for jobid: {jobid}')



# Plot mean evaluation time
plt.figure(1)
plt.title('Mean evaluation time')
h_atoms = np.array(settings)[:,0].reshape(-1, 6)
n_flags = np.array(settings)[:,1].reshape(-1, 6)
data = np.array(mean_times).reshape(-1, 6)

print('\nMean times:')
print(data)

legends = []

for i in range(len(h_atoms[0,:])):
    print(h_atoms[:,i])
    try:
        plt.plot(n_flags[:,i], data[:,i])
    except TypeError:
        print('Cannot plot stupid data')
    legends.append(f'N(H) = {h_atoms[0,i]:>2},\nN(qb) = {int(h_atoms[0,i]) * 2 - 3:>2}')

plt.legend(legends, loc='lower right')
plt.grid(True, which='both')
plt.yscale('log')
plt.xscale('log')
plt.tight_layout()
plt.xlabel('Number of Tasks')
plt.ylabel('Seconds [s]')




plt.figure(2)
plt.title('Mean evaluation time standard deviatition')
data = np.array(mean_time_std_devs).reshape(-1, 6)

print('\nMean time standard deviation:')
print(data)

legends = []

for i in range(len(h_atoms[0,:])):
    print(h_atoms[:,i])
    try:
        plt.plot(n_flags[:,i], data[:,i])
    except TypeError:
        print('Cannot plot stupid data')
    legends.append(f'N(H) = {h_atoms[0,i]:>2},\nN(qb) = {int(h_atoms[0,i]) * 2 - 3:>2}')

plt.legend(legends, loc='best')
plt.grid(True, which='both')
#plt.yscale('log')
plt.tight_layout()
plt.xlabel('Number of Tasks')
plt.ylabel('Seconds [s]')




plt.figure(3)
plt.title('Total wall time')
data = np.array(real_times).reshape(-1, 6)

print('\nReal wall times:')
print(data)

legends = []

for i in range(len(h_atoms[0,:])):
    print(h_atoms[:,i])
    try:
        plt.plot(n_flags[:,i], data[:,i], marker='+')
    except TypeError:
        print('Cannot plot stupid data')
    if any(data[:,i]):
        legends.append(f'N(H) = {h_atoms[0,i]:>2},\nN(qb) = {int(h_atoms[0,i]) * 2 - 3:>2}')

plt.legend(legends, loc='best')
plt.grid(True, which='both')
#plt.yscale('log')
plt.tight_layout()
plt.xlabel('Number of Tasks')
plt.ylabel('Seconds [s]')

plt.show()