import os
import csv

# Directory containing the CSV files
directory = './data/EEG/movements_4'

merge_file = open('merged/merged_9.csv', 'a', newline='')
merge_writer = csv.writer(merge_file)


blue_count = 0
red_count = 0
green_count = 0
yellow_count = 0

# Iterate through each file in the directory
for filename in os.listdir(directory):
    if filename.endswith(".csv"):
        filepath = os.path.join(directory, filename)
        print(filepath)
        individual_file = open(filepath, 'r')
        reader = csv.reader(individual_file)
        for row in reader:
            try:
                if int(row[1]) < 3:

                    if int(row[1]) == 1:
                        if blue_count >= 368:
                            continue
                        blue_count += 1
                    elif int(row[1]) == 2:
                        if red_count >= 368:
                            continue
                        red_count += 1
                    elif int(row[1]) == 3:
                        if green_count >= 368:
                            continue
                        green_count += 1
                    elif int(row[1]) == 4:
                        if yellow_count >= 368:
                            continue
                        yellow_count += 1

                    merge_writer.writerow(row[:2])
            except Exception as E:
                print(E)
                # print(row)

merge_file.close()

print(f"{blue_count} blue values.")
print(f"{red_count} red values.")
print(f"{green_count} green values.")
print(f"{yellow_count} yellow values.")


csv_file = open('merged/merged_9.csv', 'r', newline='')
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
print(f"{one_count} up values.")
print(f"{two_count} down values.")
print(f"{three_count} green values.")
print(f"{four_count} yellow values.")