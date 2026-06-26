from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit.quantum_info import SparsePauliOp
from qiskit_ibm_runtime import EstimatorV2 as Estimator
from qiskit.primitives import BackendEstimatorV2
from qiskit_aer.noise import NoiseModel



# -> MAPEAMENTO <-

# Parâmetros
J = 1.0    # acoplamento antiferromagnético (J > 0)
hx = -0.5  # força do campo transversal
obs = SparsePauliOp.from_list([("ZZ", J), ("XI", hx), ("IX", hx)])
qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.x(1)
qc.z(0)
print(qc)

# -> TRANSPILAÇÃO <-

backend = AerSimulator()
print(backend.name)
target = backend.target
pm = generate_preset_pass_manager(target=target, optimization_level=3)
qc_isa = pm.run(qc)

# Adaptar os observáveis ao layout do circuito transpilado
obs_isa = obs.apply_layout(layout=qc_isa.layout)
print(obs_isa)

# -> EXECUÇÃO <-

# estimator = Estimator(mode=backend)

# Alternativa: usar simulador Aer com modelo de ruído
noise_model = NoiseModel.from_backend(backend)
estimator_sim = BackendEstimatorV2(backend=backend)

job = estimator_sim.run([(qc_isa, obs_isa)])
resultado = job.result()
energia = resultado[0].data.evs

# -> PÓS PROCESSAMENTO E EXIBIÇÃO DOS DADOS <-

print("Energia: ", energia)
