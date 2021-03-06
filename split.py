import sys
import csv

# This will be solved be considering the whole thing as a directed and weighted graph.

# The set of all verticies
V = set([])
# The set of all edges. Note that a node N1 points at N2 with the weight w by E[N1] = [N2, w]
E = dict([])
# The list of all buyes
buyers = []

# Adds a vertex to V, if it does not already exists
def addToV(s):
    isVertex = False

    for v in V:
        if v.name == s:
            isVertex = True

    if not isVertex:
        V.add(Node(s))

# Returns the node v which has the name s.
# If not such v exists it returns False.
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

# Function for Adding multiple edges between multiple nodes.
def extendEdges(start, value, names):
    p = value/float(len(names))
    for n in names:
        if n != start.name:
            addToV(n)
            v = getV(n)
            start.addEdge(v, p)

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

# Initializes the graph.
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

# Finds a pseudo cycle.
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

# Returns a list containing the mid and the two branches.
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

# Function jused in breakCycles().
def appendCycles(C1, C2):
    C = [[n, 1] for n in C1]

    if len(C2) > 1:
        for n in C2[:-1:][::-1]:
            C.append([n, -1])
    else:
        C.append([C2[0], 1])

    return C

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

# This function will contract the graph.
# In other words it will given startNode and endNode romove excess edges
# and hence there will be less transactions.
def contractGraph(start):
    if start not in E.keys():
        return None

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
            if p[1] > 0:
                print(p[0].name, 'transfers to', v.name, p[1])
            else:
                print(v.name, 'transfers to', p[0].name, -p[1])
            total += 1
    print('')
    print('Total number of transactions is', total)

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

# Function to print number of edges.
def noEdges():
    s = 0

    for k in E.keys():
        s += len(E[k])

    return s

# Checks if an edge exists.
# If the edge from n1 to n2 exists it is returned otherwise False.
def inE(n1, n2):
    if n1 in E.keys():
        for e in E[n1]:
            if n2 == e[0]:
                return e
    return False

# Reads the csv-file
with open(sys.argv[1], 'rt') as f:
    reader = csv.reader(f)
    for row in reader:
        addToV(row[0])
        node = getV(row[0])

        if node not in buyers:
            buyers.append(node)

        extendEdges(node, float(row[1]), row[2::])

print('First print')
print(noEdges())
printPayees()
#print(makeTransfers(True))

print('')
print('Minimizing number of transactions')
for b in buyers:
    contractGraph(b)

print('')
print('Second print')
print(noEdges())
printPayees()
#print(makeTransfers(True))
