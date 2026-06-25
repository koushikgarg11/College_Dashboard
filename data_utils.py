import pandas as pd
import re

def load_data():
    df = pd.read_excel("Final_Data_1.xlsx", sheet_name="Colleges_List")
    df = df.dropna(subset=["College Name"])
    
    # Parse avg package to numeric (take lower bound)
    def parse_pkg(val):
        if pd.isna(val):
            return None
        val = str(val)
        nums = re.findall(r'\d+\.?\d*', val)
        if nums:
            return float(nums[0])
        return None

    df["Avg Pkg (LPA)"] = df["Avg Pkg"].apply(parse_pkg)
    
    # Parse highest package (domestic preferred)
    def parse_highest(val):
        if pd.isna(val):
            return None
        val = str(val)
        # Check for Domestic value first (e.g. "1 CR(Domestic)")
        domestic = re.search(r'(\d+\.?\d*)\s*CR\(Domestic\)', val)
        if domestic:
            return float(domestic.group(1)) * 100
        lpa = re.findall(r'(\d+\.?\d*)\s*LPA', val, re.IGNORECASE)
        if lpa:
            return float(lpa[-1])
        cr = re.findall(r'(\d+\.?\d*)\s*CR', val, re.IGNORECASE)
        if cr:
            return float(cr[-1]) * 100
        return None

    df["Highest Pkg (LPA)"] = df["Highest Pkg"].apply(parse_highest)
    
    # Tier classification
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
    
    # ROI Score (placement * avg_pkg / 100 as proxy)
    df["ROI Score"] = (df["Placement %"] * df["Avg Pkg (LPA)"] / 100).round(2)
    
    return df
