# Gandhali Shastri



# try:
    # import Queue as Q
# except ImportError:
    # import queue as Q
	
from Queue import Queue
import heapq
import sys

#https://stackoverflow.com/questions/19745116/python-implementing-a-priority-queue
#Python 2.4 (omega version) doesn't have PriorityQueue data structure, so PriorityQueue class is used.
class PriorityQueue(Queue):
    def __init__(self):
        self.items = []

    def push(self, priority):
        heapq.heappush(self.items, priority)

    def pop(self): 
        return heapq.heappop(self.items)

    def empty(self):
        return not self.items

#Creates dictionary using the input file.
def createDictionary(inputFile):
	f = open(inputFile,'r')

	routes = {}

	for line in f:
		if not 'END' in line:
			line = line.split()
			routes.setdefault(line[0], []).append((line[1],line[2]))
			routes.setdefault(line[1], []).append((line[0],line[2]))
			#https://stackoverflow.com/questions/3483520/use-cases-for-the-setdefault-dict-method
			#https://stackoverflow.com/questions/3199171/append-multiple-values-for-one-key-in-python-dictionary   
	f.close()
	return routes

#Uniform Cost Search algorithm is implemented using the following reference.
#http://aima.cs.berkeley.edu/algorithms.pdf   (pseudocode)
def searchUCS(map, start, destination):
	
	explored = set()	#expanded nodes
	route = []	#list of cities on the basis of minimum dist
	frontier = PriorityQueue()	#a priority queue ordered by city-dist
	frontier.push((0, [start]))	#queue initialized
	
	while frontier:

		if frontier.empty():	#no route
			print ('distance: infinity \nroute: \nnone')
			break
					
		dist, route = frontier.pop()	#pops city with least dist
		
		city = route[len(route)-1]

		if city not in explored:
			explored.add(city) 
	
			if city == destination:	#gets the optimal route
				route.append(dist)
				displayRoutes(map,route)
				return route
	
		elements = map[city]
		neighbor=[i[0] for i in elements]	#get child nodes
		
		for i in neighbor:
			if i not in explored:
				#calc total cost with cumulative dist
				totalDist = dist + int(getDist(map, city, i))
				temp = route[:]
				temp.append(i)
				
				frontier.push((totalDist, temp)) #final que
			
	return frontier

#Creates dictionary using the input file.
def heuristicDictionary(heuFile):
	f = open(heuFile, 'r')
	heu = {}
	for line in f:
		if not 'END' in line:
			line = line.split()
			heu.setdefault(line[0], []).append(line[1])
	#print(heu)		
	f.close()

	return heu
	
#Similar to UCS, except that it uses the getHeuristic() to calc totalDist.
def searchAS(map, straightLineDist, start, destination):
	
	explored = set() #expanded nodes
	route = []	#list of cities on the basis of minimum dist
	#frontier = Q.PriorityQueue()
	frontier = PriorityQueue()	#a priority queue ordered by city-dist
	initheu=int(straightLineDist[start][0])
	frontier.push((initheu, [start]))	#queue initialized
	
	while frontier:
		if frontier.empty():	#no route
			print ('distance: infinity\nroute:\nnone')
			return
		
		dist, route = frontier.pop()	#pops city with least dist
		city = route[len(route)-1]	
		 
		if city not in explored:	#gets the optimal route
			explored.add(city) 	
			if city == destination: 
				route.append(dist)
				
				displayRoutes(map,route)
				
				return route

		elements = map[city]	#xplores the child nodes
		neighbor=[i[0] for i in elements]	#neighbors of current city
		
		for i in neighbor:
			if i not in explored:
				#calc total cost with f(n)=g(n)+h(n)				
				totalDist = (dist - int(straightLineDist[city][0])) + int(getDist(map, city, i)) + int(getheuristic(straightLineDist,i))
				heur=int(getheuristic(straightLineDist,city))
				dist1=int(getDist(map, city, i))
				temp = route[:]
				temp.append(i)
				frontier.push((totalDist, temp))
	return frontier
	
#gets dist of current city to it's given neighbor
def getDist(map, current, neighbor):
	index = [i[0] for i in map[current]].index(neighbor)
	return map[current][index][1]
	
#gets heuristic value of given city	
def getheuristic(straightLineDist,current):
	return straightLineDist[current][0]

#display function
def displayRoutes(map,route):
	size = len(route)
	distance = route[-1]
	print ('distance: %s'%(distance))
	print ('route: ')
	count = 0
	while count < (size-2):
		km = getDist(map, route[count], route[count+1]) 
		print ('%s to %s, %s km' %(route[count],route[count+1],km))
		count+=1
	return	

#accepts cmd arg and calls other functions.	
def main():
	
	length = len(sys.argv)	#sys args assignment
	
	if length == 5 and sys.argv[1] == 'uninf':	#UCS algorithm
		inputFile = sys.argv[2]
		start = sys.argv[3]
		destination = sys.argv[4]
		map = createDictionary(inputFile)
		
		if start not in map:	#wrong city name
			print ((start) + "\tCity not found on the map!")
			return
		if destination not in map:
			print ((destination) + "\tCity not found on the map!")
			return
		
		route = []
		route = searchUCS(map, start, destination)	#calling UCS algo func
		
	elif length == 6 and sys.argv[1] == 'inf':	#A* algorihtm
			
			inputFile = sys.argv[2]
			heuFile = sys.argv[5]
			start = sys.argv[3]
			destination = sys.argv[4]
			
			map = createDictionary(inputFile)
			straightLineDist = heuristicDictionary(heuFile)
			
			if start not in map:
				print ((start) + "\tCity not found on the map!")
				return
			
			if destination not in map:
				print ((destination) + "\tCity not found on the map!")
				return
			
			route = []
			route = searchAS(map, straightLineDist, start, destination)	
	else:
		print('Wrong input!')	#if wrong number of arg are entered
main()


