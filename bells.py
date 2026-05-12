from qiskit import QuantumCircuit
from qiskit.visualization import plot_histogram
from qiskit_aer import AerSimulator
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager # Otimiza o Circuito para Rodar em Hardware Real
from qiskit_ibm_runtime import SamplerV2 as Sampler, QiskitRuntimeService # O RuntimeService faz a conexão e o Sampler roda e coleta os dados

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


# bell.draw("mpl") # Mostrar o circuito visualmente

def run_circuit_and_get_counts(circuit, backend, shots=1000):
    pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
    isa_circuit = pm.run(circuit)

    sampler = Sampler(mode=backend)
    job = sampler.run([isa_circuit], shots=shots)
    result = job.result() # Aguarda o job ter os dados

    return result[0].data.meas.get_counts() # Extrai o dicionário de contagens (quantas vezes cada resultado apareceu)



# Definindo as configurações da classe
QiskitRuntimeService.save_account(
    channel="ibm_quantum_platform",
    token="vFkeYR0cFbpuERrY7cZHieexAacf_siBK_eXZ0YhyZl6",
    overwrite=True, # Sobreescreve se já tiver configurações anteriores
    set_as_default=True, # Define essa configuração como padrão
)
service = QiskitRuntimeService(channel="ibm_quantum_platform") # Apenas reelembrando a configuração padrão

backend = service.least_busy(operational=True, simulator=False, min_num_qubits=127)
# backend = AerSimulator() // Para rodar no simulador
print(backend.name)


# Rodando e plotando
for nome, circ in [("Φ+", bell_phi_plus), ("Φ−", bell_phi_minus), ("Ψ+", bell_psi_plus), ("Ψ−", bell_psi_minus)]:
    counts = run_circuit_and_get_counts(circ, backend, shots=1000)
    print(f"Estado {nome}: {counts}")