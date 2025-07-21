# ===== File: generate_excel_summary.py =====

import json
import os
import pandas as pd
import re
from collections import Counter
from extract_trade_data import extract_trades, expected_columns, segment_mappings

# Update paths accordingly
json_path = "/Users/er.vishalmishra/Documents/Hindu-Jeevan-Backend/zer/analyzeDocResponse.json"
output_excel = "/Users/er.vishalmishra/Documents/Hindu-Jeevan-Backend/zer/Extracted_Tables.xlsx"
segment_order = ["Equity", "Mutual Funds", "Futures&Options", "Equity (External)", "MF(External)"]
segment_reverse = {v.lower(): k for k, v in segment_mappings.items()}

# Extract trades
with open(json_path, "r", encoding="utf-8") as f:
    textract_data = json.load(f)

trade_data = extract_trades(textract_data)
df_trades = pd.DataFrame(trade_data, columns=expected_columns)

# Enhanced Demat extraction with line-based logic
demat_number = "NA"
date_range = "NA"
ui_noise_words = ["dashboard", "portfolio", "reports", "funds", "account"]

lines = [b for b in textract_data.get("Blocks", []) if b.get("BlockType") == "LINE"]
for line in lines:
    text = line.get("Text", "").lower()
    if any(word in text for word in ui_noise_words):
        match = re.search(r"\b[A-Za-z0-9]{6}\b", text)
        if match:
            demat_number = match.group(0)
            break

# Fallback to global Demat search
if demat_number == "NA":
    for block in textract_data.get("Blocks", []):
        txt = block.get("Text", "")
        if re.search(r"\b[A-Za-z0-9]{6}\b", txt):
            demat_number = re.search(r"\b[A-Za-z0-9]{6}\b", txt).group(0)
            break

# Date Range extraction
for block in textract_data.get("Blocks", []):
    txt = block.get("Text", "")
    if re.search(r"(\d{4}-\d{2}-\d{2}[-\s]+\d{4}-\d{2}-\d{2})", txt):
        date_range = re.search(r"(\d{4}-\d{2}-\d{2}[-\s]+\d{4}-\d{2}-\d{2})", txt).group(1)
        break

# Count trades per segment
trade_counts = Counter(df_trades["Segment"].str.strip())

summary_row = {
    "Demat Number": demat_number,
    "Date Range": date_range
}
for seg in segment_order:
    summary_row[seg] = trade_counts.get(seg, "NA" if seg not in df_trades["Segment"].unique() else 0)

df_summary = pd.DataFrame([summary_row])

# Detect Missing Segments
present_segments = set(df_trades["Segment"].str.strip())
missing_segments = [seg for seg in segment_order if seg not in present_segments]
df_missing = pd.DataFrame([[demat_number, date_range, seg] for seg in missing_segments], columns=["Demat Number", "Date Range", "Segment"])

# Empty Segments (0 trades counted but segment declared)
empty_segments = [seg for seg in present_segments if trade_counts.get(seg, 0) == 0]
df_empty = pd.DataFrame([[demat_number, date_range, seg] for seg in empty_segments], columns=["Demat Number", "Date Range", "Segment"])

# Write to Excel
with pd.ExcelWriter(output_excel) as writer:
    df_summary.to_excel(writer, sheet_name="Summary", index=False)
    df_missing.to_excel(writer, sheet_name="Missing Segments", index=False)
    df_empty.to_excel(writer, sheet_name="Empty Segments", index=False)
    df_trades.to_excel(writer, sheet_name="Trade Details", index=False)

print(f"✅ Excel Report Generated: {output_excel}")