from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import SamplerV2 as Sampler, QiskitRuntimeService

# Estados de Bell

bell_phi_plus = QuantumCircuit(2)
bell_phi_plus.h(0)
bell_phi_plus.cx(0, 1)
bell_phi_plus.measure_all()

bell_phi_minus = QuantumCircuit(2)
bell_phi_minus.h(0)
bell_phi_minus.z(0)
bell_phi_minus.cx(0, 1)
bell_phi_minus.measure_all()

bell_psi_plus  = QuantumCircuit(2)
bell_psi_plus.h(0)
bell_psi_plus.x(1)
bell_psi_plus.cx(0, 1)
bell_psi_plus.measure_all()

bell_psi_minus  = QuantumCircuit(2)
bell_psi_minus.h(0)
bell_psi_minus.x(1)
bell_psi_minus.z(0)
bell_psi_minus.cx(0, 1)
bell_psi_minus.measure_all()


print(bell_phi_plus)
print(bell_phi_minus)
print(bell_psi_plus)
print(bell_psi_minus)

def run_circuit_and_get_counts(circuit, backend, shots=1000):
    pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
    isa_circuit = pm.run(circuit)

    sampler = Sampler(mode=backend)
    job = sampler.run([isa_circuit], shots=shots)
    result = job.result()

    return result[0].data.meas.get_counts()


# QiskitRuntimeService.save_account(
#     channel="ibm_quantum_platform",
#     token="vFkeYR0cFbpuERrY7cZHieexAacf_siBK_eXZ0YhyZl6",
#     overwrite=True,
#     set_as_default=True,
# )
# service = QiskitRuntimeService(channel="ibm_quantum_platform")
# backend = service.least_busy(operational=True, simulator=False, min_num_qubits=127)

backend = AerSimulator()
print(backend.name)


# Rodando e plotando
for nome, circ in [("Φ+", bell_phi_plus), ("Φ−", bell_phi_minus), ("Ψ+", bell_psi_plus), ("Ψ−", bell_psi_minus)]:
    counts = run_circuit_and_get_counts(circ, backend, shots=1000)
    print(f"Estado {nome}: {counts}")
