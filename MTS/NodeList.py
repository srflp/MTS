from .Node import Node


class NodeList:
    def __init__(self):
        self.node_list = []
        self.queue_list = []  # po dojściu do liścia otwartego/zamkniętego, kontynuuj rozwijanie tych węzłów (beta)
        self.cur_node_id = 0
        self.depth = 0

    def __iter__(self):
        return iter(self.node_list)

    def register(self, node: Node):
        node.id = self.cur_node_id
        if self.cur_node_id == 0:
            node.parent_id = None
        elif not node.parent_id:
            node.parent_id = self.cur_node_id - 1
        node.depth = self.depth
        self.node_list.append(node)
        self.cur_node_id += 1
        self.depth += 1

    def register_in_queue(self, node: Node):
        if not node.parent_id:
            node.parent_id = self.cur_node_id - 2
        self.queue_list.append(node)

    def take_node_from_queue(self):
        node = self.queue_list.pop(0)
        node.id = self.cur_node_id
        node.depth = node.parent_id+1
        self.depth = node.parent_id+2
        self.node_list.append(node)
        self.cur_node_id += 1

    def get_last(self):
        return self.node_list[self.cur_node_id-1]