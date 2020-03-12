import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt


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
    mean_time = total_time / len(data)

    #for d in data:
    #    print(d)

    return mean_time


res_dir = './Results/'
settings_filename = 'H_chain_benchmarks.csv'

# Read the settings
settings_file = open(res_dir + settings_filename, 'r')
settings = []

for line in settings_file:
    setting = line.strip().split(',')
    settings.append(setting)
    print(setting)

data = []
for setting in settings:
    jobid = setting[-1]
    
    try:
        mean_time = mean_time_slurm_file(res_dir + 'slurm-' + str(jobid) + '.out')
        data.append(mean_time.total_seconds())
        print(f"-n: {setting[1]:>2}, N(H): {setting[0]:>2} Mean time: {mean_time}")
    except FileNotFoundError:
        data.append(None)
        print(f'Could not find slurm file for jobid: {jobid}')




h_atoms = np.array(settings)[:,0].reshape(-1, 6)
n_flags = np.array(settings)[:,1].reshape(-1, 6)
y_data = np.array(data).reshape(-1, 6)
print(h_atoms)
print(n_flags)
print(y_data)

legends = []

for i in range(len(h_atoms[0,:])):
    print(h_atoms[:,i])
    try:
        plt.plot(n_flags[:,i], y_data[:,i])
    except TypeError:
        print('Cannot plot stupid data')
    legends.append(f'N(H) = {h_atoms[0,i]:>2},\nN(qb) = {int(h_atoms[0,i]) * 2 - 3:>2}')

plt.legend(legends)
plt.grid(True)
plt.yscale('log')
plt.tight_layout()
plt.xlabel('Number of Tasks')
plt.ylabel('Seconds [s]')
plt.show()


