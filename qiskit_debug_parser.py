'''
Functions for parsing the output of a Qiskit logger for VQE runs with DEBUG level set.
'''
import numpy as np
from datetime import datetime

def get_mean_time(filename):
    # we want to find the files where the energy evaluation is printed
    data = []
    start = None
    with open(filename) as slurm_file:
        for line in slurm_file:
            if ' Submitting 1 circuits.' in line:
                start = datetime.fromisoformat(line.split(',', 1)[0])

            elif ' Energy evaluation ' in line:
                date_time = datetime.fromisoformat(line.split(',', 1)[0])
                idx = int(line.split(' Energy evaluation ')[1].split(' returned')[0])
                energy = float(line.split(' returned ')[1].strip())
                data.append((idx, energy, date_time))



    if len(data) < 1:
        return 0, 0

    total_time = data[-1][2] - start
    mean_time = total_time.total_seconds() / len(data)

    total_square = 0
    prev = start
    for d in data:
        time = (d[2] - prev).total_seconds()
        total_square += time ** 2
        prev = d[2]

    variance = total_square / len(data) - (mean_time ** 2)
    if variance < 0: 
        raise ValueError(f'Something has gonde horribly wrong, the calculated variance is negative: {variance}')
    std_dev = np.sqrt(variance)

    return mean_time, std_dev


def get_real_time(filename):
    # we want to find the files where the final 'real (wall) time' is printed
    real_time = 0
    with open(filename) as slurm_file:
        for line in slurm_file:
            if 'real\t' in line:
                time_str = line.strip().split('\t', 1)[1]
                time_arr = time_str.split('m') # Split on the m
                minutes = float(time_arr[0])
                seconds = float(time_arr[1][:-1]) # Last char is 's'
                real_time = minutes * 60 + seconds
        if real_time == 0:
            real_time = None
    #        print('Did not finish')

    return real_time


def get_number_evaluation_steps(filename):
    nbr_steps = 0
    with open(filename, 'r') as debug_file:
        for line in debug_file:
            if ' Energy evaluation ' in line:
                nbr_steps += 1

    return nbr_steps


def get_qubits(filename):
    nbr_qubits = None
    with open(filename, 'r') as debug_file:
        for line in debug_file:
            if '-- num_qubits: ' in line:
                nbr_qubits = int(line.strip().split('num_qubits: ')[1])


    return nbr_qubits

def get_nbr_circuit_parameters(filename):
    nbr_parameters = 0
    with open(filename, 'r') as debug_file:
        for line in debug_file:
            if '-- num_parameters: ' in line:
                nbr_parameters = int(line.strip().split('num_parameters: ')[1])


    return nbr_parameters
