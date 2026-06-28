import pandas as pd
import re

DATA_PATH = "Final_Data_1.xlsx"


def _parse_avg_pkg(s):
    """Extract midpoint from range like '21-25 LPA' → 23.0"""
    if pd.isna(s):
        return None
    nums = re.findall(r"[\d.]+", str(s))
    if len(nums) >= 2:
        return (float(nums[0]) + float(nums[1])) / 2
    elif len(nums) == 1:
        return float(nums[0])
    return None


def _parse_highest_domestic(s):
    """Extract domestic highest pkg in LPA. CR × 100 = LPA."""
    if pd.isna(s):
        return None
    s = str(s)
    m = re.search(r"([\d.]+)\s*CR\s*\(Domestic\)", s, re.IGNORECASE)
    if m:
        return round(float(m.group(1)) * 100, 1)
    # plain LPA fallback
    nums = re.findall(r"[\d.]+", s)
    return float(nums[-1]) if nums else None


def _parse_highest_intl(s):
    """Extract international highest pkg in LPA. CR × 100 = LPA."""
    if pd.isna(s):
        return None
    s = str(s)
    m = re.search(r"([\d.]+)\s*CR\s*\(Intl\)", s, re.IGNORECASE)
    if m:
        return round(float(m.group(1)) * 100, 1)
    return None


def _parse_alumni(s):
    """Extract numeric alumni count from free-text."""
    if pd.isna(s):
        return None
    cleaned = str(s).replace(",", "")
    nums = re.findall(r"\d+", cleaned)
    return int(nums[0]) if nums else None


def _parse_list(s):
    """Split a comma-separated string into a cleaned list."""
    if pd.isna(s):
        return []
    return [x.strip() for x in str(s).split(",") if x.strip()]


def _parse_internship_companies(s):
    """Extract internship company names from 'Yes – Mandatory 6 months | Co1, Co2, Co3'."""
    if pd.isna(s):
        return []
    parts = str(s).split("|")
    if len(parts) > 1:
        return [c.strip() for c in parts[1].split(",") if c.strip()]
    return []


def _assign_tier(category):
    cat = str(category)
    if cat in ["IIT", "Research Institute"]:
        return "Tier 1"
    if cat in ["NIT", "IIIT"]:
        return "Tier 2"
    return "Tier 3"


def _value_grade(roi):
    if pd.isna(roi):
        return "C — Fair"
    if roi > 22:
        return "S — Exceptional"
    if roi > 16:
        return "A — Great"
    if roi > 10:
        return "B — Good"
    return "C — Fair"


def load_data(path: str = DATA_PATH) -> pd.DataFrame:
    df = pd.read_excel(path)

    # Drop fully empty rows
    df = df.dropna(subset=["College Name"]).reset_index(drop=True)

    # ── Parsed numeric columns ──────────────────────────────────────────
    df["Avg Pkg (LPA)"]     = df["Avg Pkg"].apply(_parse_avg_pkg)
    df["Highest Pkg (LPA)"] = df["Highest Pkg"].apply(_parse_highest_domestic)
    df["Intl Pkg (LPA)"]    = df["Highest Pkg"].apply(_parse_highest_intl)
    df["Alumni Count"]      = df["Alumni Network Strength"].apply(_parse_alumni)

    # ── List columns ────────────────────────────────────────────────────
    df["Recruiter List"]       = df["Top Recruiters"].apply(_parse_list)
    df["Recruiter Count"]      = df["Recruiter List"].apply(len)
    df["Partner List"]         = df["Industry Partnerships"].apply(_parse_list)
    df["Partner Count"]        = df["Partner List"].apply(len)
    df["Internship Companies"] = df["Internship Opportunities"].apply(_parse_internship_companies)
    df["Internship Count"]     = df["Internship Companies"].apply(len)

    # ── Derived categorical ─────────────────────────────────────────────
    df["Tier"]       = df["Category"].apply(_assign_tier)
    df["ROI Score"]  = (df["Placement %"] * df["Avg Pkg (LPA)"] / 100).round(2)
    df["Value Grade"] = df["ROI Score"].apply(_value_grade)

    # ── Convenience string columns (for hover labels) ───────────────────
    df["Avg Pkg Range"]     = df["Avg Pkg"].fillna("N/A")
    df["Highest Pkg Range"] = df["Highest Pkg"].fillna("N/A")

    return df
