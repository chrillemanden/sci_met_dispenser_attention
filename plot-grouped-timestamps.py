import matplotlib.pyplot as plt
import csv

year = 2020
activations = {}

with open ('activations_latest.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    lines = 0
    for row in csv_reader:
        lines += 1
        activations[row[1]] = activations.get(row[1], 0) + 1
        #print (row)

print(lines)
print (sum(activations.values()))
print (activations)

plt.bar(myDictionary.keys(), myDictionary.values(), width, color='g')