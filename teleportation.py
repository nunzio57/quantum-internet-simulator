import numpy as np
from qubit import Qubit, TwoQubitSystem, ThreeQubitSystem

class Teleportation:

    def teleport(self, qubit, entanglement_fidelity):
        original = Qubit(qubit.alpha, qubit.beta)

        # creo sistema a 3 qubit con EPR già entangled
        system = ThreeQubitSystem.create(qubit)

        # Alice applica CNOT e H
        system.apply_cnot_01()
        system.apply_h_first()

        # Alice misura
        bit1, bit2 = system.measure_first_two()

        # estraggo il qubit di Bob
        epr_bob = system.extract_bob()

        # Bob applica correzione
        if bit2 == 1:
            epr_bob.x_gate()
        if bit1 == 1:
            epr_bob.z_gate()

        # applica decoerenza
        epr_bob = self._apply_decoherence(epr_bob, entanglement_fidelity)

        # calcola fidelity
        fidelity = original.fidelity(epr_bob)

        return epr_bob, fidelity

    def _create_epr_pair(self):
        """Crea una coppia EPR perfetta |Φ+⟩"""
        # creo due qubit separati che rappresentano la coppia EPR
        epr_alice = Qubit(1+0j, 0+0j)
        epr_bob = Qubit(1+0j, 0+0j)
        # applica H ad alice e poi "entanglement"simulato
        epr_alice.h_gate()
        return epr_alice, epr_bob

    def _apply_decoherence(self, qubit, fidelity):
        """
        Degrada il qubit in base alla fidelity dell'entanglement.
        Mescola lo stato del qubit con uno stato completamente misto.
        F=1 -> qubit perfetto, F=0 -> qubit completamente casuale
        """
        # con probabilità (1-fidelity) sostituisco con uno stato casuale
        if np.random.random() > fidelity:
            # stato casuale, simula decoerenza completa
            angle = np.random.random() * 2 * np.pi
            new_alpha = np.cos(angle / 2)
            new_beta = np.sin(angle / 2) * np.exp(1j * np.random.random() * 2 * np.pi)
            q = Qubit(new_alpha, new_beta)
            return q
        return qubit

    def __repr__(self):
        return "Teleportation()"
