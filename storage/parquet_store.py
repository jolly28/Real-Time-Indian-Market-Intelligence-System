import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from pathlib import Path

def save(records, path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(records)
    pq.write_table(pa.Table.from_pandas(df), path)
