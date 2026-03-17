class Node:
    def __init__(self, name, is_repeater=False):
        self.name = name
        self.is_repeater = is_repeater
        self.channels = {}

    def add_channel(self, channel):
        if channel.node_a.name == self.name:
            other = channel.node_b.name
        else:
            other = channel.node_a.name
        self.channels[other] = channel
        

    def __repr__(self):
        return f"Node name:{self.name}, is repeater={self.is_repeater}, links={list(self.channels.keys())}"
