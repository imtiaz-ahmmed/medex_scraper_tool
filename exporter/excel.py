import pandas as pd
from datetime import datetime
import os

def export_excel(rows, section):
    os.makedirs("data", exist_ok=True)
    df = pd.DataFrame(rows)
    name = f"data/{section}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    df.to_excel(name, index=False)
    return name
