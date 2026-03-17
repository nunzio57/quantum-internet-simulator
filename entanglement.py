class EntanglementManager:
    def __init__(self, network, router):
        self.network = network
        self.router = router

    def swap(self, path):
        """
        Dato un percorso ['e1', 'r1', 'r2', 'e4'],
        simula l'entanglement swapping in ogni repeater intermedio.
        Restituisce la fidelity finale dell'entanglement e1-e4.
        """
        if len(path) < 2:
            return 0


        fidelity = self.router.get_fidelity(path)

        repeaters = path[1:-1]  # nodi intermedi
        if repeaters:
            print(f"Entanglement swapping in: {repeaters}")
            print(f"Entanglement finale {path[0]}-{path[-1]}: F={fidelity:.3f}")
        else:
            print(f"Link diretto {path[0]}-{path[-1]}: F={fidelity:.3f}")

        return fidelity

    def __repr__(self):
        return f"EntanglementManager(network={self.network})"