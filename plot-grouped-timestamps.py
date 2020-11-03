#import matplotlib
import csv

with open ('activations.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    lines = 0
    for row in csv_reader:
        lines += 1

print(lines)
