# EBYPTABL Sequence Analyzer

A web-based tool to analyze the Error Bypass Table (EBYPTABL.TXT) and find available sequence slots for inserting new entries.

## 📋 Requirements

- Python 3.7 or higher
- Gradio library

## 🚀 Installation

1. Install the required library:
```bash
pip install gradio
```

## 📂 File Structure

```
EBYPTABL/
├── EBYPTABL.TXT           # Your data file (must be present)
├── ebyptabl_analyzer.py   # Main application script
├── CODE_EXPLANATION.md    # Detailed code explanation
└── README.md              # This file
```

## ▶️ How to Run

1. Make sure `EBYPTABL.TXT` is in the same directory as the script

2. Run the script:
```bash
python ebyptabl_analyzer.py
```

3. The application will:
   - Parse the EBYPTABL.TXT file
   - Start a web server on http://127.0.0.1:7860
   - Automatically open in your default browser

## 🎯 How to Use

1. **Enter EDIT Code** (Required): Type the edit code you want to analyze (e.g., E417, F956, E433)

2. **Enter VIP** (Required): Specify the VIP value to filter by (e.g., 256, 413, 858, 999)

3. **Enter FREE_SLOTS** (Required): Specify how many consecutive sequence slots you need

4. **Click Analyze**: The tool will search for available gaps and provide recommendations

## 📊 Output Scenarios

### ✓ Gap Found
Shows two boundary rows where you can insert new entries:
- Row before the gap (with all 6 fields)
- Row after the gap (with all 6 fields)
- Available slot range

### ⚠ No Gap Found
Shows the last row for that EDIT code and recommends coding after it

### ✗ EDIT Not Found
Indicates the EDIT code doesn't exist in the table and suggests starting with SEQ 0001

## 📖 Example Usage

**Example 1: Finding gap for E417 with VIP 999 and 3 slots needed**
```
Input:
- EDIT: E417
- VIP: 999
- FREE_SLOTS: 3

Output:
✓ Sufficient Gap Found
Gap of 97 slots found between SEQ 0002 and 0100
Available slots: 0003 through 0099
```

**Example 2: EDIT not found**
```
Input:
- EDIT: Z999
- VIP: 256
- FREE_SLOTS: 5

Output:
✗ EDIT Not Found
INPUT Z999 not present in the table (with VIP=256)
Recommendation: Start with SEQ 0001
```

## 🔍 How It Works

1. **Parses** EBYPTABL.TXT using fixed-width column positions:
   - SUB PLN: positions 0-2 (3 characters)
   - SVC PLN: positions 4-6 (3 characters)
   - NETWORK ID: positions 8-14 (7 characters)
   - VIP: positions 16-19 (4 characters)
   - SEQ: positions 21-24 (4 characters)
   - EDIT: positions 26-30 (5 characters)

2. **Filters** data to only include rows with SUB_PLN=780 and SVC_PLN=780

3. **Finds** all rows matching the input EDIT code and VIP

4. **Calculates** gaps between consecutive SEQ values using formula:
   ```
   gap = next_seq - current_seq - 1
   ```

5. **Recommends** where to insert new entries based on available gaps

## 🛠️ Troubleshooting

### File Not Found Error
- Ensure `EBYPTABL.TXT` is in the same directory as the script
- Check the file name spelling (case-sensitive on Linux/Mac)

### Port Already in Use
If port 7860 is already in use, modify the last line in `ebyptabl_analyzer.py`:
```python
demo.launch(share=False, server_name="127.0.0.1", server_port=7861)  # Change port
```

### Gradio Not Installed
```bash
pip install gradio
```

## 📝 Notes

- The application runs locally and is not accessible from other computers
- The web interface automatically refreshes when you make changes
- Press `Ctrl+C` in the terminal to stop the server

## 📚 Documentation

For detailed code explanation, see [CODE_EXPLANATION.md](CODE_EXPLANATION.md)

## 🎨 Features

- ✅ User-friendly web interface
- ✅ Real-time analysis
- ✅ Color-coded results (green/orange/red)
- ✅ Example inputs for quick testing
- ✅ Detailed output with all 6 fields
- ✅ Required field validation (EDIT, VIP, FREE_SLOTS)
- ✅ VIP-based filtering for accurate results
- ✅ Input validation and error handling

## 📄 License

This tool is provided as-is for analyzing EBYPTABL files.