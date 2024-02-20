class Graph:
    def __init__(self):
        self.adj_list = {}

    def add_edge(self, u, v):
        if u not in self.adj_list:
            self.adj_list[u] = []
        if v not in self.adj_list:
            self.adj_list[v] = []
        self.adj_list[u].append(v)
        self.adj_list[v].append(u)


class AffectNodeDetect:
    def __init__(self, affected_node):
        self.counter = 0
        self.preorder = None
        self.low = None
        self.affected_node = affected_node

    def get_graph(self, connections):
        # Build the graph
        graph = [[] for _ in range(n)]
        for conn in connections:
            from_node, to_node = conn
            graph[from_node].append(to_node)
            graph[to_node].append(from_node)
        return graph

    def track_visited_node(self, graph, start, visited=None):
        if visited is None:
            visited = set()
        visited.add(start)
        print(start)  # This line prints the current node being visited
        if start == self.affected_node:
            return []

        for neighbor in graph[start]:
            if neighbor not in visited and neighbor != self.affected_node:
                self.track_visited_node(graph, neighbor, visited)
        return visited

    def critical_connections(self, n, connections, graph_structure):
        result = []
        graph = self.get_graph(connections)

        self.preorder = [-1] * n
        self.low = [-1] * n

        for i in range(n):
            if self.preorder[i] == -1:
                self.dfs(graph, i, i, result)
        print(result)
        result = [conn for conn in result if self.affected_node in conn]
        print(result)
        # value = result[0] if result else []
        # start_point_value = list(filter(lambda x: x != self.affected_node, value))
        # print(start_point_value)
        result = self.track_visited_node(graph_structure, result[0][1]) if result else []
        return result

    def dfs(self, graph, src, parent, result):
        self.preorder[src] = self.counter
        self.low[src] = self.counter
        self.counter += 1

        for neighbor in graph[src]:
            if self.preorder[neighbor] == -1:
                self.dfs(graph, neighbor, src, result)
                self.low[src] = min(self.low[src], self.low[neighbor])

                if self.low[neighbor] == self.preorder[neighbor]:
                    result.append([src, neighbor])
            elif neighbor != parent:
                self.low[src] = min(self.low[src], self.preorder[neighbor])


# this class
solution = AffectNodeDetect(affected_node=4)

# Define the number of nodes and the list of connections
connections = [[0, 1], [0, 2], [1, 3], [1, 6], [2, 4], [4, 6], [4, 5], [5, 7]]
n = len(connections)

# implement graph
graph = Graph()
for u, v in connections:
    graph.add_edge(u, v)

# Call the critical_connections method on the AffectNodeDetect instance
critical_conn = solution.critical_connections(n, connections, graph.adj_list)
print(critical_conn)
