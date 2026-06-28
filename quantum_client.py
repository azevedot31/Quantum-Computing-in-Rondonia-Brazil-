# quantum_client.py
import requests, pickle, base64

class RemoteQuantumServer:
    def __init__(self, host: str, port: int = 8000):
        self.base_url = f"http://{host}:{port}"

    def health(self):
        r = requests.get(f"{self.base_url}/health", timeout=5)
        r.raise_for_status()
        return r.json()

    def _detect_framework(self, circuit) -> str:
        """Identifica de qual framework o circuito veio."""
        module_name = type(circuit).__module__
        if "qiskit" in module_name: return "qiskit"
        if "cirq" in module_name: return "cirq"
        if "pennylane" in module_name: return "pennylane"
        return "unknown"

    def run(self, circuit, shots: int = 1024):
        """Aceita um circuito de QUALQUER framework suportado pelo qBraid."""
        framework = self._detect_framework(circuit)
        payload = {
            "program_b64": base64.b64encode(pickle.dumps(circuit)).decode(),
            "source_framework": framework,
            "shots": shots
        }
        r = requests.post(f"{self.base_url}/run", json=payload, timeout=60)
        r.raise_for_status()
        return r.json()["counts"]
