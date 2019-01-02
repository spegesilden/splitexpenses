import csv

# This will be solved be considering the whole thing as a directed and weighted graph.

# The set of all verticies
V = set([])
# The set of all edges. Note that a node N1 points at N2 with the weight w by E[N1] = [N2, w]
E = dict([])
# The set of all edges. Note that it is not directed
U = dict([])
# The list of all buyes
buyers = []

def addToU(start, end, direction):
    if start in U.keys():
        wasInU = False

        for i, e in enumerate(U[start]):
            if e[0] == end:
                wasInU = True
                U[start][i][1] = U[start][i][1] or direction

        if not wasInU:
            U[start].append([end, direction])
    else:
        U[start] = [[end, direction]]


# The nodes of V consist of objects of the class Node.
class Node:
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.name == other.name
        return False

    def __hash__(self):
        return self.name.__hash__()

    def __str__(self):
        return self.name.__str__()

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return str(self)

    def addEdge(self, node, value):
        wasThere = False

        if self in E.keys():
            for e in E[self]:
                if e[0] == node:
                    e[1] += value
                    wasThere = True

        # Adds the directed edge
        if not wasThere:
            E.setdefault(self, [[node, value]]).append([node, value])

        # Adds the undirected edge
        addToU(self, node, True)
        addToU(node, self, False)

# Function for Adding multiple edges between multiple nodes.
def extendEdges(start, value, names):
    p = value/float(len(names))
    for n in names:
        if n != start.name:
            start.addEdge(Node(n), p)

# Function to add a payee as a Node in V.
def createPayeeEdges(payees):
    for p in payees:
        E.setdefault(Node(p), [])

# Checks if a given route is actually possible
# i.e. if it is possible to travel along the route.
def isRoutable(route):
    for i in range(len(route)):
        if route[i+1] not in E[route[i]]:
            return False
    return True

# Checks whether there is an edge from start to end.
def isEdge(start, end):
    for e in E[start]:
        if end == e[0]:
            return True
    return False

# Deletes the edge from start to end
def delEdge(start, end):
    edge = None
    for e in E[start]:
        if e[0] == end:
            edge = e
    E[start].remove(edge)

# Finds all routes from start to end which a longer than 1 edge.
def findRoutes(start, end, route, seen):
    s = 0
    seen.append(route[-1])

    #for e in E[route[-1]]:
    #    if e[0] not in seen:

# TODO: Make this work!
# Given a route from start to end the function will delete this route
# and then update the edge from start to end.
def updateEdges(start, end, rmRoute):
    change = 0
    toDelete = []

    if len(rmRoute) > 2:
        for i in range(len(rmRoute) - 1):
            for e in E[rmRoute[i]]:
                if rmRoute[i+1] == e[0]:
                    change += e[1]
                    #delEdge(rmRoute[i], rmRoute[i+1])
                    toDelete.append([rmRoute[i], i+1])

        for d in toDelete:
            delEdge(d[0], rmRoute[d[1]])

        # Update the last edge
        if isEdge(start, end):
            for i, e in enumerate(E[start]):
                if end == e[0]:
                    E[start][i] = [e[0], e[1] + change]
                    if e[1]+change > 100:
                        print(start, e[0], e[1], change, e[1]+change)
        else:
            E.setdefault(start, [[end, change]]).append([end, change])
    #print('')

# TODO: Make this work!
# This function will contract the graph.
# In other words it will given startNode and endNode romove excess edges
# and hence there will be less transactions.
def contractGraph(startNode, endNode, values, seen, route):
    for e in E[route[-1]]:
        if e[0] not in seen:
            newValues = values[::]
            newValues.append(e[1])
            newRoute = route[::]
            newRoute.append(e[0])

            if e[0] == endNode and len(newRoute) > 2:
                change = sum(newValues)
                print('Updating edge', startNode, endNode)
                for r in newRoute:
                    print(r)
                updateEdges(startNode, endNode, newRoute)
            elif e[0] != startNode:
                newSeen = seen[::]
                newSeen.append(e[0])
                contractGraph(startNode, endNode, newValues, newSeen, newRoute)
            #seen.append(e[1])

# Function to print the payees.
def printPayees():
    total = 0
    for v in V:
        for p in E[v]:
            print(v.name, p[0].name, p[1])
            total += 1
    print(total)

# This will count how much the persons who should have money will get
# and print the total value.
# The function is only for validating if the program works
def makeTransfers():
    total = 0
    for v, edges in E.items():
        s = 0
        for e in edges:
            s += e[1]

        print(v, s)
        total += s
    print(total)

# Function to print the edges.
def printEdges():
    for k in E.keys():
        print(str(k) + " points at:")
        for e in E[k]:
            print(e[0])

# Function to print number of edges.
def noEdges():
    s = 0

    for k in E.keys():
        s += len(E[k])

    return s

# Reads the csv-file
with open('reciepts.csv', 'rt') as f:
    reader = csv.reader(f)
    for row in reader:
        node = Node(row[0])

        if node not in buyers:
            buyers.append(node)

        V.add(node)
        extendEdges(node, float(row[1]), row[2::])
        createPayeeEdges(row[2::])

for e in U[Node('Sisse')]:
    print(e[0], e[1])

#print('First print')
#printPayees()
#print('')
#makeTransfers()
#print('')
#
#for b1 in buyers:
#    for b2 in buyers:
#        if b1 != b2:
#            contractGraph(b1, b2, [], [b1], [b1])
#
#print('')
#print('Second print')
#printPayees()
#print('')
#makeTransfers()
