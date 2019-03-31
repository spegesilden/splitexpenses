# splitexpenses
It is a program for when you are splitting expenses with other people and want to minimize the number of transactions.

# What it is
The idea is that if you are a set of people who would like to share some expenses this would be a way to calculate how much each owes one another.
Say a person covers for a subset A of the people and another person covers for a subset B of the people, then the program should be considering every possibility of whether A overlaps B or if A is contained in B, etc.
The task is then to minimize the number of transactions so that everyone gets the amount of money they need.

# Mandatory argument
The program takes a mandatory argument which is the path to the csv file containing the data. Every line should reflect that one person, say Bob, has covered, say $20, for several other persons, say Wanda and Eric. The line is comma separated and should start with who has covered for the expense, then the amount of money, followed all the people who have been covered for including the one who covered if that person did participate in the expense. So in our example, a correct entry would be:

Bob,20,Wanda,Bob,Eric

# A bit about the solution
I have treated the problem as a graph problem, where the graph will be a weighted and directed graph. Furthermore, if a vertex A points at B with weight w, then B owes A w in cash. I think I just needed a convention, and this makes it easy to see how much A is owed by the others.
To complete the task I consider pseudo-cycles, that is if we have two vertices with two paths from one to the other this is considered as a pseudo-cycle. The idea is to find every pseudo-cycles and break it in a cash flow preserving way.
Having found a pseudo-cycle I simply remove one edge and update the weight of every other edge in the pseudo-cycle with respect to the removed weight. There are two scenarios, one that changes the sign and one which conserves it.
All the vertices I need to consider are the ones who have been covering for others since they are the only ones who give rise to pseudo-cycles.
