from node import Node
from channel import QuantumChannel

class QuantumNetwork:
    def __init__(self):
        # dizionario dei nodi e lista dei canali
        self.nodes = {}
        self.channels = []

    def add_host(self, name):
        # crea un nodo host e lo aggiunge alla rete
        node = Node(name, is_repeater = False)
        self.nodes[name] = node

    def add_repeater(self, name):
        # crea un nodo repeater e lo aggiunge alla rete
        node = Node(name, is_repeater = True)
        self.nodes[name] = node

    def add_link(self, name_a, name_b, gamma):
        # crea un canale tra i due nodi
        # chiama add_channel su entrambi i nodi
        node_a = self.nodes[name_a]
        node_b = self.nodes[name_b]
        channel = QuantumChannel(node_a,node_b,gamma)
        node_a.add_channel(channel)
        node_b.add_channel(channel)
        self.channels.append(channel)

    def tick(self, dt):
        # fa avanzare il tempo — chiama decay su tutti i canali
        for c in self.channels:
            c.decay(dt)

    def __repr__(self):
        result = "QuantumNetwork:\n"
        for node in self.nodes.values():
            result += f"  {node}\n"
        for channel in self.channels:
            result += f"  {channel}\n"
        return result