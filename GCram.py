import networkx as nx
import uuid


def mex(s):  # helper mex function
    i = 0
    while i in s:
        i += 1
    return i


def xor(s):
    result = 0
    for i in s:
        result ^= i
    return result


def g1ncram(x):
    first = [0, 0, 1, 1, 2, 0, 3, 1, 1, 0, 3, 3, 2, 2, 4, 0, 5, 2, 2, 3, 3, 0,
             1, 1, 3, 0, 2, 1, 1, 0, 4, 5, 2, 7, 4, 0, 1, 1, 2, 0, 3, 1, 1, 0, 3, 3, 2, 2, 4, 4, 5, 5, 2]
    periodic = [3, 3, 0, 1, 1, 3, 0, 2, 1, 1, 0, 4, 5, 3, 7, 4, 8, 1, 1, 2, 0, 3, 1, 1, 0, 3, 3, 2, 2, 4, 4, 5, 5, 9]
    if x < len(first):
        return first[x]
    else:
        return periodic[(x - len(first)) % len(periodic)]


class GCram:
    def __init__(self, edges=None, graph=None):
        if graph is not None:
            self.graph = graph
        elif edges is not None:
            self.graph = nx.Graph()
            self.graph.add_edges_from(edges)
        else:
            self.graph = nx.Graph()

    def __eq__(self, other):
        return nx.is_isomorphic(self.graph, other.graph)

    def __hash__(self):
        return int(nx.weisfeiler_lehman_graph_hash(self.graph), 16)

    def uid(self):
        return int(nx.weisfeiler_lehman_graph_hash(self.graph) + uuid.uuid4().hex, 16)

    def options(self):
        edges = self.graph.edges()
        options = set([self.cram_remove_edge(edge) for edge in edges])
        return options

    def create_new(self, edges=None, graph=None):
        return GCram(edges, graph)

    def cram_remove_edge(self, edge):
        new_graph = self.graph.copy()
        new_graph.remove_node(edge[0])
        new_graph.remove_node(edge[1])
        new_graph.remove_nodes_from(list(nx.isolates(new_graph)))  # remove isolates
        return self.create_new(graph=new_graph)

    def known_nim(self):
        return None

    def nim_values(self, s: dict = None):
        if s is None:
            s = {}

        def __nim_values__(graph, cache):
            if graph.graph.number_of_edges() == 0:
                return 0
            if graph.known_nim() is not None:
                return graph.known_nim()
            if graph in cache:
                return cache[graph]
            elif not nx.is_connected(graph.graph):
                subset = []
                for component in nx.connected_components(graph.graph):
                    subset.append(__nim_values__(self.create_new(graph=graph.graph.subgraph(component)), cache))
                return xor(subset)
            else:
                subset = set()
                for option in graph.options():
                    val = __nim_values__(option, cache)
                    subset.add(val)
                cache[graph] = mex(subset)
            return cache[graph]

        return __nim_values__(self, s), s

    def cram_minors(self, s: set = None):
        if s is None:
            s = set()

        def __cram_minors__(graph, cache):
            if graph.graph in cache or graph.graph.number_of_edges() == 0:
                return set()
            elif not nx.is_connected(graph.graph):
                for component in nx.connected_components(graph.graph):
                    __cram_minors__(self.create_new(graph=graph.graph.subgraph(component)), cache)
            else:
                for option in graph.options():
                    __cram_minors__(option, cache)
                    if option.graph.number_of_edges() != 0 and nx.is_connected(option.graph):
                        cache.add(option)

        __cram_minors__(self, s)
        return s

    def __str__(self):
        return f'{self.graph.nodes()},{self.graph.edges()}'

    def __repr__(self):
        return f'{self.graph.nodes()},{self.graph.edges()}'


class LatticeBasedGCram(GCram):
    @staticmethod
    def lattice(m, n):
        edges = []
        for i in range(m):
            for j in range(n):
                if i < m - 1:
                    edges.append(((i, j), (i + 1, j)))
                if j < n - 1:
                    edges.append(((i, j), (i, j + 1)))
        return LatticeBasedGCram(m, n, edges=edges)

    def __init__(self, m, n, edges=None, graph=None):
        super().__init__(edges, graph)
        self.m = m
        self.n = n

    def create_new(self, edges=None, graph=None):
        return LatticeBasedGCram(self.m, self.n, edges, graph)

    def uid(self):
        node_set = set(self.graph.nodes())
        result = 0
        for i in node_set:
            result |= 1 << (i[0] * self.n + i[1])
        return result

    def known_nim(self):
        if self.is_even_lattice():
            return 0
        elif self.is_path():
            return g1ncram(self.is_path())
        else:
            return None

    def is_even_lattice(self):
        max_x = max([i[0] for i in self.graph.nodes()])
        max_y = max([i[1] for i in self.graph.nodes()])
        min_x = min([i[0] for i in self.graph.nodes()])
        min_y = min([i[1] for i in self.graph.nodes()])
        return ((max_x - min_x + 1) % 2 == 0 and (max_y - min_y + 1) % 2 == 0
                and self.graph.number_of_nodes() == (max_x - min_x + 1) * (max_y - min_y + 1))

    def is_path(self):
        if not nx.is_connected(self.graph):
            return False
        if self.graph.number_of_nodes() != self.graph.number_of_edges() + 1:
            return False
        for node in self.graph.nodes():
            if self.graph.degree(node) > 2:
                return False
        return self.graph.number_of_nodes()

    def __str__(self):
        return f'{self.uid():0{m * n}b}'

    def __repr__(self):
        return f'{self.uid():0{m * n}b}'


class CompleteGraph(GCram):
    @staticmethod
    def complete_graph(n):
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                edges.append((i, j))
        return CompleteGraph(n, edges=edges)

    def __init__(self, n, edges=None, graph=None):
        super().__init__(edges, graph)
        self.n = n

    def uid(self):
        node_set = set(self.graph.nodes())
        result = 0
        for i in node_set:
            result |= 1 << i
        return result


if __name__ == "__main__":
    # m = 3
    # n = 7
    # G = LatticeBasedGCram.lattice(m, n)
    # nim_value, s = G.nim_values()
    # print(nim_value)
    # print(len(s))

    G = CompleteGraph.complete_graph(10)
    nim_value, s = G.nim_values()
    print(nim_value)
    # minors = G.cram_minors()
    # print(len(minors))
    # for minor in minors:
    #     print(f'{minor.uid():0{m * n}b}')
    # initial_set = set([GCram.lattice(i, j) for i in range(2, m - 1) for j in range(2, n - 1)]).union(set([GCram.lattice(1, n) for n in range(2, n - 2)]))
    # minors = G.cram_minors(s=set([GCram.lattice(i, j) for i in range(2, m - 1) for j in range(2, n - 1)]))
    # print([(g.graph.number_of_nodes(), g.graph.number_of_edges()) for g in minors])
    # print([g.graph.edges() for g in G.cram_minors()])
    # print([g.graph.nodes() for g in G.cram_minors()])
    # print(len(minors))
