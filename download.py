import csv
import io
import re
import zipfile
from pathlib import Path
import requests

URL = "https://www.ssa.gov/oact/babynames/names.zip"
ZIP_FILE = Path("names.zip")
OUTPUT_FILE = Path("ssa-baby-names.csv")

# Minimal headers required by SSA's server
HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "*/*",
    "Accept-Language": "en-US",
}

response = requests.get(URL, headers=HEADERS, timeout=60)
response.raise_for_status()
ZIP_FILE.write_bytes(response.content)

with zipfile.ZipFile(ZIP_FILE) as zf, OUTPUT_FILE.open("w", newline="", encoding="utf-8") as out_f:
    writer = csv.writer(out_f)
    writer.writerow(["year", "name", "sex", "count"])

    for filename in sorted(zf.namelist()):
        match = re.fullmatch(r"yob(\d{4})\.txt", filename)
        if match:
            year = match.group(1)
            with zf.open(filename) as raw_file:
                for row in csv.reader(io.TextIOWrapper(raw_file, encoding="utf-8")):
                    if row:
                        writer.writerow([year, *row])
