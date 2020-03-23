

filename = 'Data/H_chain_benchmarks.csv'

'''
rows = []
with open(filename, 'r+') as summary_file:
    rows = summary_file.readlines()
    summary_file.seek(0)
    for i, _ in enumerate(rows):
        cols = rows[i].strip().split(',')
        cols[-1] = 'slurm-' + cols[-1] + '.out\n'
        rows[i] = ','.join(cols)
        summary_file.write(rows[i])
'''


