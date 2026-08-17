from queue import PriorityQueue

def best_first_search(graph, start, target, heuristics):
    visited = set()
    pq = PriorityQueue()

    # (heuristic_value, current_node, path)
    pq.put((heuristics[start], start, [start]))
    visited.add(start)

    while not pq.empty():
        h, node, path = pq.get()

        if node == target:
            return path, h

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                pq.put((heuristics[neighbor], neighbor, path + [neighbor]))

    return None, None


# Example Usage
if __name__ == "__main__":
    graph = {
        'A': ['B', 'C'],
        'B': ['D', 'E'],
        'C': ['F'],
        'D': [],
        'E': [],
        'F': []
    }

    heuristics = {
        'A': 10,
        'B': 5,
        'C': 3,
        'D': 2,
        'E': 1,
        'F': 0
    }

    path, cost = best_first_search(graph, 'A', 'F', heuristics)

    print(f"Path found by Best-First Search: {path}")
    print(f"Target Heuristic Value: {cost}")