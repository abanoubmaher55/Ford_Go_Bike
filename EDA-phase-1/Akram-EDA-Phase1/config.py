
"""Configuration settings for the Ford GoBike data analysis pipeline.

Defines file paths, dataset reference anchors, target column groupings,
and imputation values used across preprocessing and modeling scripts.
"""

from pathlib import Path

#File Paths & Temporal Anchors
BASE_DIR: Path = Path(__file__).resolve().parent
FILE_PATH: Path = BASE_DIR / "fordgobike-tripdataFor201902.csv"
CURRENT_YEAR: int = 2019

#Column Groupings
CAT_COLS: list[str] = [
    "user_type",
    "member_gender",
    "bike_share_for_all_trip",
]


DATA_STAT: list[str] = [
    "age",
    "duration_min",
    "duration_sec",
    "member_birth_year",
    "bike_id",
]

#Imputation Values
GENDER_FILL: str = "Unknown"