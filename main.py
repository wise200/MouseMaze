from random import choice

class Maze:
	def __init__(self, rows, cols, frameRate=10):
		self.grid = [[BabyCell(row,col,self) for col in range(cols)] for row in range(rows)]
		for row in self.grid:
			for cell in row:
				cell.addNeighbors()
		#Create Maze with Recursive Backtracking
		stack = [self.grid[0][0]]
		self.grid[0][1].neighbors.remove(self.grid[0][0])
		self.grid[1][0].neighbors.remove(self.grid[0][0])
		while len(stack) > 0:
			cell = stack.pop()
			if cell.hasNeighbors():
				stack.append(cell)
				stack.append(cell.popNeighbor())
		 

class BabyCell:
	def __init__(self, row, col, grid):
		self.row = row
		self.col = col
		self.grid = grid
		self.floor = True
		self.wall = True
		self.neighbors = {}
	
	def addNeighbors(self):
		self.neighbors += self.top()
		self.neighbors += self.bottom()
		self.neighbors += self.left()
		self.neighbors += self.right()
		self.neighbors.discard(None)
	
	def hasNeighbors(self):
		return len(self.neighbors) > 0
	
	def popNeighbor(self):
		neighbor = self.neighbors.remove(choice(tuple(self.neighbors)))
		self.breakWall(neighbor)
		for cell in neighbor.neighbors:
			cell.neighbors.remove(neighbor)
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
		return self.grid[self.row-1][col] if self.row > 0 else None
	
	def bottom(self):
		return self.grid[self.row+1][col] if sel.row < len(self.grid)-1 else None
	
	def left(self):
		return self.grid[self.row][col-1] if sel.col > 0 else None
	
	def right(self):
		return self.grid[self.row][col+1] if sel.col < len(self.grid[self.row])-1 else None