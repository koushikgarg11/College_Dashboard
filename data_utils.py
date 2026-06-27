import pandas as pd
import re


def load_data():
    df = pd.read_excel("Final_Data_1.xlsx", sheet_name="Colleges_List")
    df = df.dropna(subset=["College Name"])

    # ── Avg Package → numeric (midpoint of range) ─────────────────────────
    def parse_pkg(val):
        if pd.isna(val):
            return None
        val = str(val)
        # Handle range like "21-25 LPA" → midpoint 23
        range_match = re.search(r'(\d+\.?\d*)\s*[-–]\s*(\d+\.?\d*)', val)
        if range_match:
            lo, hi = float(range_match.group(1)), float(range_match.group(2))
            return round((lo + hi) / 2, 1)
        nums = re.findall(r'\d+\.?\d*', val)
        if nums:
            return float(nums[0])
        return None

    df["Avg Pkg (LPA)"] = df["Avg Pkg"].apply(parse_pkg)

    # ── Highest Package → numeric (domestic preferred, CR→LPA) ───────────
    def parse_highest(val):
        if pd.isna(val):
            return None
        val = str(val)
        domestic = re.search(r'(\d+\.?\d*)\s*CR\s*\(Domestic\)', val, re.IGNORECASE)
        if domestic:
            return round(float(domestic.group(1)) * 100, 1)
        lpa = re.findall(r'(\d+\.?\d*)\s*LPA', val, re.IGNORECASE)
        if lpa:
            return float(lpa[-1])
        cr = re.findall(r'(\d+\.?\d*)\s*CR', val, re.IGNORECASE)
        if cr:
            return round(float(cr[-1]) * 100, 1)
        return None

    df["Highest Pkg (LPA)"] = df["Highest Pkg"].apply(parse_highest)

    # ── Tier classification ───────────────────────────────────────────────
    def get_tier(row):
        cat = str(row.get("Category", ""))
        rank = row.get("NIRF Rank", None)
        if cat in ["IIT", "Research Institute"] or (pd.notna(rank) and rank <= 10):
            return "Tier 1"
        elif cat in ["NIT", "IIIT", "Deemed University"] or (pd.notna(rank) and rank <= 50):
            return "Tier 2"
        else:
            return "Tier 3"

    df["Tier"] = df.apply(get_tier, axis=1)

    # ── Alumni count (numeric) ────────────────────────────────────────────
    def alumni_num(v):
        if pd.isna(v):
            return None
        nums = re.findall(r'[\d,]+', str(v))
        if nums:
            return int(nums[0].replace(',', ''))
        return None

    df["Alumni Count"] = df["Alumni Network Strength"].apply(alumni_num)

    # ── Internship companies list ─────────────────────────────────────────
    def intern_cos(v):
        if pd.isna(v):
            return []
        m = re.search(r'\|(.*)', str(v))
        if m:
            return [x.strip() for x in m.group(1).split(',') if x.strip()]
        return []

    df["Internship Companies"] = df["Internship Opportunities"].apply(intern_cos)
    df["Internship Count"] = df["Internship Companies"].apply(len)

    # ── Recruiter & partner lists ─────────────────────────────────────────
    def split_c(v):
        if pd.isna(v):
            return []
        return [x.strip() for x in str(v).split(',') if x.strip()]

    df["Recruiter List"] = df["Top Recruiters"].apply(split_c)
    df["Recruiter Count"] = df["Recruiter List"].apply(len)
    df["Partner List"] = df["Industry Partnerships"].apply(split_c)
    df["Partner Count"] = df["Partner List"].apply(len)

    # ── ROI Score ─────────────────────────────────────────────────────────
    df["ROI Score"] = (df["Placement %"] * df["Avg Pkg (LPA)"] / 100).round(2)

    return df
