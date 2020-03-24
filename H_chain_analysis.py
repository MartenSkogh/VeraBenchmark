import sys, os
import numpy as np
from datetime import datetime

os.environ['MATPLOTLIBRC'] = './config/matplotlibrc'
data_dir = './Data/'
figure_dir = './Results/Figures/'
settings_filename = 'H_chain_benchmarks.csv'


import matplotlib.pyplot as plt
from qiskit_debug_parser import get_mean_time, get_real_time, get_qubits, get_number_evaluation_steps



# Read the settings
settings_file = open(data_dir + settings_filename, 'r')
settings = []

for line in settings_file:
    setting = line.strip().split(',')
    settings.append(setting)
    print(setting)

qubits = []
evaluation_steps = []
mean_times = []
mean_time_std_devs = []
real_times = []

for setting in settings:
    jobid = setting[-1]
    
    try:
        nbr_qubits = get_qubits(data_dir + f'circuit_nH={i}.out')
        nbr_evalutaion_steps = get_number_evaluation_steps(data_dir + f'circuit_nH={i}.out')
        mean_time, std_dev = get_mean_time(data_dir + 'slurm-' + str(jobid) + '.out')
        real_time = get_real_time(data_dir + 'slurm-' + str(jobid) + '.out')

        qubits.append(nbr_qubits)
        evaluation_steps.append(nbr_evalutaion_steps)
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
plt.savefig(figure_dir + 'mean_evaluation_time.png', bbox_inches='tight')




plt.figure(2)
plt.title('Mean evaluation time standard deviation')
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
plt.savefig(figure_dir + 'evaluation_time_standard_deviation.png', bbox_inches='tight')




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
plt.savefig(figure_dir + 'total_wall_time.png', bbox_inches='tight')

plt.show()
