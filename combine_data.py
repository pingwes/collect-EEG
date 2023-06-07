import os
import pandas as pd
import csv

# Directory containing the CSV files
directory = './data/'

merge_file = open('merged/merged_0.csv', 'a', newline='')
merge_writer = csv.writer(merge_file)

# Iterate through each file in the directory
for filename in os.listdir(directory):
    if filename.endswith(".csv"):
        filepath = os.path.join(directory, filename)
        print(filepath)
        individual_file = open(filepath, 'r')
        reader = csv.reader(individual_file)
        for row in reader:
            try:
                if int(row[1]) <= 5:
                    merge_writer.writerow(row[:2])
            except Exception as E:
                print(E)
                # print(row)

merge_file.close()

csv_file = open('merged/merged_0.csv', 'r', newline='')
# Count the number of rows
total_rows = 0
one_count = 0
two_count = 0
three_count = 0
four_count = 0
for row in csv_file:
    total_rows += 1
    classification = row.split(",")[-1].strip()

    if classification == "1": one_count += 1
    if classification == "2": two_count += 1
    if classification == "3": three_count += 1
    if classification == "4": four_count += 1

# Print the result
print(f"The CSV file has {total_rows} rows.")
print(f"{one_count} blue values.")
print(f"{two_count} red values.")
print(f"{three_count} green values.")
print(f"{four_count} yellow values.")