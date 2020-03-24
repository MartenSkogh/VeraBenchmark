import numpy as np
import matplotlib.pyplot as plt

from qiskit_debug_parser import get_mean_time, get_qubits, get_number_evaluation_steps, get_nbr_circuit_parameters, get_real_time

data_dir = './Data/'

files = [
         './Data/circuit_nH=1.out',
         './Data/circuit_nH=2.out',
         './Data/circuit_nH=3.out',
         './Data/circuit_nH=4.out',
         './Data/circuit_nH=5.out',
         './Data/circuit_nH=6.out',
         './Data/circuit_nH=7.out',
         './Data/circuit_nH=8.out',
         './Data/slurm-1068103.out',
         './Data/slurm-1068104.out',
         './Data/slurm-1068105.out',
         './Data/slurm-1068106.out',
         './Data/slurm-1068107.out',
         './Data/slurm-1068108.out',
         './Data/slurm-1068109.out',
         './Data/slurm-1068110.out',
         './Data/slurm-1068111.out',
         './Data/slurm-1068112.out',
         './Data/slurm-1068113.out',
         './Data/slurm-1068114.out',
         './Data/slurm-1068115.out',
         './Data/slurm-1068116.out',
         './Data/slurm-1068117.out',
         './Data/slurm-1068118.out',
         './Data/slurm-1068119.out',
         './Data/slurm-1068120.out',
         './Data/slurm-1068121.out',
         './Data/slurm-1068122.out',
         './Data/slurm-1068123.out',
         './Data/slurm-1068124.out',
         './Data/slurm-1068125.out',
         './Data/slurm-1068126.out',
         './Data/slurm-1068127.out',
         './Data/slurm-1068128.out',
         './Data/slurm-1068129.out',
         './Data/slurm-1068130.out',
         './Data/slurm-1068131.out',
         './Data/slurm-1068132.out',
         './Data/slurm-1068133.out',
         './Data/slurm-1068134.out',
         './Data/slurm-1068135.out',
         './Data/slurm-1068136.out',
         './Data/slurm-1068137.out',
         './Data/slurm-1068138.out',
         './Data/slurm-1068144.out'
         ]

mean_times = []
mean_times_std_dev = []
qubits = []
evaluation_steps = []
parameters = []
wall_times = []

# Files that have run on small systems (no parallel processing)
for filename in files:
    mean_time, std_dev = get_mean_time(filename)
    nbr_qubits = get_qubits(filename)
    nbr_evalutaion_steps = get_number_evaluation_steps(filename)
    nbr_circuit_params = get_nbr_circuit_parameters(filename)
    wall_time = get_real_time(filename)

    mean_times.append(mean_time)
    mean_times_std_dev.append(std_dev)
    qubits.append(nbr_qubits)
    evaluation_steps.append(nbr_evalutaion_steps)
    parameters.append(nbr_circuit_params)
    wall_times.append(wall_time)

print(qubits[0], qubits[0] == None)

data = [mean_times, mean_times_std_dev, qubits, evaluation_steps, parameters, wall_times]
#data_sorted = sorted(data, key=lambda x: [x[1:2], 0, x[3:]] if x[2] is None else x)
data_sorted = sorted(zip(*data), key=lambda x: 0 if x[2] is None else x[2])


for mt, sd, qubit, steps, params, wt in data_sorted:
    print(f'Qubits: {0 if qubit is None else qubit:2d}, Parameters: {params:4d}, Evaluation steps: {steps:5d}, Mean time per step: {mt:8.2f}, Total time: {"dnf" if wt is None else wt:>10}, Mean time std. deviation: {sd:7.2f}')

plt.plot(qubits, evaluation_steps)
plt.show()
