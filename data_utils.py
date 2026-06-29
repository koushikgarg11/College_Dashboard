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
    """Extract domestic highest package in LPA."""
    if pd.isna(s):
        return None

    s = str(s)

    m = re.search(r"([\d.]+)\s*CR\s*\(Domestic\)", s, re.IGNORECASE)

    if m:
        return round(float(m.group(1)) * 100, 1)

    nums = re.findall(r"[\d.]+", s)

    return float(nums[-1]) if nums else None


def _parse_highest_intl(s):
    """Extract international highest package in LPA."""
    if pd.isna(s):
        return None

    s = str(s)

    m = re.search(r"([\d.]+)\s*CR\s*\(Intl\)", s, re.IGNORECASE)

    if m:
        return round(float(m.group(1)) * 100, 1)

    return None


def _parse_alumni(s):
    """Extract alumni count."""
    if pd.isna(s):
        return None

    cleaned = str(s).replace(",", "")
    nums = re.findall(r"\d+", cleaned)

    return int(nums[0]) if nums else None


def _parse_list(s):
    """Convert comma separated text into list."""
    if pd.isna(s):
        return []

    return [x.strip() for x in str(s).split(",") if x.strip()]


def _parse_internship_companies(s):
    """
    Example:
    Yes – Mandatory 6 months | Google, Microsoft, Amazon
    """

    if pd.isna(s):
        return []

    parts = str(s).split("|")

    if len(parts) > 1:
        return [x.strip() for x in parts[1].split(",") if x.strip()]

    return []


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


def load_data(path=DATA_PATH):

    df = pd.read_excel(path)

    # ----------------------------------------------------
    # Remove empty rows
    # ----------------------------------------------------
    df = df.dropna(subset=["College Name"]).reset_index(drop=True)

    # ----------------------------------------------------
    # Numeric Columns
    # ----------------------------------------------------
    df["Avg Pkg (LPA)"] = df["Avg Pkg"].apply(_parse_avg_pkg)

    df["Highest Pkg (LPA)"] = df["Highest Pkg"].apply(
        _parse_highest_domestic
    )

    df["Intl Pkg (LPA)"] = df["Highest Pkg"].apply(
        _parse_highest_intl
    )

    df["Alumni Count"] = df["Alumni Network Strength"].apply(
        _parse_alumni
    )

    # ----------------------------------------------------
    # Recruiters
    # ----------------------------------------------------
    df["Recruiter List"] = df["Top Recruiters"].apply(_parse_list)

    df["Recruiter Count"] = df["Recruiter List"].apply(len)

    # ----------------------------------------------------
    # Industry Partners
    # ----------------------------------------------------
    df["Partner List"] = df["Industry Partnerships"].apply(_parse_list)

    df["Partner Count"] = df["Partner List"].apply(len)

    # ----------------------------------------------------
    # Internship Companies
    # ----------------------------------------------------
    df["Internship Companies"] = df[
        "Internship Opportunities"
    ].apply(_parse_internship_companies)

    df["Internship Count"] = df["Internship Companies"].apply(len)

    # ====================================================
    # IMPORTANT
    # Entire dataset contains only Tier 1 colleges
    # ====================================================

    df["Tier"] = "Tier 1"

    # ----------------------------------------------------
    # ROI
    # ----------------------------------------------------
    df["ROI Score"] = (
        df["Placement %"] * df["Avg Pkg (LPA)"] / 100
    ).round(2)

    df["Value Grade"] = df["ROI Score"].apply(_value_grade)

    # ----------------------------------------------------
    # Hover Labels
    # ----------------------------------------------------
    df["Avg Pkg Range"] = df["Avg Pkg"].fillna("N/A")

    df["Highest Pkg Range"] = df["Highest Pkg"].fillna("N/A")

    return df
