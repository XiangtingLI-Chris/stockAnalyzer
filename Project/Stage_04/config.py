from pathlib import Path

# \Project\Stage_04
STAGE4_DIR = Path(__file__).resolve().parent

# \Project
PROJECT_DIR = STAGE4_DIR.parent

# \Project\Stage_03
STAGE3_DIR = PROJECT_DIR / "Stage_03"

# \Project\Stage_03\output
STAGE3_OUTPUT_DIR = STAGE3_DIR / "output"

# Path of the input Excel file
IN_PATH = STAGE3_OUTPUT_DIR / "stage3_common_months.xlsx"

# \Project\Stage_04\output
STAGE4_OUTPUT_DIR = STAGE4_DIR / "output"

# Path of the output Excel file
OUT_PATH = STAGE4_OUTPUT_DIR / "stage4_analyze_reason.xlsx"
