import csv

def append_column(input_csv, output_csv, source_column, target_column):
    with open(input_csv, 'r') as infile, open(output_csv, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        for row in reader:
            if len(row) > source_column and len(row) > target_column:
                row[target_column - 1] += row[source_column - 1]
            writer.writerow(row)

# Example usage:
input_file = 'data/pathways_exports/courses.csv'
output_file = 'data/pathways_exports/courses_merged.csv'
source_column_index = 3  # Assuming column indexing starts from 1
target_column_index = 4  # Assuming column indexing starts from 1

append_column(input_file, output_file, source_column_index, target_column_index)
