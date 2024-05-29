import random
from dataclasses import dataclass, field
import matplotlib.pyplot as plt

@dataclass
class MazeCell:
    x: int
    y: int
    component: int
    is_open: bool = field(default=False)
    walls: list = field(default_factory=list)

class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x != root_y:
            if self.rank[root_x] < self.rank[root_y]:
                self.parent[root_x] = root_y
            elif self.rank[root_x] > self.rank[root_y]:
                self.parent[root_y] = root_x
            else:
                self.parent[root_y] = root_x
                self.rank[root_x] += 1

def generate_maze(N):
    maze = [[MazeCell(x, y, x * N + y, True) for y in range(N)] for x in range(N)]
    uf = UnionFind(N * N)
    while len(set(uf.parent)) > 1:
        x, y = random.randint(0, N - 1), random.randint(0, N - 1)
        dx, dy = random.choice([(0, 1), (1, 0), (0, -1), (-1, 0)])
        nx, ny = x + dx, y + dy
        if 0 <= nx < N and 0 <= ny < N:
            if uf.find(x * N + y) != uf.find(nx * N + ny):
                uf.union(x * N + y, nx * N + ny)
                maze[x][y].is_open = True
                maze[x][y].walls[random.choice([(dx, dy), (-dx, -dy)])] = False
                maze[nx][ny].is_open = True
                maze[nx][ny].walls[random.choice([(dx, dy), (-dx, -dy)])] = False
    return maze

def draw_maze(maze):
    for row in maze:
        for cell in row:
            if not cell.is_open:
                plt.fill([cell.x, cell.x + 1, cell.x + 1, cell.x], [cell.y, cell.y, cell.y + 1, cell.y + 1], 'black')
            if cell.walls[0]:
                plt.plot([cell.x, cell.x + 1], [cell.y + 1, cell.y + 1], 'black')
            if cell.walls[1]:
                plt.plot([cell.x + 1, cell.x + 1], [cell.y, cell.y + 1], 'black')
            if cell.walls[2]:
                plt.plot([cell.x, cell.x + 1], [cell.y, cell.y], 'black')
            if cell.walls[3]:
                plt.plot([cell.x, cell.x], [cell.y, cell.y + 1], 'black')
    plt.axis('equal')
    plt.axis('off')

N = 30
maze = generate_maze(N)

plt.figure(figsize=(10, 10))
draw_maze(maze)
plt.show()
