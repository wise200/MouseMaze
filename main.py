from classes import Maze
from random import choice

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

dfs(Maze(25,25,10,True))
