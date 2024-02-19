
# priority queue using min heap.
class PriorityQueue:
    def __init__(self):
        self.data = []

    def is_empty(self):
        return len(self.data) == 0

    def peek(self):
        if not self.is_empty():
            return self.data[0]
        else:
            return None

    def enqueue(self, item):
        self.data.append(item)
        c_index = len(self.data) - 1
        p_index = (c_index - 1) // 2

        while c_index > 0 and self.data[c_index] < self.data[p_index]:
            self.data[c_index], self.data[p_index] = self.data[p_index], self.data[c_index]
            c_index = p_index
            p_index = (c_index - 1) // 2

    def dequeue(self):
        if len(self.data) == 0:
            return None
        elif len(self.data) == 1:
            return self.data.pop(0)
        else:
            to_return = self.data[0]
            self.data[0] = self.data.pop(-1)
            p_index = 0

            while True:
                l_index = 2 * p_index + 1
                lesser_child_index = l_index

                if l_index >= len(self.data):
                    break

                r_index = l_index + 1
                if r_index < len(self.data) and self.data[r_index] < self.data[l_index]:
                    lesser_child_index = r_index

                if self.data[lesser_child_index] < self.data[p_index]:
                    self.data[p_index], self.data[lesser_child_index] = self.data[lesser_child_index], self.data[p_index]
                    p_index = lesser_child_index
                else:
                    break

            return to_return

    def __str__(self):
        return str(self.data)


# Example usage:
if __name__ == "__main__":
    pq = PriorityQueue()
    pq.enqueue(3)
    pq.enqueue(1)
    pq.enqueue(4)
    pq.enqueue(2)
    pq.enqueue(5)
    print(pq.dequeue())  # Output: 1
    print(pq.dequeue())  # Output: 2
    print(pq.dequeue())  # Output: 3
    print(pq.dequeue())  # Output: 4
    print(pq.dequeue())  # Output: 5


#     min heap kukras algo

from typing import List

class DisjointSet:
    def __init__(self, vertices):
        self.parent = [-1] * vertices

    def find(self, v):
        if self.parent[v] == -1:
            return v
        return self.find(self.parent[v])

    def union(self, src, dest):
        src_parent = self.find(src)
        dest_parent = self.find(dest)
        self.parent[src_parent] = dest_parent

class Edge:
    def __init__(self, src, dest, weight):
        self.src = src
        self.dest = dest
        self.weight = weight

class KukrasAlgorithm:
    def kruskalMST(self, edges: List[Edge], vertices: int) -> List[Edge]:
        # Initialize disjoint-set
        ds = DisjointSet(vertices)

        # Sort edges based on weight
        edges.sort(key=lambda x: x.weight)

        # Initialize result
        result = []

        for edge in edges:
            src_parent = ds.find(edge.src)
            dest_parent = ds.find(edge.dest)

            # Add edge to result if including it doesn't form a cycle
            if src_parent != dest_parent:
                result.append(edge)
                ds.union(src_parent, dest_parent)

        return result

# Example usage
if __name__ == "__main__":
    edges = [
        Edge(0, 1, 10),
        Edge(0, 2, 6),
        Edge(0, 3, 5),
        Edge(1, 3, 15),
        Edge(2, 3, 4)
    ]

    kruskalMST = KukrasAlgorithm()
    mst = kruskalMST.kruskalMST(edges, 4)

    print("Minimum Spanning Tree:")
    for edge in mst:
        print(edge.src, "-", edge.dest, ":", edge.weight)

