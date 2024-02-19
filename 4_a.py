from collections import deque

def shortestPath(grid):
    if not grid:
        return -1

    m, n = len(grid), len(grid[0])
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    keys = set()
    doors = set()
    start = None
    total_keys = 0

    for i in range(m):
        for j in range(n):
            if grid[i][j] == 'S':
                start = (i, j)
            elif grid[i][j] == 'E':
                exit_point = (i, j)
            elif 'a' <= grid[i][j] <= 'f':
                keys.add(grid[i][j])
                total_keys += 1
            elif 'A' <= grid[i][j] <= 'F':
                doors.add(grid[i][j])

    queue = deque([(start[0], start[1], set(), 0)])
    visited = set()

    while queue:
        x, y, collected_keys, steps = queue.popleft()

        if (x, y) == exit_point:
            if len(collected_keys) == total_keys:
                return steps
            else:
                continue

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if 0 <= nx < m and 0 <= ny < n and grid[nx][ny] != 'W' and (nx, ny, collected_keys) not in visited:
                cell = grid[nx][ny]
                new_keys = set(collected_keys)

                if 'a' <= cell <= 'f':
                    new_keys.add(cell)
                elif 'A' <= cell <= 'F' and cell.lower() in collected_keys:
                    new_keys.remove(cell.lower())

                visited.add((nx, ny, new_keys))
                queue.append((nx, ny, new_keys, steps + 1))

    return -1

# Example usage:
grid = [
    ["S", "P", "P", "P"],
    ["W", "P", "P", "E"],
    ["P", "b", "W", "P"],
    ["P", "P", "P", "P"]
]
print(shortestPath(grid))  # Output: 8