"""Shared paths, constants and loaders for every notebook in this repo."""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).parent
DATA_DIR = ROOT / "data"
OUT_DIR = ROOT / "outputs"                    # result CSVs (tracked)
INTERMEDIATE_DIR = OUT_DIR / "intermediate"   # household-level files (git-ignored)
FIG_DIR = ROOT / "images"
SEED = 42                                     # no notebook draws random numbers; kept for any future resampling

for _d in (OUT_DIR, INTERMEDIATE_DIR, FIG_DIR):
    _d.mkdir(parents=True, exist_ok=True)

# analysis windows
TIER_MIN_WEEK, TIER_MAX_WEEK = 17, 32      # spending tiers are fixed on these pre-campaign weeks
CAMP_MIN_WEEK, CAMP_MAX_WEEK = 33, 101     # campaign observation window (week 102 is a partial week)
MID_WEEK = (CAMP_MIN_WEEK + CAMP_MAX_WEEK) // 2   # split point of the placebo comparison
CELL_SIZE_THRESH = 30                      # campaign-by-tier cells below this are treated as reference-only

# Tier labels are the English names written to the CSVs. TIER_EN is kept as the label map applied when saving.
TIER3_ORDER = ["low", "mid", "high"]
TIER5_ORDER = ["q1 (lowest)", "q2", "q3", "q4", "q5 (highest)"]
TIER_EN = {"low": "low", "mid": "mid", "high": "high"}


def _as_tiers(df):
    df["tier3"] = pd.Categorical(df["tier3"], categories=TIER3_ORDER, ordered=True)
    df["tier5"] = pd.Categorical(df["tier5"], categories=TIER5_ORDER, ordered=True)
    return df


def load_tiers():
    """Household table written by h2_stage1_2: pre-period spend, tiers, will_receive (index = household_key)."""
    return _as_tiers(pd.read_csv(INTERMEDIATE_DIR / "tier_households.csv", index_col="household_key"))


def load_panel():
    """Household-week panel (weeks 33-101) written by h2_stage3."""
    return _as_tiers(pd.read_csv(INTERMEDIATE_DIR / "panel.csv"))


def load_camp_full():
    """campaign_table joined with campaign type and start/end week (written by h2_stage1_2)."""
    return pd.read_csv(INTERMEDIATE_DIR / "campaign_households.csv")
