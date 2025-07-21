import json
import pandas as pd
import re
from difflib import SequenceMatcher

# Update these paths as needed
json_path = "/Users/er.vishalmishra/Documents/Hindu-Jeevan-Backend/zer/analyzeDocResponse.json"
output_excel = "/Users/er.vishalmishra/Documents/Hindu-Jeevan-Backend/zer/Extracted_Tables.xlsx"
expected_columns = ["Symbol", "Trade time", "Order ID", "Trade ID", "Type", "Qty.", "Price", "Segment"]

segment_mappings = {
    "equity": "Equity",
    "mutual funds": "Mutual Funds",
    "mf external": "MF(External)",
    "equity external": "Equity (External)",
    "futures options": "Futures&Options",
    "futures & options": "Futures&Options",
    "futures": "Futures&Options",
    "f&o": "Futures&Options"
}

ignore_keywords = ["holdings", "positions"]

def fuzzy_match(text, targets, threshold=0.6):
    text = re.sub(r'\W+', '', text.lower())
    for key, label in targets.items():
        key_clean = re.sub(r'\W+', '', key.lower())
        if SequenceMatcher(None, text, key_clean).ratio() >= threshold:
            return label
    return None

with open(json_path, "r", encoding="utf-8") as f:
    textract_data = json.load(f)

blocks = textract_data["Blocks"]
block_map = {block["Id"]: block for block in blocks}

pages = {}
lines_by_page = {}
tables_by_page = {}
ignored_pages = set()

# First Pass: Collect PAGE, LINE, TABLE info
for block in blocks:
    if block["BlockType"] == "PAGE":
        pages[block["Id"]] = block
        lines_by_page[block["Id"]] = []
        tables_by_page[block["Id"]] = []

for block in blocks:
    if block["BlockType"] == "LINE":
        for page_id in pages:
            page_top = pages[page_id]["Geometry"]["BoundingBox"]["Top"]
            page_bottom = page_top + pages[page_id]["Geometry"]["BoundingBox"]["Height"]
            line_top = block["Geometry"]["BoundingBox"]["Top"]

            if page_top <= line_top <= page_bottom:
                lines_by_page[page_id].append(block)

    if block["BlockType"] == "TABLE":
        for page_id in pages:
            page_top = pages[page_id]["Geometry"]["BoundingBox"]["Top"]
            page_bottom = page_top + pages[page_id]["Geometry"]["BoundingBox"]["Height"]
            table_top = block["Geometry"]["BoundingBox"]["Top"]

            if page_top <= table_top <= page_bottom:
                tables_by_page[page_id].append(block)

# Detect Ignored Pages
for page_id, lines in lines_by_page.items():
    full_text = " ".join(line.get("Text", "") for line in lines).lower()
    if any(kw in full_text for kw in ignore_keywords):
        ignored_pages.add(page_id)

clean_data = []

for page_id, tables in tables_by_page.items():
    if page_id in ignored_pages:
        continue

    lines = lines_by_page[page_id]
    persistent_segment = ""

    # Detect last known segment in lines (anywhere on page)
    for line in lines:
        label = fuzzy_match(line.get("Text", ""), segment_mappings)
        if label:
            persistent_segment = label

    for table in tables:
        table_top = table["Geometry"]["BoundingBox"]["Top"]
        detected_segment = ""

        # Search lines spatially above table for nearest segment
        for line in lines:
            line_bottom = line["Geometry"]["BoundingBox"]["Top"] + line["Geometry"]["BoundingBox"]["Height"]
            if line_bottom < table_top:
                label = fuzzy_match(line.get("Text", ""), segment_mappings)
                if label:
                    detected_segment = label

        # Fallback to page-wide persistent segment
        if not detected_segment:
            detected_segment = persistent_segment

        # Extract Table Data
        cells = []
        for rel in table.get("Relationships", []):
            if rel["Type"] == "CHILD":
                for cell_id in rel["Ids"]:
                    cell = block_map[cell_id]
                    if cell["BlockType"] == "CELL":
                        row = cell["RowIndex"]
                        col = cell["ColumnIndex"]
                        text = ""
                        for child_rel in cell.get("Relationships", []):
                            if child_rel["Type"] == "CHILD":
                                for word_id in child_rel["Ids"]:
                                    word = block_map[word_id]
                                    if word["BlockType"] == "WORD":
                                        text += word["Text"] + " "
                        cells.append({"row": row, "col": col, "text": text.strip()})

        data_dict = {}
        for cell in cells:
            row = cell["row"]
            col = cell["col"]
            text = cell["text"]
            if row not in data_dict:
                data_dict[row] = {}
            data_dict[row][col] = text

        for row_idx in sorted(data_dict.keys()):
            row = data_dict[row_idx]

            symbol = row.get(1, "").strip()
            exch = row.get(2, "").strip()
            tradetime = row.get(3, "").strip()
            orderid = row.get(4, "").strip()
            tradeid = row.get(5, "").strip()
            tradetype = row.get(6, "").strip()
            qty = row.get(7, "").strip()
            price = row.get(8, "").strip()

            combined = f"{symbol} {exch} {tradetime} {orderid}".lower()
            if "showing page" in combined or "last updated" in combined or symbol.lower() == "symbol":
                continue

            full_symbol = f"{symbol} {exch}".strip()

            if not qty and price:
                parts = price.split()
                if len(parts) == 2:
                    qty, price = parts[0], parts[1]

            type_clean = "BUY" if "buy" in tradetype.lower() else "SELL" if "sell" in tradetype.lower() else tradetype.upper()

            clean_data.append([
                full_symbol, tradetime, orderid, tradeid, type_clean, qty, price, detected_segment
            ])

# Build DataFrame
df = pd.DataFrame(clean_data, columns=expected_columns)
df.to_excel(output_excel, index=False)

print(f"✅ Stable report with geometry-driven segment detection saved to {output_excel}")