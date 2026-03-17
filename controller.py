from routing import Router
from entanglement import EntanglementManager
from teleportation import Teleportation

class EntanglementDefinedController:
    def __init__(self, network):
        self.network = network
        self.router = Router(network)
        self.entanglement = EntanglementManager(network, self.router)
        self.teleportation = Teleportation()

    def request_teleportation(self, qubit, source, destination):
        print(f"\n--- Richiesta teleportazione: {source} -> {destination} ---")

        path, _ = self.router.find_best_path(source, destination)
        if path is None:
            print("Nessun percorso disponibile")
            return None, 0

        print(f"Percorso scelto: {path}")

        fidelity = self.entanglement.swap(path)

        qubit_ricevuto, fidelity_finale = self.teleportation.teleport(qubit, fidelity)

        print(f"Fidelity entanglement: {fidelity:.3f}")
        print(f"Fidelity finale qubit: {fidelity_finale:.3f}")

        return qubit_ricevuto, fidelity_finale

    def __repr__(self):
        return f"EntanglementDefinedController(network={self.network})"