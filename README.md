# splitexpenses
Is a program for when you are splitting expenses with other people and want to minimize the number of transactions.

The idea is that if you are a set of people who would like to share some expenses this would be a way to calculate how much each owes one another.
Say a person covers for a subset A of the people and another person covers for a subset B of the people, then the program should be considering every possibility of whether A overlaps B or if A is contained in B, etc.
The task is then to minimize the number of transactions so that everyone gets the amount of money they need.

The program takes a mandatory argument which is the path to the csv file containing the data. Every line should reflect that one person, say Bob, has covered, say $20, for several other persons, say Wanda and Eric. The line is comma separated and should start with who has covered for the expense, then the amount of money, followed all the people who have been covered for including the one who covered if that person did participate in the expense. So in our example, a correct entry would be:

Bob,20,Wanda,Bob,Eric
