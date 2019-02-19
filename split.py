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
        sn = inE(self, node)
        ns = inE(node, self)

        if sn:
            sn[1] += value
        elif ns:
            ns[1] -= value
        else:
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

    if v in E.keys():
        for e in E[v]:
            e[0].parent.append(v)
            if e[0].visited:
                return e[0]
            else:
                visit(e[0], start)

# Finds a cycle
def findCycle(start):
    start.visited = True

    for e in E[start]:
        e[0].parent.append(start)
        if e[0].visited:
            return e[0]
        else:
            visit(e[0], start)

    return False

# Will return a list containing the mid and the two branches.
def getCycle(start, node):
    C1 = [node]
    C2 = [node]

    # Function will return one branch
    def getC(n, cycle):
        while n != start:
            cycle.append(n)
            n = n.parent[0]

    getC(node.parent[0], C1)
    getC(node.parent[1], C2)

    # Reduces so there is no loose end.
    s = start

    while C1[-1] == C2[-1]:
        s = C1[-1]
        C1.remove(s)
        C2.remove(s)

    C1.append(s)
    C2.append(s)

    return [C1, C2]

# This is called if there is an odd number of edges.
# It will change the cycle in order to get an even number of edges.
# Returns the new change.
def changeCycle(C):
    # Nodes
    end = C[-1][0]
    mid = C[-2][0]
    parent = C[-3][0]

    # Multipliers
    m = C[-2][1]
    p = C[-3][1]

    change = inE(mid, end)[1]
    isEdge = inE(parent, end)

    # Removes the last edge and updates the second last one.
    e = rmEdge(mid, end)
    if mid.parent == [parent]:
        updateEdge(parent, mid, -(m*e[1]))
    else:
        updateEdge(parent, mid, m*e[1])

    # Adds or updates last edge.
    if isEdge:
        isEdge[1] -= m*change
    else:
        parent.addEdge(end, change)

# Function used in breakCycle().
def update(C, change):
    for i in range(0, len(C) - 1, 2):
        updateEdge(C[i][0], C[i - 1][0], C[i - 1][1]*change)
        updateEdge(C[i + 1], C[i], *change)

# Function jused in breakCycles().
def appendCycles(C1, C2):
    C = [[n, 1] for n in C1[1::]]

    for n in C2[:-1:]:
        C.append([n, -1])

    return C

# Removes or breaks a cycle
def breakCycle(C1, C2):
    l1 = len(C1)
    l2 = len(C2)
    l = l1 + l2 - 2
    removedEdge = None
    wasC1 = False
    C = []

    # Removes one edge.
    if l1 > 2:
        wasC1 = True
        removedEdge = rmEdge(C1[1], C1[0])
        C = appendCycles(C1, C2)
    else:
        removedEdge = rmEdge(C2[1], C2[0])
        C = appendCycles(C2, C1)

    print(C1)
    print(C2)
    print(C)
    change = removedEdge[1]

    if l % 2 == 0:
        changeCycle(C)
        update(C2, -change)
    else:
        update(C1, -change)
        update(C2[1::], change)

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
def contractGraph(start):
    initialize()
    end = findCycle(start)

    while end:
        L = getCycle(start, end)
        breakCycle(L[0], L[1])

        initialize()
        end = findCycle(start)

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

def inE(n1, n2):
    for e in E[n1]:
        if n2 == e[0]:
            return e
    return False

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

#node = getV('Karoline')
#print(node in E[node])
#print(noEdges())
#contractGraph(node)
#print(noEdges())


print('First print')
#printPayees()
print('')
makeTransfers()
print('')

n = getV('Karoline')
contractGraph(n)
#initialize()
#n = getV('Nina')
#print()
#print('Starting with', n)
#contractGraph(n)
#s = findCycle(n)
#print(s)

##print(noEdges())
#for b in buyers:
#    if b in E.keys():
#        contractGraph(b)
##print(noEdges())

print('')
print('Second print')
#printPayees()
print('')
makeTransfers()
