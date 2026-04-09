from config import IN_PATH, OUT_PATH
from analyze_reason import analyze_reason
import pandas as pd

def run_stage4_pipeline(in_path: str = IN_PATH, out_path: str = OUT_PATH) -> None:
    # Read the input Excel file
    df = pd.read_excel(in_path)

    # Add a column based on `analyze_reason` function
    df["上涨原因"] = df.apply(
        lambda row: analyze_reason(row["股票名称"], row["月份"], row.get("涨幅次数")),
        axis=1
    )

    # Output the file
    df.to_excel(out_path, index=False)

    print(f"Already output: {out_path}, totally {len(df)} lines.")