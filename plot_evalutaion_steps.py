import numpy as np
import matplotlib.pyplot as plt

from qiskit_debug_parser import get_qubits, get_number_evaluation_steps, get_nbr_circuit_parameters

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

qubits = []
evaluation_steps = []
parameters = []

# Files that have run on small systems (no parallel processing)
for filename in files:
    nbr_qubits = get_qubits(filename)
    nbr_evalutaion_steps = get_number_evaluation_steps(filename)
    nbr_circuit_params = get_nbr_circuit_parameters(filename)

    qubits.append(nbr_qubits)
    evaluation_steps.append(nbr_evalutaion_steps)
    parameters.append(nbr_circuit_params)

print(qubits[0], qubits[0] == None)

sorted_qubits, sorted_steps, sorted_params = zip(*sorted(zip(qubits, evaluation_steps, parameters), key=lambda x: (0,x[1], x[2]) if x[0] is None else x))

for qubit, steps, params in zip(sorted_qubits, sorted_steps, sorted_params):
    print(f'Qubits: {qubit}, Parameters: {params}, Evaluation steps: {steps}')

plt.plot(qubits, evaluation_steps)
plt.show()
