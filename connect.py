import itertools
from maze_bfs import Maze

class Appliance(object):
    def __init__(self, pinDict, blockedPos):
        #pinDict is a dictionary with pins as keys and position of the pins as 
        # values. The values are tuples of integers, and the positions are 
        # corresponding to the top left corner of the appliance
        self.pinDict = pinDict
        #blockedPos is a set of positions where wires should not pass through 
        # within the appliance
        self.blockedPos = blockedPos
        self.pinNet = dict()
        for pin in self.pinDict:
            self.pinNet[pin] = ""

    def emptyPin(self):
        self.pinDict = dict()

    def addPin(self, pin, pos):
        self.pinDict[pin] = pos
        self.pinNet[pin] = ""

    def editNet(self, pin, net):
        self.pinNet[pin] = net

    def getPinNet(self, pin):
        return self.pinNet[pin]
    
    def getPinPos(self, pin):
        return self.pinDict[pin]

    def getAllPos(self):
        pos = set()
        for (pin, position) in self.pinDict.items:
            pos.add(position)
        return pos


class Pcb(object):
    def __init__(self, width, height, board, appliances):
        self.width = width
        self.height = height
        self.board = board
        #appliances is the list of all appliances to be put onto the board
        self.appliances = appliances
        self.appPos = dict()
        for appliance in self.appliances:
            self.appPos[appliance] = (0, 0)
        self.wiredTotal = []

    def emptyBoard(self):
        self.board = [["green"] * self.width for i in range(self.height)]

    def addApp(self, app):
        self.appliances.append(app)
        self.appPos[app] = (0, 0)

    def place(self, app, row, col):
        self.appPos[app] = (row, col)

    def update(self):
        self.emptyBoard()
        for app in self.appliances:
            (drow, dcol) = self.appPos[app]
            for pin in app.pinDict:
                net = app.getPinNet(pin)
                (row, col) = app.getPinPos(pin)
                self.board[drow + row][dcol + col] = net
            for (blockRow, blockCol) in app.blockedPos:
                self.board[drow + blockRow][dcol + blockCol] = "block"

    #collect all the nets that need to be connected
    def getAllNet(self):
        allNet = []
        for app in self.appliances:
            for pin in app.pinDict:
                net = app.getPinNet(pin)
                if not net in allNet:
                    allNet.append(net)
        return allNet

    #convert the pcb with appliances placed into a maze for a specific net
    def wirePcb(self, wired, net):
        for (row, col) in wired:
            self.board[row][col] = net

    def toMaze(self, net):
        maze = []
        nodes = []
        for row in range(self.height):
            mazeRow = []
            for col in range(self.width):
                cell = self.board[row][col]
                if cell == "green":
                    mazeRow.append(0)
                elif cell == net:
                    mazeRow.append(1)
                    nodes.append((row, col))
                else:
                    mazeRow.append(2)
            maze.append(mazeRow)
        return maze, nodes

    def updateMaze(self, maze, wireList):
        for wire in wireList:
            maze[wire[0]][wire[1]] = 1
        
    def wireNet(self, net):
        maze, nodes = self.toMaze(net)
        seen = set()
        for node in nodes:
            wire = Maze(self.width, self.height, maze, node)
            if not node in seen:
                wired = wire.solve()
                if not wired == None:
                    self.wiredTotal.append(wired)
                    seen.add(wire.end)
                    self.updateMaze(maze, wired)
                    seen.add(node)
                    self.wirePcb(wired, net)

    def printPcb(self):
        for row in self.board:
            print(row)

#Test case -- GND * 2
def test2():
    print("Testing 2 GND pads ...")
    ####INITIALIZE####
    # Appliance
    # Pad
    pinDictP1 = {"1": (0, 0)}
    blockedP1 = set()
    P1 = Appliance(pinDictP1, blockedP1)
    P1.editNet("1", "GND")
    P2 = Appliance(pinDictP1, blockedP1)
    P2.editNet("1", "GND")
    # board
    pcb2 = Pcb(5, 3, [[]], [P1, P2])
    pcb2.emptyBoard()
    pcb2.printPcb()
    pcb2.place(P1, 1, 1)
    pcb2.place(P2, 1, 3)
    pcb2.update()
    pcb2.printPcb()
    ####CONNECT####
    allNet2 = pcb2.getAllNet()
    print(allNet2)
    for net in allNet2:
        pcb2.wireNet(net)
    print(pcb2.wiredTotal)
    pcb2.printPcb()
    print("Test passed")

#Test case -- AC to DC
def test1():
    #Test case -- AC to DC:
    #Appliance
    #Capacitor
    pinDictC1 = {"1": (1, 0), "2": (1, 2)}
    blockedC1 = set([(0, 1), (1, 1), (2, 1)])
    C1 = Appliance(pinDictC1, blockedC1)
    C1.editNet("1", "Vout")
    C1.editNet("2", "GND")
    #Diode
    pinDictD1 = {"1": (0, 0), "2": (3, 0)}
    blockedD1 = set([(1, 0), (2, 0)])
    D1 = Appliance(pinDictD1, blockedD1)
    D1.editNet("1", "Vcc+")
    D1.editNet("2", "Vout")
    D2 = Appliance(pinDictD1, blockedD1)
    D2.editNet("1", "Vcc-")
    D2.editNet("2", "Vout")
    D3 = Appliance(pinDictD1, blockedD1)
    D3.editNet("1", "GND")
    D3.editNet("2", "Vcc-")
    D4 = Appliance(pinDictD1, blockedD1)
    D4.editNet("1", "GND")
    D4.editNet("2", "Vcc+")
    #Pad
    pinDictP1 = {"1": (0, 0)}
    blockedP1 = set()
    P1 = Appliance(pinDictP1, blockedP1)

    #Board
    pcb1 = Pcb(18, 6, [[]], [C1, D1, D2, D3, D4])
    #pcb1 = Pcb(18, 10, [[]], [D1, D2, D3, D4])
    pcb1.emptyBoard()
    pcb1.place(D1, 1, 1)
    pcb1.place(D2, 1, 4)
    pcb1.place(D3, 1, 7)
    pcb1.place(D4, 1, 10)
    pcb1.place(C1, 1, 14)
    pcb1.update()
    pcb1.printPcb()
    ####CONNECT####
    allNet1 = pcb1.getAllNet()
    print(allNet1)
    for net in allNet1:
        pcb1.wireNet(net)
    print(pcb1.wiredTotal)
    pcb1.printPcb()
    print(pcb1.wiredTotal)
    print("Test passed")

#Test case -- GND * 3
def test3():
    print("Testing 3 GND pads ...")
    ####INITIALIZE####
    # Appliance
    # Pad
    pinDictP1 = {"1": (0, 0)}
    blockedP1 = set()
    P1 = Appliance(pinDictP1, blockedP1)
    P1.editNet("1", "GND")
    P2 = Appliance(pinDictP1, blockedP1)
    P2.editNet("1", "GND")
    P3 = Appliance(pinDictP1, blockedP1)
    P3.editNet("1", "GND")
    # board
    pcb3 = Pcb(5, 3, [[]], [P1, P2, P3])
    pcb3.emptyBoard()
    pcb3.printPcb()
    pcb3.place(P1, 1, 1)
    pcb3.place(P2, 1, 3)
    pcb3.place(P3, 2, 4)
    pcb3.update()
    pcb3.printPcb()
    ####CONNECT####
    allNet2 = pcb3.getAllNet()
    print(allNet2)
    for net in allNet2:
        pcb3.wireNet(net)
    print(pcb3.wiredTotal)
    pcb3.printPcb()
    print("Test passed")

#Test case -- LED * 2 + GND * 1
def test4():
    print("Testing 1 GND pad and two LEDs ...")
    ####INITIALIZE####
    # Appliance
    # Pad
    pinDictP1 = {"1": (0, 0)}
    blockedP1 = set()
    P1 = Appliance(pinDictP1, blockedP1)
    P1.editNet("1", "GND")
    # LED1
    pinDictP2 = {"1": (0, 0), "2": (1, 0)}
    blockedP2 = set()
    P2 = Appliance(pinDictP2, blockedP2)
    P2.editNet("1", "GND")
    P2.editNet("2", "VCC")
    # LED2
    pinDictP3 = {"1": (0, 0), "2": (1, 0)}
    blockedP3 = set()
    P3 = Appliance(pinDictP3, blockedP3)
    P3.editNet("2", "GND")
    P3.editNet("1", "VCC")
    # board
    pcb3 = Pcb(5, 3, [[]], [P1, P2, P3])
    pcb3.emptyBoard()
    pcb3.printPcb()
    pcb3.place(P1, 2, 4)
    pcb3.place(P2, 1, 3)
    pcb3.place(P3, 0, 1)
    pcb3.update()
    pcb3.printPcb()
    ####CONNECT####
    allNet2 = pcb3.getAllNet()
    print(allNet2)
    for net in allNet2:
        pcb3.wireNet(net)
    print(pcb3.wiredTotal)
    pcb3.printPcb()
    print("Test passed")

# test1()
# test2()
# test3()
# test4()