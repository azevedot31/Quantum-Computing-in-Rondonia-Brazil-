from quantum_client import RemoteQuantumServer
server = RemoteQuantumServer(host="localhost", port=8000)  # via túnel SSH

# --- Vindo do Qiskit ---
from qiskit import QuantumCircuit
qc = QuantumCircuit(2, 2); qc.h(0); qc.cx(0,1); qc.measure_all()
print(server.run(qc, shots=1000))

# --- Vindo do Cirq ---
import cirq
q0, q1 = cirq.LineQubit.range(2)
circuit_cirq = cirq.Circuit(cirq.H(q0), cirq.CNOT(q0, q1), cirq.measure(q0, q1))
print(server.run(circuit_cirq, shots=1000))

# --- Vindo do PennyLane ---
import pennylane as qml
with qml.tape.QuantumTape() as tape:
    qml.Hadamard(wires=0)
    qml.CNOT(wires=[0, 1])
    qml.measure(wires=0)
    qml.measure(wires=1)
print(server.run(tape, shots=1000))
