
class Maze(object):
    def __init__(self, width, height, maze, start):
        self.width = width
        self.height = height
        self.maze = maze
        #0 is empty; 1 is node; 2 is blocked; 3 is visited
        self.start = start
        self.end = (-1, -1)
        self.queue = []
        self.visited = []
        self.path = dict()
        self.sol = []
        self.last = (-1, -1)

    def success(self, curr): 
        if (not (self.start[0] == curr[0] and self.start[1] == curr[1]) 
            and self.maze[curr[0]][curr[1]] == 1):
            # self.path[curr] = self.last
            self.end = curr
            return True
        return False

    def move(self, curr):
        self.visited.append(curr)

    def nextMoves(self, curr):
        possible = [(curr[0]-1, curr[1]), (curr[0]+1, curr[1]),
                    (curr[0], curr[1]-1), (curr[0], curr[1]+1)]
        for (row, col) in possible:
            if not (row, col) in self.visited:
                if (0 <= row < self.height and 0<= col < self.width):
                    if self.maze[row][col] == 0 or self.maze[row][col] == 1:
                        self.queue.append((row, col))
                        self.path[(row, col)] = curr

    def search(self, curr):
        if self.success(curr):
            key = self.end
            #print(self.path)
            while not (key == self.start):
                self.sol.append(key)
                key = self.path[key]
            self.sol.append(key)
            #print(self.sol)
            return self.sol
        else:
            self.nextMoves(curr)
            self.visited.append(self.queue.pop(0))
            self.last = curr
            if len(self.queue) > 0:
                return self.search(self.queue[0])
            else:
                return None

    def solve(self):
        self.queue.append(self.start)
        return self.search(self.start)

#Test
maze1 = [[0, 1, 0, 0, 2], 
         [0, 0, 0, 2, 1], 
         [2, 2, 0, 2, 0], 
         [0, 1, 0, 0, 0]]
M1 = Maze(5, 4, maze1, (0, 1))
M1Sol = M1.solve()
print(M1Sol)
maze2 = [[1, 2], [0, 1]]
M2 = Maze(2, 2, maze2, (0, 0))
M2Sol = M2.solve()
print(M2Sol)