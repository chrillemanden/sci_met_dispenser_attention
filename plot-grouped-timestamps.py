import matplotlib.pyplot as plt
import csv

year = 2020
activations = {}

with open ('activations_all.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    lines = 0
    for row in csv_reader:
        lines += 1
        activations[row[1]] = activations.get(row[1], 0) + 1
        #print (row)

test_file = open("test_file.csv", "w+")
for key, value in activations.items():
    test_file.write("%s,%s\n" % (key, value))


print(lines)
print (sum(activations.values()))
print (activations)



dates = activations.keys()
values = activations.values()
# print(dates)
# print(values)

# for i, d in enumerate(dates):
#     dates[i] = str(i) + d

# print(dates)
# plt.bar(dates, values, 0.5, color='g')
# plt.show()
#ax = plt.subplot(111)
#ax.bar(dates, values, 0.5, color='g')

#ax.xaxis_date()

# plt.bar(*zip(*activations.items()))
# plt.show()