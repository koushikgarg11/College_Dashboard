import pandas as pd
import re

def load_data():
    df = pd.read_excel("Final_Data_1.xlsx", sheet_name="Colleges_List")
    df = df.dropna(subset=["College Name"]).copy()

    # ── Parse Avg Pkg: take midpoint of range like "21-25 LPA" ──
    def parse_avg_pkg(val):
        if pd.isna(val): return None
        nums = re.findall(r'\d+\.?\d*', str(val))
        if len(nums) >= 2:
            return (float(nums[0]) + float(nums[1])) / 2
        elif len(nums) == 1:
            return float(nums[0])
        return None

    # ── Parse Highest Pkg: prefer Domestic CR value, else LPA ──
    def parse_highest_pkg(val):
        if pd.isna(val): return None
        val = str(val)
        # Domestic CR: e.g. "1.68 CR(Domestic)" → 168 LPA
        dom = re.search(r'([\d.]+)\s*CR\(Domestic\)', val)
        if dom:
            return round(float(dom.group(1)) * 100, 1)
        # International CR: e.g. "3.5 CR(Intl)" → 350 LPA
        intl = re.search(r'([\d.]+)\s*CR\(Intl\)', val)
        if intl:
            return round(float(intl.group(1)) * 100, 1)
        # Plain LPA: e.g. "90 LPA"
        lpa = re.search(r'([\d.]+)\s*LPA', val, re.IGNORECASE)
        if lpa:
            return float(lpa.group(1))
        # Plain number
        nums = re.findall(r'[\d.]+', val)
        if nums: return float(nums[0])
        return None

    # ── Parse Highest Pkg International ──
    def parse_intl_pkg(val):
        if pd.isna(val): return None
        val = str(val)
        intl = re.search(r'([\d.]+)\s*CR\(Intl\)', val)
        if intl:
            return round(float(intl.group(1)) * 100, 1)
        return None

    df["Avg Pkg (LPA)"]      = df["Avg Pkg"].apply(parse_avg_pkg)
    df["Highest Pkg (LPA)"]  = df["Highest Pkg"].apply(parse_highest_pkg)
    df["Intl Pkg (LPA)"]     = df["Highest Pkg"].apply(parse_intl_pkg)

    # ── Parse Alumni Count ──
    def parse_alumni(val):
        if pd.isna(val): return None
        nums = re.findall(r'[\d,]+', str(val))
        if nums:
            return int(nums[0].replace(',', ''))
        return None
    df["Alumni Count"] = df["Alumni Network Strength"].apply(parse_alumni)

    # ── Parse Internship companies ──
    def parse_intern(val):
        if pd.isna(val): return []
        m = re.search(r'\|(.*)', str(val))
        if m: return [x.strip() for x in m.group(1).split(',') if x.strip()]
        return []
    df["Internship Companies"] = df["Internship Opportunities"].apply(parse_intern)
    df["Internship Count"]     = df["Internship Companies"].apply(len)

    # ── Parse Recruiter & Partner lists ──
    def split_list(val):
        if pd.isna(val): return []
        return [x.strip() for x in str(val).split(',') if x.strip()]
    df["Recruiter List"]  = df["Top Recruiters"].apply(split_list)
    df["Recruiter Count"] = df["Recruiter List"].apply(len)
    df["Partner List"]    = df["Industry Partnerships"].apply(split_list)
    df["Partner Count"]   = df["Partner List"].apply(len)

    # ── Tier Classification (based on actual category) ──
    tier_map = {
        "IIT": "Tier 1",
        "Research Institute": "Tier 1",   # IISc
        "IIIT": "Tier 2",
        "NIT": "Tier 2",
        "Deemed University": "Tier 2",
        "State University": "Tier 3",
        "Engineering College": "Tier 3",
        "University": "Tier 3",
    }
    df["Tier"] = df["Category"].map(tier_map).fillna("Tier 3")

    # ── Avg Pkg range label (keep original for display) ──
    df["Avg Pkg Range"] = df["Avg Pkg"].fillna("N/A")

    # ── ROI Score ──
    df["ROI Score"] = (df["Placement %"] * df["Avg Pkg (LPA)"] / 100).round(2)

    # ── Value Grade ──
    def grade(score):
        if pd.isna(score): return "N/A"
        if score >= 22: return "S — Exceptional"
        if score >= 16: return "A — Great"
        if score >= 10: return "B — Good"
        return "C — Fair"
    df["Value Grade"] = df["ROI Score"].apply(grade)

    return df
