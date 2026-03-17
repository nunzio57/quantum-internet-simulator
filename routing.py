from network import QuantumNetwork

class Router:
    def __init__(self, network):
        self.network = network

    def get_fidelity(self, path):
        # dato un percorso (lista di nomi di nodi)
        # calcola la fidelity totale come prodotto delle fidelity dei link
        fidelity = 1
        for i in range(0,len(path) - 1):
            j = i + 1
            if j >= len(path):
                break
            fidelity = fidelity * self.network.nodes[path[i]].channels[path[j]].fidelity

        return fidelity
        

    def find_best_path(self, source, destination):
    # DFS per trovare tutti i percorsi possibili
        all_paths = []

        def dfs(current, destination, path, visited):
            if current == destination:
                all_paths.append(list(path))
                return
            visited.add(current)
            for neighbor in self.network.nodes[current].channels.keys():
                if neighbor not in visited:
                    path.append(neighbor)
                    dfs(neighbor, destination, path, visited)
                    path.pop()
            visited.remove(current)

        dfs(source, destination, [source], set())

        if not all_paths:
            return None, 0

        best_path = max(all_paths, key=lambda p: self.get_fidelity(p))
        best_fidelity = self.get_fidelity(best_path)

        return best_path, best_fidelity