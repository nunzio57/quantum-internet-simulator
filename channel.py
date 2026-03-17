import math

class QuantumChannel:
    def __init__(self, node_a, node_b, gamma):
        self.node_a = node_a
        self.node_b = node_b
        self.gamma = gamma
        self.fidelity = 1.0
        self.timer = 0

    def decay(self, dt):
        self.timer = self.timer + dt
        self.fidelity = math.exp(-2 * self.gamma * self.timer)

    def regenerate(self):
        self.fidelity = 1.0
        self.timer = 0

    def __repr__(self):
        return f"Channel({self.node_a.name}-{self.node_b.name}, F={self.fidelity:.3f}, t={self.timer}s)"

