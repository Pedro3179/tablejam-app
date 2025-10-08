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
2. **Attention:** Make sure original and translation files have the same number of subtitles. Translating your source material in *Translator Mode* (that is, side by side) is advised. 
3. Run the script from the command prompt:

   ```bash
   python tablejam_app.py
4. Open table.csv on *Microsoft Word*.
5. Select all.
6. Click on *Insert, Table,* then *Convert Text to Table*.
7. Under *Separate text at*, select *Semicolons*.

### Excel

Just open and *voilà*.

---

## Future Improvements

- Work with different number of subtitles in the transcription and translation.
- Enumerate the lines in the table.
- Improve usability by allowing users to place transcription and translation files in dedicated directories instead of entering filenames manually.