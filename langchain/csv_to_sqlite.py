import sqlite3
import pandas as pd

def convert(csv_file, sqlite_db, table):

    df = pd.read_csv(csv_file)
    df.columns = df.columns.str.strip()

    connection = sqlite3.connect(sqlite_db)

    df.to_sql(table, connection, if_exists='replace', index=False)

    connection.close()

if __name__ == "__main__":

    csv_file = "data/pathways_exports/courses.csv"
    sqlite_db = "data/sample_database/pathways.db"
    table = "courses"

    convert(csv_file, sqlite_db, table)
