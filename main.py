from classes import Maze
from random import choice
maze = Maze(5,5,2)
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
		cell.hasCheese = False
	nbs = [nb for nb in cell.neighbors if nb not in visited]
	if len(nbs) > 0:
		nb = choice(nbs)
		visited.add(nb)
		stack.append(cell)
		stack.append(nb)
maze.show(0)