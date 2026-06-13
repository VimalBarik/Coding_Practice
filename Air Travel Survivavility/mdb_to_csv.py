import subprocess
import pandas as pd
from io import StringIO
import os

mdb_file = "avall.mdb"

# Get list of tables
tables_raw = subprocess.check_output(['mdb-tables', '-1', mdb_file])
tables = tables_raw.decode('utf-8').splitlines()

# Create output folder
os.makedirs("csv_output", exist_ok=True)

for table in tables:
    if not table.strip():
        continue
    print(f"Exporting: {table}")
    try:
        data = subprocess.check_output(['mdb-export', mdb_file, table])
        df = pd.read_csv(StringIO(data.decode('utf-8')))
        df.to_csv(f"csv_output/{table}.csv", index=False)
    except Exception as e:
        print(f"Failed to export table '{table}': {e}")
