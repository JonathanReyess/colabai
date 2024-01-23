import sqlite3
import pandas as pd

# Read CSV into DataFrame
df = pd.read_csv("Pathways DB/database/courses.csv")
df.columns = df.columns.str.strip()

# Connect to SQLite database
connection = sqlite3.connect("pathways.db")
# Use Pandas to insert data into the table
df.to_sql("courses", connection, if_exists='replace', index=False)

# Close the connection
connection.close()
