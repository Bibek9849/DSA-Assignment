from collections import deque

class Four_a:
    def __init__(self):
        pass

    def shortestPath(self, grid):
        m = len(grid)
        n = len(grid[0])
        keys = set()
        doors = {}
        start_x = -1
        start_y = -1

        for i in range(m):
            for j in range(n):
                cell = grid[i][j]
                if cell == 'S':
                    start_x = i
                    start_y = j
                elif 'a' <= cell <= 'z':
                    keys.add(cell)
                elif 'A' <= cell <= 'Z':
                    doors[cell] = (i, j)

        keys_list = list(keys)
        min_distance = [float('inf')]
        self.dfs(grid, start_x, start_y, keys_list, doors, [[False] * n for _ in range(m)], "", 0, min_distance)

        return min_distance[0] if min_distance[0] != float('inf') else -1

    def dfs(self, grid, x, y, keys, doors, visited, collected_keys, distance, min_distance):
        if distance >= min_distance[0]:
            return

        visited[x][y] = True

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx = x + dx
            ny = y + dy

            if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and not visited[nx][ny]:
                cell = grid[nx][ny]

                if cell == 'P' or cell == 'S':
                    self.dfs(grid, nx, ny, keys, doors, visited, collected_keys, distance + 1, min_distance)
                elif 'a' <= cell <= 'z':
                    new_collected_keys = collected_keys + cell
                    if len(new_collected_keys) == len(keys):
                        min_distance[0] = min(min_distance[0], distance + 1)
                    else:
                        self.dfs(grid, nx, ny, keys, doors, visited, new_collected_keys, distance + 1, min_distance)
                elif 'A' <= cell <= 'Z':
                    key = cell.lower()
                    if key in collected_keys:
                        self.dfs(grid, nx, ny, keys, doors, visited, collected_keys, distance + 1, min_distance)

        visited[x][y] = False

if __name__ == "__main__":
    grid = [
        ['S', 'P', 'q', 'P', 'P'],
        ['W', 'W', 'W', 'P', 'W'],
        ['r', 'P', 'Q', 'P', 'R']
    ]
    grid= ["SPaPP","WWWPW","bPAPB"] 
    solution = Four_a()
    print(solution.shortestPath(grid))
