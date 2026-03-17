from network import QuantumNetwork
from qubit import Qubit
from controller import EntanglementDefinedController

net = QuantumNetwork()
net.add_host('e1')
net.add_host('e4')
net.add_repeater('r1')
net.add_repeater('r2')
net.add_link('e1', 'r1', gamma=0.01)
net.add_link('r1', 'r2', gamma=0.02)
net.add_link('r2', 'e4', gamma=0.015)

net.tick(10)

controller = EntanglementDefinedController(net)
qubit = Qubit(0.6+0j, 0.8+0j)
qubit_ricevuto, fidelity = controller.request_teleportation(qubit, 'e1', 'e4')