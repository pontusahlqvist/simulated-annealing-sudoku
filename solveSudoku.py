import copy
import numpy as np
import matplotlib.pyplot as plt

def costOfList(l):
	dim = len(l)
	cost = 0
	for i in range(dim):
		cost += abs(l.count(i+1) - 1)
	return cost

def costFunction(state):
	cost = 0
	dim = len(state)
	for i in range(dim):
		row = state[i]
		col = [r[i] for r in state]
		sqrt = int(dim**0.5)
		colInd = ((i%sqrt))*sqrt 
		rowInd = int(i/sqrt)*sqrt
		square = [state[r][c] for r in range(rowInd,rowInd + sqrt) for c in range(colInd, colInd + sqrt)]
		cost += costOfList(row)
		cost += costOfList(col)	
		cost += costOfList(square)
	return cost

def findNeighbor(inState, puzzle_state):
	outState = copy.deepcopy(inState)
	dim = len(inState)
	randRow1 = np.random.randint(dim)
	randCol1 = np.random.randint(dim)
	while not puzzle_state[randRow1][randCol1] == 0:
		randRow1 = np.random.randint(dim)
		randCol1 = np.random.randint(dim)
	randRow2 = randRow1
	randCol2 = randCol1
	while (randRow2 == randRow1) or (randCol2 == randCol1) or (not puzzle_state[randRow2][randCol2] == 0):
		randRow2 = np.random.randint(dim)
		randCol2 = np.random.randint(dim)

	#print "%d,%d  and  %d,%d"%(randRow1,randCol1,randRow2,randCol2)

	outState[randRow1][randCol1] = inState[randRow2][randCol2]
	outState[randRow2][randCol2] = inState[randRow1][randCol1]

	return outState

def printState(state):
	dim = len(state)
	sqrt = int(dim**0.5)
	print ''
	for ind,row in enumerate(state):
		if ind%(int(sqrt)) == 0 and not ind == 0:
			print "-"*(dim + sqrt + 1)
		s = '|'
		for i in range(sqrt):
			s = s + "".join([str(d) for d in row[i*sqrt:(i+1)*sqrt]]) + '|'
		print s
	print ''

puzzle_state = [[1,0,0,4],[0,2,1,0],[3,0,0,2],[2,0,3,0]]
dim = len(puzzle_state)
digit_count = [0]*dim
for row in puzzle_state:
	for d in row:
		if d == 0:
			continue
		digit_count[d-1] += 1

state = copy.deepcopy(puzzle_state)
for i in range(dim):
	for j in range(dim):
		if puzzle_state[i][j] == 0:
			shuffledRange = range(dim)
			np.random.shuffle(shuffledRange)
			for k in shuffledRange:
				if digit_count[k] < dim:
					state[i][j] = k+1
					digit_count[k] += 1
					break
		else:
			state[i][j] = puzzle_state[i][j]

print "Puzzle State (0s are undetermined numbers)"
printState(puzzle_state)
print "Initial Guess"
printState(state)
oldCost = costFunction(state)
print "Initial Cost = %d"%oldCost

tempUnit = 0.1
temp     = 10*tempUnit
tempUpdateFrequency = 5000
costs = []
for i in range(100000):
	costs.append(oldCost)
	if i%tempUpdateFrequency == 0 and temp > tempUnit:
		print "iteration %d, decreasing temp. Current cost = %d"%(i,oldCost)
		temp -= tempUnit
	newState = findNeighbor(state,puzzle_state)
	newCost = costFunction(newState)
	if newCost == 0:
		state = copy.deepcopy(newState)
		break
	while newCost > oldCost and np.random.rand() > np.exp(-(newCost - oldCost) / temp):
		newState = findNeighbor(state,puzzle_state)
		newCost = costFunction(newState)
	oldCost = newCost
	state = copy.deepcopy(newState)

print '\n\n****************************\nFinal State:'
printState(state)
print "Final cost = %d"%costFunction(state)
plt.plot(range(len(costs)), costs)
plt.ylim(0,40)
plt.savefig('costFunction.jpg')
