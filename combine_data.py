import os
import pandas as pd
import csv

# Directory containing the CSV files
directory = './data/'

merge_file = open('merged/merged_4.csv', 'a', newline='')
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
            except:
                print(row)



merge_file.close()

csv_file = open('merged/merged_4.csv', 'r', newline='')
# Count the number of rows
num_rows = sum(1 for row in csv_file)
# Print the result
print(f"The CSV file has {num_rows} rows.")