import pandas as pd
import os

os.makedirs("data", exist_ok=True)


def export(rows):
    if not rows:
        print("❌ No data to export")
        return

    df = pd.DataFrame(rows)

    df.to_csv("data/brands.csv", index=False)

    with pd.ExcelWriter("data/medex_data.xlsx") as writer:
        df.to_excel(writer, sheet_name="Brands", index=False)

    print("📁 Exported", len(df), "rows to Excel & CSV")
