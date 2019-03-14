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

### Might be unneecessary
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

    def __bool__(self):
        if self.name is not None:
            return True

        return False

    def __len_(self):
        return len(self.name)

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
        #addToU(self, node, True)
        #addToU(node, self, False)

# Function for Adding multiple edges between multiple nodes.
def extendEdges(start, value, names):
    p = value/float(len(names))
    for n in names:
        if n != start.name:
            addToV(n)
            v = getV(n)
            start.addEdge(v, p)

### Might be unneecessary
# Removes zero-edges
def rmZeroEdges():
    toRemove = []

    for v, edges in E.items():
        for i, e in enumerate(edges):
            if e[1] == 0:
                toRemove.append([v, e[0]])

    for r in toRemove:
        rmEdge(r[0], r[1])

### Might be unneecessary
# Do I need this?
# Function to add a payee as a Node in V.
def createPayeeEdges(payees):
    for p in payees:
        E.setdefault(Node(p), [])

# Deletes the edge from start to end.
# Returns False is there is no edge.
def rmEdge(start, end):
    edge = inE(start, end)

    if len(E[start]) > 1:
        #print(E[start])
        E[start].remove(edge)
    else:
        del E[start]

    return edge

### Might be unneecessary
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
    C = False

    if v in E.keys():
        for e in E[v]:
            if e[0].visited:
                e[0].parent.append(v)
                return e[0]
            else:
                e[0].parent = [v]
                C = C or visit(e[0], start)

            if C:
                break

    return C

# Finds a cycle
def findCycle(start):
    start.visited = True
    C = False

    for e in E[start]:
        if e[0].visited:
            e[0].parent.append(start)
            return e[0]
        else:
            e[0].parent = [start]
            C = C or visit(e[0], start)

        if C:
            break

    return C

# Will return a list containing the mid and the two branches.
def getCycle(mid, node):
    C1 = [node]
    C2 = [node]

    # Function will return one branch
    def getC(n, cycle):
        cycle.append(n)
        while n != mid:
            n = n.parent[0]
            cycle.append(n)

    getC(node.parent[0], C1)
    getC(node.parent[1], C2)

    # Reduces so there is no loose end.
    s = mid

    while C1[-1] == C2[-1] and len(C1) > 1 and len(C2) > 1:
        s = C1[-1]
        if len(s.parent) <= 1:
            s.parent = []
        C1.remove(s)
        C2.remove(s)

    if len(C1[-1].parent) <= 1:
        C1[-1].parent = [s]
    if len(C2[-1].parent) <= 1:
        C2[-1].parent = [s]

    C1.append(s)
    C2.append(s)

    return [C1, C2]

# Checks if a cycle is extendable. Returns the nodes which should be manipulated.
def findExtendingNode(C):
    for i in range(1, len(C)):
        start = C[i][0]
        end = C[i - 1][0]
        if C[i][1] == -1:
            start = C[i - 1][0]
            end = C[i][0]

        for e in E[start]:
            if e[0] not in [c[0] for c in C]:
                return [start, end, e[0], i]
    return False

# Extends a cycle if it is too small.
def extendCycle(C):
    Nodes = findExtendingNode(C)

    def updateParent(node, parent):
        if len(node.parent) > 1:
            node.parent.remove(C[1][0])
            node.parent.append(parent)
        else:
            node.parent = [parent]

    if Nodes:
        #print(Nodes)
        updateParent(Nodes[2], Nodes[0])
        updateParent(Nodes[1], Nodes[2])

        e = rmEdge(Nodes[0], Nodes[1])

        Nodes[2].addEdge(Nodes[1], 0)

        i = Nodes[3]
        if C[i][1] == -1:
            if inE(Nodes[1], Nodes[2]):
                C.insert(i - 1, [Nodes[2], -1])
            else:
                C.insert(i - 1, [Nodes[2], 1])
        else:
            if inE(Nodes[1], Nodes[2]):
                C.insert(i, [Nodes[2], -1])
            else:
                C.insert(i, [Nodes[2], 1])

        #e1 = inE(Nodes[1], Nodes[2])

    return Nodes

# This is called if there is an odd number of edges.
# It will change the cycle in order to get an even number of edges.
# Returns the new change.
def changeCycle(C):
    # Nodes
    end = C[0][0]
    mid = C[1][0]
    parent = C[2][0]

    # Multipliers
    m = C[1][1]
    p = C[2][1]

    e = rmEdge(mid, end)
    change = e[1]
    e1 = inE(parent, end)

    # Removes the edge which is not in the cycle.
    updateEdge(parent, mid, change, p)

    # Adds or updates edge between parent and end.
    parent.addEdge(end, change)
    if e1:
        C[2][1] = 1
    else:
        C[2][1] = -1

    end.parent.remove(mid)
    end.parent.append(parent)

    # Remove the second last element from the cycle.
    C.remove(C[1])

# Function jused in breakCycles().
def appendCycles(C1, C2):
    C = [[n, 1] for n in C1]

    if len(C2) > 1:
        for n in C2[:-1:][::-1]:
            C.append([n, -1])
    else:
        C.append([C2[0], 1])

    return C

def cycleValue(C, start):
    #print('Printing vlaue')
    s = 0

    for i in range(start, len(C) - 1):
        c1 = C[i][0]
        c2 = C[i + 1][0]
        #print(i)
        #print(c1, c2, C[i + 1][1])
        #print(c1, inE(c1, c2))
        #print(c2, inE(c2, c1))
        if C[i + 1][1] == -1:
            s += inE(c1, c2)[1]
        else:
            s += inE(c2, c1)[1]

    return s

# Removes or breaks a cycle
def breakCycle(C1, C2):
    l1 = len(C1)
    n = l1 + len(C2)
    change = None
    C = []

    # Appends the cycles
    if l1 > 2:
        C = appendCycles(C1, C2)
    else:
        C = appendCycles(C2, C1)

    end = C[0][0]
    mid = C[1][0]
    parent = C[2][0]

    # Removes one edge.
    if inE(C[0][0], C[1][0]):
        change = rmEdge(C[0][0], C[1][0])[1]
    else:
        change = rmEdge(C[1][0], C[0][0])[1]

    for i in range(2, len(C)):
        a = C[i][1]
        updateEdge(C[i][0], C[i - 1][0], change, a)

# This will update an edge if it exists.
def updateEdge(start, end, change, orientation = 1):
    e = inE(start, end)

    if orientation == -1:
        e = inE(end, start)

    if e:
        e[1] -= orientation * change

### Might be unneecessary
# Find n to be the first in route which is not in E.
def findNonEdge(route):
    n = 1
    while route[n][1] and n < len(route) - 1:
        n += 1

    if not route[n][1]:
        return n - 1
    return False

### Might be unneecessary
def updateEdges(v, change):
    p = v.parent
    if p.parent is None:
        updateEdge(v, p, change)

### Might be unneecessary
# Find all edges in U which are not in E.
def findNonEdges():
    edges = []

    for v in U.keys():
        for e in U[v]:
            if not e[1] and len(U[v]) > 1:
                edges.append([v, e[0]])

    return edges

### Might be unneecessary
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
        C = getCycle(start, end)
        breakCycle(C[0], C[1])

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
def makeTransfers(a = False):
    total = 0
    N = dict([])

    for v, edges in E.items():
        N.setdefault(v, [0, 0, 0])
        for e in edges:
            N.setdefault(e[0], [0, 0, 0])
            if e[1] > 0:
                N[v][0] += e[1]
                N[e[0]][1] += e[1]
            else:
                N[v][1] -= e[1]
                N[e[0]][0] -= e[1]

    for v, s in N.items():
        N[v][2] = N[v][0] - N[v][1]
        if a:
            print(v, N[v])
        total += s[2] #- s[1]

    return total

# Function to print the edges.
def printEdges():
    for k in E.keys():
        print(str(k) + " points at:")
        for e in E[k]:
            print(e[0])

def printCycle(C):
    for i in range(0, len(C) - 1):
        if C[i+1][1] == -1:
            print(C[i][0], C[i+1], inE(C[i][0], C[i+1][0]))
        else:
            print(C[i+1], C[i][0], inE(C[i+1][0], C[i][0]))

# Function to print number of edges.
def noEdges():
    s = 0

    for k in E.keys():
        s += len(E[k])

    return s

def inE(n1, n2):
    if n1 in E.keys():
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
print(noEdges())
#printPayees()
#print(makeTransfers(True))
print('')

n = getV('Karoline')
print(findCycle(n))
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
print(noEdges())
#printPayees()
#print(makeTransfers(True))
