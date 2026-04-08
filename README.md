# Quantum Internet Simulator

A Python simulator for quantum network communication, implementing core quantum networking concepts including quantum teleportation, entanglement-based routing, and an SDN-inspired Entanglement-Defined Controller (EDC).

## Motivation

This project was inspired by the research of the Quantum Internet Research Group at the University of Naples Federico II, in particular:

- *"Quantum Internet Architecture: Unlocking Quantum-Native Routing via Quantum Addressing"* — Caleffi, Cacciapuoti, IEEE Transactions on Communications, 2026

I read this paper while exploring the field and found the open problems 
around quantum-native simulation interesting enough to try building something.

## Architecture

The simulator is structured as a modular library. Each module is independent and can be composed freely to build arbitrary quantum network topologies.

```
qubit.py          — Qubit state representation, quantum gates, multi-qubit systems
channel.py        — Quantum link with fidelity decay 
node.py           — Network node (host or repeater)
network.py        — Network topology manager
routing.py        — Fidelity-based routing (maximizes end-to-end entanglement fidelity)
entanglement.py   — Entanglement swapping across repeaters
teleportation.py  — Full quantum teleportation protocol (Bell circuit + corrections)
controller.py     — Entanglement-Defined Controller (EDC), inspired by the 2026 paper
```

## Key Concepts

### Decoherence Model
Link fidelity decays over time according to the formula:

```
F(t) = e^(-2γt)
```

Each link has an independent decay rate γ and timer. When fidelity drops below a threshold, the entanglement is regenerated (simulating quantum repeater behavior).

### Fidelity-Based Routing
Unlike classical networks that minimize hop count or latency, this simulator routes based on **entanglement fidelity**. The end-to-end fidelity of a path is the product of the fidelities of its links:

```
F(path) = F(link_1) × F(link_2) × ... × F(link_n)
```

The router finds the path that maximizes this value using DFS over the network graph.

### Quantum Teleportation
The teleportation protocol follows these steps:

1. Create EPR pair shared between source and destination
2. Alice applies CNOT and H gates
3. Alice measures and she obtains 2 classical bits
4. Bob applies corrections (X, Z gates) based on the 2 bits
5. Decoherence is applied based on entanglement fidelity

The implementation uses full quantum state vectors and matrix operations (via NumPy), not approximations.

### Entanglement-Defined Controller (EDC)
The controller is the SDN layer of the simulator. It receives a teleportation request and coordinates:
- Routing
- Entanglement swapping across repeaters
- Teleportation
- Fidelity reporting

This architecture directly mirrors the EDC concept proposed in the 2026 paper, where entanglement is managed as a dynamic network resource with separation between control plane and data plane.

## Usage

```python
from network import QuantumNetwork
from qubit import Qubit
from controller import EntanglementDefinedController

# Build network topology
net = QuantumNetwork()
net.add_host('alice')
net.add_host('bob')
net.add_repeater('r1')
net.add_repeater('r2')
net.add_link('alice', 'r1', gamma=0.01)
net.add_link('r1', 'r2', gamma=0.02)
net.add_link('r2', 'bob', gamma=0.015)

# Simulate time passing (decoherence)
net.tick(10)

# Request teleportation
controller = EntanglementDefinedController(net)
qubit = Qubit(0.6+0j, 0.8+0j)
received, fidelity = controller.request_teleportation(qubit, 'alice', 'bob')
```

## Requirements

```
Python 3.9+
numpy
```

Install with:
```
pip install numpy
```

## Limitations and Future Work

- Decoherence model is currently a probabilistic approximation. A full density matrix implementation using Lindblad operators would be more physically accurate.
- Entanglement purification is not yet implemented.
- Real-time simulation mode (time advances automatically in background) is planned.
- The simulator does not yet support the quantum addressing scheme proposed in the 2026 paper.

## Author

Nunzio Giordano  
MSc Computer Engineering, University of Naples Federico II

Built as a personal learning project while approaching quantum networking 
for the first time. FNS!
