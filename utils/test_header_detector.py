import pandas as pd

from header_detector import HeaderDetector


df = pd.DataFrame([
    ["User ID", "204223627", None, None],
    ["As of date", "Nov. 10, 2025", None, None],
    [None, None, None, None],
    ["Note", "This is a portfolio report.", None, None],
    [None, None, None, None],
    ["Allocation date", "Plan", "Instrument type", "Instrument"],
    ["2025-01-01", "TFSA", "Stock", "ABC"],
    ["2025-02-01", "RRSP", "ETF", "XYZ"],
])


detector = HeaderDetector()

header_row = detector.detect(df)

print(f"Detected header row: {header_row}")

if header_row == 5:
    print("Header detection test PASSED.")
else:
    print("Header detection test FAILED.")