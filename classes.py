from random import choice
import pygame
from queue import Queue
from pygame import Rect
import ctypes
class Maze:
	def __init__(self, rows, cols, cheeses=0, isMac=False):
		self.maze = [[BabyCell(row,col,self) for col in range(cols)] for row in range(rows)]
		for row in self.maze:
			for cell in row:
				cell.addNeighbors()
		#Create Maze with Recursive Backtracking
		stack = [self.maze[0][0]]
		#self.maze[0][1].neighbors.remove(self.maze[0][0])
		#self.maze[1][0].neighbors.remove(self.maze[0][0])
		self.maze[0][0].visited = True
		while len(stack) > 0:
			cell = stack.pop()
			if cell.hasNeighbors():
				stack.append(cell)
				stack.append(cell.popNeighbor())
		#self.maze[0][0].wall, self.maze[0][0].floor = False, False
		#Create traversable graph from maze
		self.graph = [[Cell(row,col) for col in range(cols)] for row in range(rows)]
		for r in range(rows):
			for c in range(cols):
				cell = self.graph[r][c]
				babyCell = self.maze[r][c]
				if not babyCell.wall:
					cell.addNeighbor(self.graph[r][c+1])
				if not babyCell.floor:
					cell.addNeighbor(self.graph[r+1][c])
		
		for row in self.maze:
			for cell in row:
				cell.visited = False
		self.startScreen(isMac)
		self.mouse = Mouse(self.graph[0][0], self.boxSize)
		
	def startScreen(self, isMac=False):
		pygame.init()
		displayInfo = pygame.display.Info()
		dims = (displayInfo.current_w, displayInfo.current_h)
		if not isMac:
			ctypes.windll.user32.SetProcessDPIAware()
			dims = (ctypes.windll.user32.GetSystemMetrics(0),ctypes.windll.user32.GetSystemMetrics(1))
		self.screen = pygame.display.set_mode(dims,pygame.FULLSCREEN)
		width = dims[0] // len(self.maze[0])
		height = dims[1] // len(self.maze) - 1
		self.boxSize = min(width, height)
		self.sizeCalc = self.boxSize+1
		self.left = (dims[0] - self.sizeCalc * len(self.maze[0])) // 2
		self.top = 0
		self.clock = pygame.time.Clock()
		
	def show(self, frameRate=5):
		while not self.mouse.queue.empty():
			if frameRate != 0:
				self.clock.tick(frameRate)
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
					sys.exit(pygame.quit())
			self.draw()
			self.mouseCell().visited = True
			self.mouse.node = self.mouse.queue.get()
			
	def draw(self):
		self.screen.fill((0,0,0))
		white = (255,255,255)
		purple = (255,20,150)
		#Draw maze
		outline = pygame.Rect(self.left, self.top, len(self.maze[0]) * self.sizeCalc, len(self.maze) * self.sizeCalc)
		pygame.draw.rect(self.screen, white, outline, 1)
		for row in self.maze:
			for cell in row:
				x = (cell.col+1) * self.sizeCalc + self.left
				y = (cell.row+1) * self.sizeCalc + self.top
				if cell.floor:
					pygame.draw.line(self.screen, white, (x-self.boxSize,y), (x,y))
				if cell.wall:
					pygame.draw.line(self.screen, white, (x,y-self.boxSize), (x,y))
				if cell.visited:
					#rect = Rect(x-self.boxSize, y-self.boxSize, self.boxSize, self.boxSize)
					#pygame.draw.rect(self.screen, purple, rect)
					pos = (x-self.boxSize//2, y-self.boxSize//2)
					pygame.draw.circle(self.screen, purple, pos, self.boxSize//4)
		#draw mouse
		x = self.mouse.node.col * self.sizeCalc + self.left
		y = self.mouse.node.row * self.sizeCalc + self.top
		
		rect = Rect(x, y, self.boxSize, self.boxSize)
		self.screen.blit(self.mouse.img, rect)
		pygame.display.flip()
		
	def mouseCell(self):
		node = self.mouse.node
		return self.maze[node.row][node.col]

class Mouse:
	def __init__(self, node, size):
		self.node = node
		self.img = pygame.image.load('mouse.png').convert_alpha()
		self.img = pygame.transform.scale(self.img, (size, size))
		self.size = size
		self.sizeCalc = size + 1
		self.queue = Queue()
		
	def moveTo(self, cell):
		self.queue.put(cell)

class Cell:
	def __init__(self, row, col):
		self.row = row
		self.col = col
		self.neighbors = []
		self.hasCheese = True
		
	def addNeighbor(self, neighbor):
		self.neighbors.append(neighbor)
		neighbor.neighbors.append(self)
		
class BabyCell:
	def __init__(self, row, col, grid):
		self.row = row
		self.col = col
		self.maze = grid
		self.floor = True
		self.wall = True
		self.neighbors =set()
		self.visited = False
	
	def addNeighbors(self):
		self.neighbors.add(self.top())
		self.neighbors.add(self.bottom())
		self.neighbors.add(self.left())
		self.neighbors.add(self.right())
		self.neighbors.discard(None)
	
	def hasNeighbors(self):
		for nb in self.neighbors:
			if not nb.visited:
				return True
		return False
	
	def popNeighbor(self):
		nbs = [nb for nb in self.neighbors if not nb.visited]
		neighbor = choice(nbs)
		neighbor.visited = True
		self.breakWall(neighbor)
		return neighbor
		
	
	def breakWall(self, neighbor):
		if neighbor.row > self.row:
			self.floor = False
		elif neighbor.row < self.row:
			neighbor.floor = False
		elif neighbor.col > self.col:
			self.wall = False
		else:
			neighbor.wall = False
	
	def top(self):
		return self.maze.maze[self.row-1][self.col] if self.row > 0 else None
	
	def bottom(self):
		return self.maze.maze[self.row+1][self.col] if self.row < len(self.maze.maze)-1 else None
	
	def left(self):
		return self.maze.maze[self.row][self.col-1] if self.col > 0 else None
	
	def right(self):
		return self.maze.maze[self.row][self.col+1] if self.col < len(self.maze.maze[self.row])-1 else None