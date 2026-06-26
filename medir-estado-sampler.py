from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import SamplerV2 as Sampler, QiskitRuntimeService
from qiskit.primitives import BackendSamplerV2
from qiskit_aer.noise import NoiseModel

# -> MAPEAMENTO <-

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.measure_all()
print(qc)

# -> TRANSPILAÇÃO <-

#service = QiskitRuntimeService(channel="ibm_quantum_platform", token="xxx")
#backend = service.least_busy(operational=True, simulator=False, min_num_qubits=127)
backend = AerSimulator()
print(backend.name)
target = backend.target
pm = generate_preset_pass_manager(target=target, optimization_level=3)
qc_isa = pm.run(qc)

# -> EXECUÇÃO <-

# sampler = Sampler(mode=backend)

# Alternativa: usar um simulador com modelo de ruído do backend real
noise_model = NoiseModel.from_backend(backend)
backend_sim = AerSimulator(noise_model=noise_model)
sampler_sim = BackendSamplerV2(backend=backend_sim)

job = sampler_sim.run([qc_isa], shots=1000)
resultado = job.result()
contagem = resultado[0].data.meas.get_counts()

# -> PÓS PROCESSAMENTO E EXIBIÇÃO DOS DADOS <-

print("contagens: ", contagem)
