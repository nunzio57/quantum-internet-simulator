import numpy as np

class Qubit:
    def __init__(self, alpha=1+0j, beta=0+0j):
        """
        Rappresenta un singolo qubit come vettore di stato.
        alpha = ampiezza di |0⟩
        beta = ampiezza di |1⟩
        """
        state = np.array([alpha, beta], dtype=complex)
        # normalizzazione
        norm = np.linalg.norm(state)
        self.state = state / norm

    @property
    def alpha(self):
        return self.state[0]

    @property
    def beta(self):
        return self.state[1]


    # Matrici dei gate
    X = np.array([[0, 1],
                  [1, 0]], dtype=complex)

    Z = np.array([[1, 0],
                  [0, -1]], dtype=complex)

    H = np.array([[1, 1],
                  [1, -1]], dtype=complex) / np.sqrt(2)

    I = np.eye(2, dtype=complex)

    def apply_gate(self, gate):
        """Applica un gate 2x2 al qubit"""
        self.state = gate @ self.state

    def x_gate(self):
        self.apply_gate(Qubit.X)

    def z_gate(self):
        self.apply_gate(Qubit.Z)

    def h_gate(self):
        self.apply_gate(Qubit.H)

    def measure(self):
        """
        Misura il qubit — collassa in 0 o 1.
        Restituisce il risultato e aggiorna lo stato.
        """
        prob_0 = abs(self.state[0])**2
        result = 0 if np.random.random() < prob_0 else 1
        if result == 0:
            self.state = np.array([1+0j, 0+0j])
        else:
            self.state = np.array([0+0j, 1+0j])
        return result

    def fidelity(self, other):
        """
        Calcola la fidelity tra questo qubit e un altro.
        F = |⟨ψ|φ⟩|²
        """
        return abs(np.dot(self.state.conj(), other.state))**2

    def __repr__(self):
        return f"Qubit(α={self.state[0]:.3f}, β={self.state[1]:.3f})"


class TwoQubitSystem:
    """
    Rappresenta un sistema di due qubit come vettore di stato a 4 componenti.
    Base: |00⟩, |01⟩, |10⟩, |11⟩
    """

    # Gate CNOT come matrice 4x4
    CNOT = np.array([[1, 0, 0, 0],
                     [0, 1, 0, 0],
                     [0, 0, 0, 1],
                     [0, 0, 1, 0]], dtype=complex)

    def __init__(self, qubit_a, qubit_b):
        """
        Crea un sistema a due qubit dal prodotto tensoriale di qubit_a e qubit_b.
        """
        self.state = np.kron(qubit_a.state, qubit_b.state)

    @classmethod
    def epr_pair(cls):
        """
        Crea una coppia EPR |Φ+⟩ = (|00⟩ + |11⟩) / √2
        """
        system = cls.__new__(cls)
        system.state = np.array([1, 0, 0, 1], dtype=complex) / np.sqrt(2)
        return system

    def apply_gate_first(self, gate):
        """Applica un gate 2x2 al primo qubit"""
        full_gate = np.kron(gate, Qubit.I)
        self.state = full_gate @ self.state

    def apply_gate_second(self, gate):
        """Applica un gate 2x2 al secondo qubit"""
        full_gate = np.kron(Qubit.I, gate)
        self.state = full_gate @ self.state

    def apply_cnot(self):
        """Applica CNOT con il primo qubit come controllo"""
        self.state = TwoQubitSystem.CNOT @ self.state

    def measure_first(self):
        """
        Misura il primo qubit.
        Restituisce il risultato e collassa lo stato.
        """
        # probabilità di misurare 0 sul primo qubit
        prob_0 = abs(self.state[0])**2 + abs(self.state[1])**2
        result = 0 if np.random.random() < prob_0 else 1
        if result == 0:
            # collassa — normalizza solo i componenti |0x⟩
            new_state = np.array([self.state[0], self.state[1], 0, 0], dtype=complex)
        else:
            # collassa — normalizza solo i componenti |1x⟩
            new_state = np.array([0, 0, self.state[2], self.state[3]], dtype=complex)
        norm = np.linalg.norm(new_state)
        self.state = new_state / norm
        return result

    def measure_second(self):
        """
        Misura il secondo qubit.
        Restituisce il risultato e collassa lo stato.
        """
        prob_0 = abs(self.state[0])**2 + abs(self.state[2])**2
        result = 0 if np.random.random() < prob_0 else 1
        if result == 0:
            new_state = np.array([self.state[0], 0, self.state[2], 0], dtype=complex)
        else:
            new_state = np.array([0, self.state[1], 0, self.state[3]], dtype=complex)
        norm = np.linalg.norm(new_state)
        self.state = new_state / norm
        return result

    def extract_second(self):
        """
        Estrae il secondo qubit come oggetto Qubit.
        Funziona solo se il primo qubit è già stato misurato.
        """
        q = Qubit.__new__(Qubit)
        # dopo la misura del primo, lo stato è fattorizzabile
        if abs(self.state[0]) > 1e-10 or abs(self.state[1]) > 1e-10:
            q.state = np.array([self.state[0], self.state[1]], dtype=complex)
        else:
            q.state = np.array([self.state[2], self.state[3]], dtype=complex)
        norm = np.linalg.norm(q.state)
        q.state = q.state / norm
        return q

    def __repr__(self):
        labels = ['|00⟩', '|01⟩', '|10⟩', '|11⟩']
        parts = [f"{self.state[i]:.3f}{labels[i]}" for i in range(4) if abs(self.state[i]) > 1e-10]
        return f"TwoQubitSystem({' + '.join(parts)})"
    
class ThreeQubitSystem:
    """
    Rappresenta un sistema di tre qubit.
    Qubit 0: il qubit da teleportare (Alice)
    Qubit 1: membro EPR di Alice
    Qubit 2: membro EPR di Bob
    """

    # CNOT con qubit 0 come controllo e qubit 1 come target
    CNOT_01 = np.kron(
        np.array([[1,0],[0,1]], dtype=complex),  # identità su qubit 2
        np.array([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]], dtype=complex)  # CNOT su 0,1
    ).reshape(8,8)

    def __init__(self, qubit, epr_state):
        """
        qubit: il qubit da teleportare (Qubit)
        epr_state: stato EPR come array numpy di 4 componenti
        """
        self.state = np.kron(qubit.state, epr_state)

    @classmethod
    def create(cls, qubit):
        """
        Crea il sistema a tre qubit con la coppia EPR |Φ+⟩ già entangled.
        """
        epr = np.array([1, 0, 0, 1], dtype=complex) / np.sqrt(2)
        return cls(qubit, epr)

    def apply_cnot_01(self):
        """CNOT con qubit 0 come controllo e qubit 1 come target"""
        cnot = np.array([
            [1,0,0,0,0,0,0,0],
            [0,1,0,0,0,0,0,0],
            [0,0,1,0,0,0,0,0],
            [0,0,0,1,0,0,0,0],
            [0,0,0,0,0,1,0,0],
            [0,0,0,0,1,0,0,0],
            [0,0,0,0,0,0,0,1],
            [0,0,0,0,0,0,1,0],
        ], dtype=complex)
        self.state = cnot @ self.state

    def apply_h_first(self):
        """Applica H gate al primo qubit"""
        h_full = np.kron(np.kron(Qubit.H, Qubit.I), Qubit.I)
        self.state = h_full @ self.state

    def measure_first_two(self):
        """
        Misura i primi due qubit (quelli di Alice).
        Restituisce (bit1, bit2) e collassa lo stato.
        """
        # probabilità dei 4 outcome possibili
        probs = np.zeros(4)
        probs[0] = abs(self.state[0])**2 + abs(self.state[1])**2  # 00
        probs[1] = abs(self.state[2])**2 + abs(self.state[3])**2  # 01
        probs[2] = abs(self.state[4])**2 + abs(self.state[5])**2  # 10
        probs[3] = abs(self.state[6])**2 + abs(self.state[7])**2  # 11

        # scegli outcome in base alle probabilità
        outcome = np.random.choice([0, 1, 2, 3], p=probs/probs.sum())

        bit1 = outcome >> 1  # primo bit
        bit2 = outcome & 1   # secondo bit

        # collassa lo stato
        new_state = np.zeros(8, dtype=complex)
        start = outcome * 2
        new_state[start] = self.state[start]
        new_state[start+1] = self.state[start+1]
        norm = np.linalg.norm(new_state)
        self.state = new_state / norm

        return bit1, bit2

    def extract_bob(self):
        """
        Estrae il qubit di Bob dopo la misura di Alice.
        """
        q = Qubit.__new__(Qubit)
        # trova i componenti non nulli
        non_zero = np.nonzero(self.state)[0]
        if len(non_zero) >= 2:
            q.state = np.array([self.state[non_zero[0]], self.state[non_zero[1]]], dtype=complex)
        else:
            q.state = np.array([self.state[non_zero[0]], 0+0j], dtype=complex)
        norm = np.linalg.norm(q.state)
        q.state = q.state / norm
        return q

    def __repr__(self):
        labels = ['|000⟩','|001⟩','|010⟩','|011⟩','|100⟩','|101⟩','|110⟩','|111⟩']
        parts = [f"{self.state[i]:.3f}{labels[i]}" for i in range(8) if abs(self.state[i]) > 1e-10]
        return f"ThreeQubitSystem({' + '.join(parts)})"