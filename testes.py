#Primita do Qiskit
import numpy as np
from qiskit import QuantumCircuit

from qiskit.visualization import plot_histogram
from qiskit_aer import AerSimulator
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager # Otimiza o Circuito para Rodar em Hardware Real
from qiskit_ibm_runtime import SamplerV2 as Sampler, QiskitRuntimeService # O RuntimeService faz a conexão e o Sampler roda e coleta os dados

# Estado Psi-Minus
qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.x(1)
qc.z(0)

qc.measure_all()
# bell.draw("mpl") # Mostrar o circuito visualmente
print(qc)

def run_circuit_and_get_counts(circuit, backend, shots=1000):
    pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
    isa_circuit = pm.run(circuit)
    isa_circuit.draw("mpl") # Exibe o circuito otimizado
    print(isa_circuit) # Exibe o circuito otimizado

    sampler = Sampler(mode=backend)
    job = sampler.run([isa_circuit], shots=shots)
    result = job.result() # Aguarda o job ter os dados


    return result[0].data.meas.get_counts() # Extrai o dicionário de contagens (quantas vezes cada resultado apareceu)



# # Definindo as configurações da classe
# QiskitRuntimeService.save_account(
#     channel="ibm_quantum_platform",
#     token="vFkeYR0cFbpuERrY7cZHieexAacf_siBK_eXZ0YhyZl6",
#     overwrite=True, # Sobreescreve se já tiver configurações anteriores
#     set_as_default=True, # Define essa configuração como padrão
# )
# service = QiskitRuntimeService(channel="ibm_quantum_platform") # Apenas reelembrando a configuração padrão

# backend = service.least_busy(operational=True, simulator=False, min_num_qubits=127)
backend = AerSimulator() # Para rodar no simulador
print(backend.name)

counts = run_circuit_and_get_counts(qc, backend, shots=1000)
print(counts)



# # Rodando e plotando
# for nome, circ in [("Φ+", bell_phi_plus), ("Φ−", bell_phi_minus), ("Ψ+", bell_psi_plus), ("Ψ−", bell_psi_minus)]:
#     counts = run_circuit_and_get_counts(circ, backend, shots=1000)
#     print(f"Estado {nome}: {counts}")
