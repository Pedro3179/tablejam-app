# TableJam

This is a Python application designed to parse subtitle files (in SRT format) and generate a table that aligns the **transcription** with the **translation**.  

This allows you to to quickly compare the two versions side by side.

---

## Features
- Reads two subtitle files: original and translation.
- Supports multiple encodings (`UTF-8 with BOM`, `UTF-8 without BOM` and `1252 Western Europe` — more to come).
- Validates subtitle structure before processing.
- Exports a clean **CSV file** (`table.csv`) with two columns: Original and Translation.

### Warning

Semicolons will be replaced by commas, otherwise they could break the CSV formatting.

---

## Requirements
- Python 3.7+

No extra installations are required.

---

## How to Run

1. Clone this repository or copy the script.
2. Run the app from the terminal:

   ```bash
   python run.py
3. Enter the original subtitle.
4. Enter the translated subtitle.
6. Open the resulting `table.csv` with *Word* or *Excel*, following the instructions below.

### Word

1. Open `table.csv` on *Microsoft Word*.
2. Select all.
3. Click on *Insert, Table,* then *Convert Text to Table*.
4. Under *Separate text at*, select *Semicolons*.

### Excel

Just open and *voilà*.

---

Special thanks to Luana Selistre who created the art for the icons.