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

def addToV(s):
    isVertex = False

    for v in V:
        if v.name == s:
            isVertex = True

    if not isVertex:
        V.add(Node(s))

def getV(s):
    for v in V:
        if v.name == s:
            return v

    return False

# The nodes of V consist of objects of the class Node.
class Node:
    def __init__(self, name):
        self.name = name
        self.visited = False
        self.parent = []
        E.setdefault(self, [])

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
            addToV(n)
            v = getV(n)
            start.addEdge(v, p)

# Removes zero-edges
def rmZeroEdges():
    toRemove = []

    for v, edges in E.items():
        for i, e in enumerate(edges):
            if e[1] == 0:
                toRemove.append([v, e[0]])

    for r in toRemove:
        rmEdge(r[0], r[1])

# Do I need this?
# Function to add a payee as a Node in V.
def createPayeeEdges(payees):
    for p in payees:
        E.setdefault(Node(p), [])

# Deletes the edge from start to end.
# Returns False is there is no edge.
def rmEdge(start, end):
    edge = False

    for i, e in enumerate(E[start]):
        if e[0] == end:
            edge = e

    if len(E[start]) > 1:
        E[start].remove(edge)
    else:
        del E[start]

    return edge

def markEdge(start, end):
    for e in E[start]:
        if e[0] == end:
            e[1] = 0

# Initializes the graph once again.
def initialize():
    for v in V:
        v.visited = False
        v.parent = []

# A recursive function used in findCycle.
def visit(v, start):
    v.visited = True

    #if v.visited:
    #    return v

    #if len(E[v]) == 0:
    #    #print(len(E[start]), len(E[p]), len(E[v]))
    #    #print(v, p, E[p])
    #    visit(p, p.parrent, start, l)
    for e in E[v]:
        e[0].parent.append(v)
        if e[0].visited:
            #e[0].parent.append(v)
            return e[0]
        else:
            #print(e[0], v, p)
            #e[0].parent.append(v)
            visit(e[0], start)

    #v.visited = False

# Finds a cycle
def findCycle(start):
    start.visited = True

    for e in E[start]:
        e[0].parent.append(start)
        if e[0].visited:
            #e[0].parent.append(start)
            return e[0]
        else:
            #e[0].parent.append(start)
            visit(e[0], start)

    return False

def getCycle(start, node):
    C = [start]
    C2 = [node]

    def getC(n, cycle):
        while n != start:
            cycle.append(n)
            n = n.parent[0]

    getC(node.parent[0], C)
    getC(node.parent[1], C2)

    s = start

    while C[-1] == C2[-1]:
        s = C[-1]
        C.remove(s)
        C2.remove(s)

    return [s, C, C2]

# This is called if there is an odd number of edges.
# It will change the cycle in order to get an even number of edges.
# Returns the new change.
def changeCycle(start, end, change):
    p = end.parent
    isEdge = rmEdge(start, p)

    updateEdge(p, end, -change)

    if isEdge:
        change += isEdge[1]

    isEdge = rmEdge(p, start)

    if isEdge:
        change -= isEdge[1]

    return change


# Removes or breaks a cycle
def breakCycle(v, start, length):
    edge = rmEdge(v, start)

    child = v
    p = v.parent

    if length % 2 == 1:
        edge = changeCycle(start, v, edge)
        child = p
        p = p.parent

    while not (p.parent is None):
        updateEdge(p, p.parent, edge)
        updateEdge(child, p, -edge)

        p = p.parent
        child = p
        p = p.parent

    updateEdge(child, p, -edge)

# Find n to be the first in route which is not in E.
def findNonEdge(route):
    n = 1
    while route[n][1] and n < len(route) - 1:
        n += 1

    if not route[n][1]:
        return n - 1
    return False

# This will update an edge if it exists.
def updateEdge(start, end, change):
    for e in E[start]:
        if e[0] == end:
            e[1] += change

def updateEdges(v, change):
    p = v.parent
    if p.parent is None:
        updateEdge(v, p, change)

# Find all edges in U which are not in E.
def findNonEdges():
    edges = []

    for v in U.keys():
        for e in U[v]:
            if not e[1] and len(U[v]) > 1:
                edges.append([v, e[0]])

    return edges

# Finds an edge in U which is in E.
def findOther(nonEdge):
    for e in U[nonEdge[0]]:
        if e[1]:
            return e[0]

# This function will contract the graph.
# In other words it will given startNode and endNode romove excess edges
# and hence there will be less transactions.
def contractGraph(start, end, values, seen, route):
    edges = findNonEdges()

    for e in edges:
        e.append(findOther(e))

    for e in edges:
        if not (e[2] is None):
            updateEdge(e[0], e[1], e[2])

# Function to print the payees.
def printPayees():
    total = 0
    for v in E.keys():
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
        if s < 0:
            total -= s
        else:
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
        addToV(row[0])
        node = getV(row[0])

        if node not in buyers:
            buyers.append(node)

        extendEdges(node, float(row[1]), row[2::])
        #createPayeeEdges(row[2::])


#print('First print')
##printPayees()
#print('')
#makeTransfers()
#print('')
#
#n1 = Node('Karoline')
#n2 = Node('Sisse')
#contractGraph(n1, n2, [], [n1], [n1])
#rmZeroEdges()
#
##for b1 in buyers:
##    for b2 in buyers:
##        if b1 != b2:
##            contractGraph(b1, b2, [], [b1], [b1])
#
#print('')
#print('Second print')
##printPayees()
#print('')
#makeTransfers()
