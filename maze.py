
class Maze(object):
    def __init__(self, width, height, maze, start):
        self.width = width
        self.height = height
        self.maze = maze
        #0 is empty; 1 is node; 2 is blocked; 3 is visited
        self.start = start
        self.end = (-1, -1)
        self.visited = [start]
        self.sol = [start]

    def success(self, curr): 
        possible = [(curr[0]-1, curr[1]), (curr[0]+1, curr[1]),
                    (curr[0], curr[1]-1), (curr[0], curr[1]+1)]
        for (row, col) in possible:
            if not (row, col) in self.visited:
                if (0 <= row < self.height and 0<= col < self.width):
                    if self.maze[row][col] == 1:
                        self.end = (row, col)
                        return True
        return False

    def move(self, curr):
        self.visited.append(curr)

    def nextMoves(self, curr):
        possible = [(curr[0]-1, curr[1]), (curr[0]+1, curr[1]),
                    (curr[0], curr[1]-1), (curr[0], curr[1]+1)]
        next = []
        for (row, col) in possible:
            if not (row, col) in self.visited:
                if (0 <= row < self.height and 0<= col < self.width):
                    if self.maze[row][col] == 0:
                        next.append((row, col))
        #print(next)
        return next

    def search(self, curr):
        if self.success(curr):
            #print("Hi")
            self.sol.append(self.end)
            return self.sol
        else:
            for nextMove in self.nextMoves(curr):
                #print(nextMove)
                self.sol.append(nextMove)
                self.move(nextMove)
                solution = self.search(nextMove) 
                if solution == None:
                    #print("no sol")
                    self.sol.pop()
                    self.visited.pop()
                else:
                    return self.sol
            return None

    def solve(self):
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