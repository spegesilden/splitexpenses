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
        self.unblocked = True
        self.parent = None

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
            V.add(Node(n))

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

# Deletes the edge from start to end
def rmEdge(start, end):
    edge = None
    for i, e in enumerate(E[start]):
        if e[0] == end:
            edge = e
    if len(E[start]) > 1:
        E[start].remove(edge)
    else:
        del E[start]

def markEdge(start, end):
    for e in E[start]:
        if e[0] == end:
            e[1] = 0

# Initializes the graph once again
def initialize():
    for v in V:
        v.unblocked = True
        v.parent = None

# A recursive function used in findCycles
def visit(v, p, start):
    v.unblocked = False
    v.parent = p

    if v == start:
        return v

    for e in E[v]:
        if e[0].unblocked:
            visit(v, p, start)

    v.unblocked = True

# Find a cycle
def findCycle(start):
    for e in E[start]:
        visit(e[0], start, start)

    return False


# Find n to be the first in route which is not in E.
def findNonEdge(route):
    n = 1
    while route[n][1] and n < len(route) - 1:
        n += 1

    if not route[n][1]:
        return n - 1
    return False

# Given a route from start to end the function will delete this route
# and then update the edge from start to end.
def updateEdge(start, end, other):
    value = 0
    n = 0

    for e in E[end]:
        if e[0] == start:
            value = e[1]
    for i, e in enumerate(E[start]):
        if e[0] == other:
            n = i

    E[start][n][1] -= value
    markEdge(end, start)

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
        node = Node(row[0])

        if node not in buyers:
            buyers.append(node)

        V.add(node)
        extendEdges(node, float(row[1]), row[2::])
        #createPayeeEdges(row[2::])

#print(findNonEdges())

print('First print')
#printPayees()
print('')
makeTransfers()
print('')

n1 = Node('Karoline')
n2 = Node('Sisse')
contractGraph(n1, n2, [], [n1], [n1])
rmZeroEdges()

#for b1 in buyers:
#    for b2 in buyers:
#        if b1 != b2:
#            contractGraph(b1, b2, [], [b1], [b1])

print('')
print('Second print')
#printPayees()
print('')
makeTransfers()
