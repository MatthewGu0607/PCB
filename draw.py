import pygame
from connect import Appliance
from connect import Pcb

#Initialize Pygame
pygame.init()

#Global variables
displayw = 13 * 25
displayh = 6 * 25
cell = 25
window = pygame.display.set_mode((displayw, displayh))
pygame.display.set_caption("PCB")

#Main Class
class MainRun(object):
    def __init__(self, displayw, displayh, cell):
        self.dw = displayw
        self.dh = displayh
        self.cell = cell
        self.Main()

    def drawPCB(self, pcb):
        for i in range(len(pcb.board)):
            for j in range(len(pcb.board[0])):
                if pcb.board[i][j] == "green":
                    pygame.draw.rect(window, (152, 251, 152), 
                        (j * self.cell, i * self.cell, self.cell, self.cell))
                elif pcb.board[i][j] == "GND":
                    pygame.draw.rect(window, (0, 0, 0), 
                        (j * self.cell, i * self.cell, self.cell, self.cell))
                elif pcb.board[i][j] == "Vcc+" or pcb.board[i][j] == "Vcc":
                    pygame.draw.rect(window, (255, 102, 102), 
                        (j * self.cell, i * self.cell, self.cell, self.cell))
                elif pcb.board[i][j] == "Vcc-":
                    pygame.draw.rect(window, (255, 153, 51), 
                        (j * self.cell, i * self.cell, self.cell, self.cell))
                elif pcb.board[i][j] == "block":
                    pygame.draw.rect(window, (102, 0, 0), 
                        (j * self.cell, i * self.cell, self.cell, self.cell))
                else:
                    pygame.draw.rect(window, (102, 178, 255), 
                        (j * self.cell, i * self.cell, self.cell, self.cell))
            
    def drawWire(self, pcb):
        for wiregroup in pcb.wiredTotal:
            for i in range(len(wiregroup) - 1):
                (startR, startC) = wiregroup[i]
                (endR, endC) = wiregroup[i+1]
                pygame.draw.line(window, (0, 0, 0), 
                    (startC * self.cell + self.cell / 2, startR * self.cell + self.cell / 2),
                    (endC * self.cell + self.cell / 2, endR * self.cell + self.cell / 2), 
                    width = 10)
                   
    def testPcbInit(self):
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
        D3.editNet("1", "Vcc-")
        D3.editNet("2", "GND")
        D4 = Appliance(pinDictD1, blockedD1)
        D4.editNet("1", "Vcc+")
        D4.editNet("2", "GND")
        #Pad
        pinDictP1 = {"1": (0, 0)}
        blockedP1 = set()
        P1 = Appliance(pinDictP1, blockedP1)

        #Board
        pcb1 = Pcb(self.dw, self.dh, [[]], [C1, D1, D2, D3, D4])
        #pcb1 = Pcb(18, 10, [[]], [D1, D2, D3, D4])
        pcb1.emptyBoard()
        pcb1.place(D1, 1, 1)
        pcb1.place(D2, 1, 3)
        pcb1.place(C1, 2, 5)
        pcb1.place(D3, 1, 9)
        pcb1.place(D4, 1, 11)
        return pcb1

    def is_clicked(self):
        return pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pygame.mouse.get_pos())

    def Main(self):
        pcb = self.testPcbInit()
        pressed = False
        stopped = False
        
        while not stopped:
            pcb.update()
            self.drawPCB(pcb)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_RETURN]:
                        pressed = True
                    elif keys[pygame.K_r]:
                        pressed = False
            if pressed:
                allNet = pcb.getAllNet()
                for net in allNet:
                    pcb.wireNet(net)
                self.drawWire(pcb)
            pygame.display.update()

if __name__ == "__main__":
    MainRun(displayw, displayh, cell)