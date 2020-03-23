"""
Using this code you will be able to reduce the number of qubits by finding underlying Z2 symmetries of the Hamiltonian.
The paper expaining the qubit reduction technique is:
by S. Bravyi et al. "Tapering off qubits to simulate fermionic Hamiltonians"
arXiv:1701.08213
This will drastically speed up all the simulations.
"""

import sys

import logging
from qiskit.aqua import set_qiskit_aqua_logging

# provides all information (can be too much text)
# set_qiskit_aqua_logging(logging.DEBUG)

# provides less information than DEBUG mode
set_qiskit_aqua_logging(logging.DEBUG)

from qiskit import Aer
from qiskit.aqua import QuantumInstance
from qiskit.aqua.operators import Z2Symmetries
from qiskit.aqua.algorithms.adaptive import VQE
from qiskit.aqua.algorithms import ExactEigensolver
from qiskit.aqua.components.optimizers import SLSQP, L_BFGS_B
from qiskit.chemistry.core import Hamiltonian, TransformationType, QubitMappingType
from qiskit.chemistry.drivers import PySCFDriver, UnitsType
from qiskit.chemistry.components.variational_forms import UCCSD
from qiskit.chemistry.components.initial_states import HartreeFock
from qiskit.chemistry.drivers import HFMethodType

from qiskit import QuantumCircuit
from qiskit.circuit import Parameter

from qiskit import transpile


def generate_hydrogen_chain(n, spacing):
    offset = - (n - 1) * spacing / 2 # make symmetric
    mol_str = ''
    for i in range(n):
        pos = i * spacing + offset
        mol_str += f'H {pos} 0.0 0.0; '

    return mol_str

n = int(sys.argv[1])
molecule = generate_hydrogen_chain(n, 0.735)

charge = 0
spin = n % 2

driver = PySCFDriver(atom=molecule,
                     unit=UnitsType.ANGSTROM,
                     charge=charge,
                     spin=spin,
                     hf_method=HFMethodType.ROHF,
                     basis='sto3g')
#                     basis='sto6g')
#                     basis='631g')

qmolecule = driver.run()

core = Hamiltonian(transformation=TransformationType.FULL,
                   qubit_mapping=QubitMappingType.PARITY,
                   two_qubit_reduction=True,
                   freeze_core=False,
                   orbital_reduction=[])

qubit_op, _ = core.run(qmolecule)

# find the symmetries of the Hamiltonian
z2_symmetries = Z2Symmetries.find_Z2_symmetries(qubit_op)
tapered_ops = z2_symmetries.taper(qubit_op)
smallest_idx = 0

# Prior knowledge of which tapered_op has ground state
# or you can find the operator that has the ground state by diagonalising each operator
#smallest_eig_value = 99999999999999
#smallest_idx = -1
#for idx in range(len(tapered_ops)):
#    print('operator number: ', idx)
#    ee = ExactEigensolver(tapered_ops[idx], k=1)
#    curr_value = ee.run()['energy']
#    if curr_value < smallest_eig_value:
#        smallest_eig_value = curr_value
#        smallest_idx = idx
#print('Operator number: ', smallest_idx, ' contains the ground state.')
# the tapered Hamiltonian operator
the_tapered_op = tapered_ops[smallest_idx]
# optimizers
optimizer = SLSQP(maxiter=50000)
# optimizer = L_BFGS_B(maxiter=1000)

# initial state
init_state = HartreeFock(num_qubits=the_tapered_op.num_qubits,
                         num_orbitals=core._molecule_info['num_orbitals'],
                         qubit_mapping=core._qubit_mapping,
                         two_qubit_reduction=core._two_qubit_reduction,
                         num_particles=core._molecule_info['num_particles'],
                         sq_list=the_tapered_op.z2_symmetries.sq_list)

# UCCSD Ansatz
var_form = UCCSD(num_qubits=the_tapered_op.num_qubits,
                 depth=1,
                 num_orbitals=core._molecule_info['num_orbitals'],
                 num_particles=core._molecule_info['num_particles'],
                 active_occupied=None,
                 active_unoccupied=None,
                 initial_state=init_state,
                 qubit_mapping=core._qubit_mapping,
                 two_qubit_reduction=core._two_qubit_reduction,
                 num_time_slices=1,
                 z2_symmetries=the_tapered_op.z2_symmetries,
                 shallow_circuit_concat=False)
#                 force_no_tap_excitation=True,
#                 method_doubles='succ',
#                 excitation_type='d',
#                 same_spin_doubles=False)

# set up VQE
algo = VQE(the_tapered_op, var_form, optimizer)

# Choose the backend (use Aer instead of BasicAer)
backend = Aer.get_backend('statevector_simulator')
quantum_instance = QuantumInstance(backend=backend, optimization_level=1)

# run the algorithm
algo_result = algo.run(quantum_instance)

# get the results
_, result = core.process_algorithm_result(algo_result)
print(result)
