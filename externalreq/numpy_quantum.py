import numpy as np

class QuantumState:
    def __init__(self, num_qubits):
        self.num_qubits = num_qubits
        self.state = np.zeros(2**num_qubits, dtype=complex)
        self.state[0] = 1  # Initialize to |0...0>

    def apply_gate(self, gate, target_qubit):
        # Apply a single-qubit gate
        full_gate = np.eye(2**self.num_qubits, dtype=complex)
        full_gate[target_qubit*2:(target_qubit+1)*2, target_qubit*2:(target_qubit+1)*2] = gate
        self.state = np.dot(full_gate, self.state)

    def measure(self, qubit):
        # Measure a single qubit
        prob_0 = sum(abs(self.state[i])**2 for i in range(2**self.num_qubits) if (i & (1 << qubit)) == 0)
        if np.random.random() < prob_0:
            outcome = 0
            norm = np.sqrt(prob_0)
        else:
            outcome = 1
            norm = np.sqrt(1 - prob_0)
        
        for i in range(2**self.num_qubits):
            if (i & (1 << qubit)) >> qubit != outcome:
                self.state[i] = 0
            else:
                self.state[i] /= norm
        
        return outcome


def main():
    state = QuantumState(2)
    hadamard = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
    state.apply_gate(hadamard, 0)
    result = state.measure(0)
    print(f"Measurement result: {result}")

if __name__ == "__main__":
    main()
