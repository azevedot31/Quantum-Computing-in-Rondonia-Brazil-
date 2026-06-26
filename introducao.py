# import sys
# import qiskit
# import qiskit_aer
# import qiskit_ibm_runtime

# Para verificar se está  tudo instalado e ok
# print("Python:", sys.version.split()[0])
# print("qiskit:", qiskit.__version__)
# print("qiskit-aer:", qiskit_aer.__version__)
# print("qiskit-ibm-runtime:", qiskit_ibm_runtime.__version__)

from qiskit import QuantumCircuit
from qiskit.visualization import plot_histogram
from qiskit_aer import AerSimulator
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
# Otimiza o Circuito para Rodar em Hardware Real
from qiskit_ibm_runtime import SamplerV2 as Sampler, QiskitRuntimeService
# O RuntimeService faz a conexão e o Sampler roda e coleta os dados


bell = QuantumCircuit(2) # Circuito como objeto
bell.h(0)
bell.cx(0, 1)
bell.measure_all()
# bell.draw("mpl") # Mostrar o circuito visualmente em uma interface gráfica
print(bell)


# Otimiza, roda e pega as contagens do circuitos ou lista de circuitos
def run_circuit_and_get_counts(circuit, backend, shots=1000):
    pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
    isa_circuit = pm.run(circuit)

    sampler = Sampler(mode=backend)
    job = sampler.run([isa_circuit], shots=shots)
    result = job.result() # Aguarda o job ter os dados

    return result[0].data.meas.get_counts() # Extrai o dicionário de contagens (quantas vezes cada resultado apareceu)
    # resultado -> circuito 0 -> dados -> registrador meas -> pegue as constagens

# Definindo as configurações da conecção com o servidor (configuração de classe)
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

# Rodando em um QPU real
counts = run_circuit_and_get_counts(bell, backend, shots=5000)
#plot_histogram(counts) # Para mostrar um histograma em GUI
print(counts)
