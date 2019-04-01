from classes import Maze
from random import choice
from queue import Queue

def dfs(maze):
	mouse = maze.mouse
	visited = set()
	stack = [mouse.node]
	visited.add(mouse.node)
	count = 0
	while len(stack) > 0:
		cell = stack.pop()
		mouse.moveTo(cell)
		if cell.hasCheese:
			count += 1
			mouse.eatCheese()
		nbs = [nb for nb in cell.neighbors if nb not in visited]
		if len(nbs) > 0:
			nb = choice(nbs)
			visited.add(nb)
			stack.append(cell)
			stack.append(nb)
	maze.show(30)
	print(count)

def bfs(maze):
	mouse = maze.mouse
	hand = maze.hand
	visited = set()
	queue = Queue()
	queue.put(mouse.node)
	queue.put(None)
	depth = 0
	found = False
	while not queue.empty() and not found:
		cell = queue.get()
		if cell is None:
			depth += 1
		else:
			found = hand.search(cell, depth)
			nbs = [nb for nb in cell.neighbors if nb not in visited]
			for nb in nbs:
				queue.put(nb)
		

bfs(Maze(25,25,10))