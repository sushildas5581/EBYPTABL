# EBYPTABL Analyzer - Complete Code Explanation

## Overview
This Python script creates a web application using Gradio to analyze the EBYPTABL.TXT file and find available sequence slots for inserting new entries with a specific EDIT code.

---

## Part 1: Imports (Lines 1-2)

```python
import gradio as gr
from typing import List
```

- **gradio**: Library to create web UI with input fields, buttons, and output display
- **typing.List**: Provides type hints to indicate a function returns a list

---

## Part 2: EBYPTABLAnalyzer Class

### 2.1 Constructor - `__init__` (Lines 4-8)

```python
def __init__(self, file_path: str):
    self.file_path = file_path
    self.data = []
    self.parse_file()
```

**Purpose**: Initialize the analyzer object  
**Usage**: `analyzer = EBYPTABLAnalyzer('EBYPTABL.TXT')`  
**What happens**:
1. Stores file path
2. Creates empty list for data
3. Calls parse_file() to read the file

---

### 2.2 File Parser - `parse_file` (Lines 10-42)

#### Step 1: Open and Read File
```python
with open(self.file_path, 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()
```
- Opens file in read mode
- `encoding='utf-8'`: Handles special characters
- `errors='ignore'`: Skips problematic characters
- `readlines()`: Reads all lines into a list

#### Step 2: Skip Header Lines
```python
for line in lines[4:]:
```
- Skips first 4 header lines
- Processes only data rows (starting from line 5)

#### Step 3: Extract Columns (Fixed-Width Format)
```python
sub_pln = line[0:3].strip()      # SUB PLN: positions 0-2 (3 chars)
svc_pln = line[4:7].strip()      # SVC PLN: positions 4-6 (3 chars)
network_id = line[8:15].strip()  # NETWORK ID: positions 8-14 (7 chars)
vip = line[16:20].strip()        # VIP: positions 16-19 (4 chars)
seq = line[21:25].strip()        # SEQ: positions 21-24 (4 chars)
edit = line[26:31].strip()       # EDIT: positions 26-30 (5 chars)
```

**Visual Example:**
```
Position: 0  3 4  7 8      15 16  20 21   25 26   31
Line:     580 580         999  0001 E417
          ^^^-^^^-------^^^^^--^^^^-^^^^^
          SUB SVC NETWORK VIP  SEQ  EDIT
```

**Key Points:**
- `line[0:3]`: Extracts characters at positions 0, 1, 2 (3 is exclusive)
- `line[16:20]`: Extracts VIP (4 characters: positions 16-19)
- `line[26:31]`: Extracts EDIT (5 characters: positions 26-30)
- `.strip()`: Removes leading/trailing spaces

#### Step 4: Filter and Store Valid Rows
```python
if sub_pln and seq and edit:  # Valid row
    total_rows += 1
    # Filter: Only include rows with SUB_PLN = 780 and SVC_PLN = 780
    if sub_pln == '780' and svc_pln == '780':
        self.data.append({
            'SUB_PLN': sub_pln,
            'SVC_PLN': svc_pln,
            'NETWORK_ID': network_id if network_id else '',
            'VIP': vip,
            'SEQ': seq,
            'EDIT': edit
        })
        filtered_rows += 1
```

**Result**: `self.data` becomes a list of dictionaries:
```python
[
    {'SUB_PLN': '580', 'SVC_PLN': '580', 'NETWORK_ID': '', 'VIP': '999', 'SEQ': '0001', 'EDIT': 'E417'},
    {'SUB_PLN': '580', 'SVC_PLN': '580', 'NETWORK_ID': '', 'VIP': '999', 'SEQ': '0002', 'EDIT': 'E417'},
    ...
]
```

---

### 2.3 Find Matching Rows - `find_edit_rows` (Lines 44-46)

```python
def find_edit_rows(self, edit_code: str) -> List[dict]:
    return [row for row in self.data if row['EDIT'] == edit_code]
```

**Purpose**: Filter rows by EDIT code  
**Input**: `"E417"`  
**Output**: All rows where EDIT column equals "E417"  
**Method**: List comprehension (compact for loop)

---

### 2.4 Main Analysis - `analyze_gaps` (Lines 66-100)

```python
def analyze_gaps(self, edit_code: str, free_slots: int, vip: str) -> str:
```

**Purpose**: Find gaps between consecutive sequences for a specific EDIT code and VIP

#### Step 1: Find Matching Rows
```python
matching_rows = self.find_edit_rows(edit_code, vip)
```

#### Step 2: Handle EDIT Not Found (Case 2)
```python
if not matching_rows:
    return self.format_not_found(edit_code, free_slots)
```
If no rows match, return "not found" message

#### Step 3: Sort by Sequence Number
```python
matching_rows.sort(key=lambda x: int(x['SEQ']))
```
- `lambda x: int(x['SEQ'])`: Converts SEQ string to integer for sorting
- Example: ['0100', '0001', '0005'] → ['0001', '0005', '0100']

#### Step 4: Extract Sequence Values
```python
seq_values = [int(row['SEQ']) for row in matching_rows]
```
- Converts: ['0001', '0005', '0100'] → [1, 5, 100]

#### Step 5: Check Gaps Between Consecutive Sequences
```python
for i in range(len(seq_values) - 1):
    current_seq = seq_values[i]
    next_seq = seq_values[i + 1]
    gap = next_seq - current_seq - 1
```

**Example Walkthrough:**
- seq_values = [1, 5, 100]
- **Iteration 1**: i=0
  - current_seq = 1, next_seq = 5
  - gap = 5 - 1 - 1 = **3** (available slots: 2, 3, 4)
- **Iteration 2**: i=1
  - current_seq = 5, next_seq = 100
  - gap = 100 - 5 - 1 = **94** (available slots: 6, 7, ..., 99)

#### Step 6: Check if Gap is Sufficient (Case 1A)
```python
if gap >= free_slots:
    return self.format_gap_found(...)
```
If gap is big enough, return the two boundary rows

#### Step 7: No Sufficient Gap (Case 1B)
```python
return self.format_no_gap(edit_code, free_slots, matching_rows[-1])
```
- `matching_rows[-1]`: Gets the last row
- Returns recommendation to code after last sequence

---

## Part 3: Formatting Methods

### 3.1 Gap Found - `format_gap_found` (Lines 102-142)

**Purpose**: Creates HTML output when gap is found

**Structure**:
- Green header with checkmark (✓)
- Search parameters (EDIT, VIP, FREE_SLOTS)
- Result with gap information
- Two colored boxes:
  - Green: Row before gap
  - Blue: Row after gap
- Available slots calculation

**Example Output**:
```
✓ Sufficient Gap Found
Search Parameters:
• EDIT: E417
• VIP: 999
• FREE_SLOTS Required: 3

Result:
Gap of 94 slots found between SEQ 0005 and 0100

Row before gap: SUB PLN: 780, ..., SEQ: 0005
Row after gap: SUB PLN: 780, ..., SEQ: 0100
Available slots: 0006 through 0099 (94 slots)
```

---

### 3.2 No Gap Found - `format_no_gap` (Lines 144-171)

**Purpose**: Creates HTML output when no sufficient gap found

**Structure**:
- Orange header with warning (⚠)
- Search parameters (EDIT, VIP, FREE_SLOTS)
- Result message
- Shows only the last row for that EDIT/VIP combination
- Recommendation to code after last SEQ

---

### 3.3 EDIT Not Found - `format_not_found` (Lines 173-201)

**Purpose**: Creates HTML output when EDIT/VIP combination doesn't exist

**Structure**:
- Red header with X (✗)
- Search parameters (EDIT, VIP, FREE_SLOTS)
- Message: "INPUT {EDIT} not present in the table (with VIP={vip})"
- Recommendation to start with SEQ 0001
- List of available EDIT codes in the filtered data

---

## Part 4: Gradio Interface - `create_gradio_interface` (Lines 204-306)

### Step 1: Initialize Analyzer
```python
try:
    analyzer = EBYPTABLAnalyzer('EBYPTABL.TXT')
    file_status = f"✓ File loaded successfully: {len(analyzer.data)} rows parsed"
except Exception as e:
    file_status = f"✗ Error loading file: {str(e)}"
    analyzer = None
```
- Tries to load and parse EBYPTABL.TXT
- Shows success message with row count
- If error, shows error message

### Step 2: Wrapper Function
```python
def analyze_wrapper(edit_code: str, free_slots: int, vip: str):
```

**Validation checks**:
1. File loaded? If not, show error
2. EDIT code entered? If not, show error
3. VIP entered? If not, show error
4. FREE_SLOTS >= 1? If not, show error
5. If all valid, call `analyzer.analyze_gaps(edit_code, free_slots, vip)`

### Step 3: Create UI Layout
```python
with gr.Blocks(title="EBYPTABL Analyzer", theme=gr.themes.Soft()) as demo:
```
- `gr.Blocks`: Container for custom layouts
- `theme=gr.themes.Soft()`: Applies soft color theme

### Step 4: Add Title and Status
```python
gr.Markdown("""# 🔍 EBYPTABL Sequence Analyzer""")
gr.Markdown(f"**File Status:** {file_status}")
```

### Step 5: Create Layout (Row and Columns)
```python
with gr.Row():
    with gr.Column(scale=1):  # Left column (inputs)
        edit_input = gr.Textbox(...)
        slots_input = gr.Number(...)
        analyze_btn = gr.Button(...)
    
    with gr.Column(scale=2):  # Right column (output, wider)
        output = gr.HTML(...)
```
- `gr.Row()`: Horizontal layout
- `gr.Column(scale=1)`: Takes 1/3 of width
- `gr.Column(scale=2)`: Takes 2/3 of width

### Step 6: Input Components (All Required Fields)

**EDIT Code Input (Required):**
```python
edit_input = gr.Textbox(
    label="EDIT Code *",
    placeholder="e.g., E417, F956, E433",
    info="Enter the edit code to search for (Required)",
    interactive=True
)
```

**VIP Input (Required):**
```python
vip_input = gr.Textbox(
    label="VIP *",
    placeholder="e.g., 256, 413, 858",
    info="Enter VIP value (Required)",
    interactive=True
)
```

**FREE_SLOTS Input (Required):**
```python
slots_input = gr.Number(
    label="FREE_SLOTS *",
    value=1,
    minimum=1,
    precision=0,
    info="Number of consecutive slots needed (Required)",
    interactive=True
)
```
- `value=1`: Default value
- `minimum=1`: Can't be less than 1
- `precision=0`: Only integers
- Asterisk (*) in label indicates required field

### Step 7: Button
```python
analyze_btn = gr.Button("🔍 Analyze", variant="primary", size="lg")
```
- `variant="primary"`: Blue color
- `size="lg"`: Large size

### Step 8: Output Area
```python
output = gr.HTML(label="Analysis Result")
```
Displays HTML formatted results

### Step 9: Example Inputs
```python
gr.Examples(
    examples=[
        ["E998", "256", 1],
        ["E998", "413", 1],
        ["E417", "999", 3],
        ["F956", "256", 5],
    ],
    inputs=[edit_input, vip_input, slots_input],
)
```
Pre-filled examples users can click (now includes VIP values)

### Step 10: Connect Button to Function
```python
analyze_btn.click(
    fn=analyze_wrapper,
    inputs=[edit_input, slots_input, vip_input],
    outputs=output
)
```
- When button clicked, calls `analyze_wrapper`
- Passes values from all three input fields (EDIT, FREE_SLOTS, VIP)
- Displays result in output area

---

## Part 5: Main Execution (Lines 309-313)

```python
if __name__ == "__main__":
    demo = create_gradio_interface()
    demo.launch(share=False, server_name="127.0.0.1", server_port=7860)
```

**What happens**:
1. `if __name__ == "__main__"`: Only runs if script executed directly
2. `create_gradio_interface()`: Creates the UI
3. `demo.launch()`: Starts web server
   - `share=False`: Only accessible locally
   - `server_name="127.0.0.1"`: Localhost only
   - `server_port=7860`: Port 7860
4. Opens browser to http://127.0.0.1:7860

---

## Complete Flow Example

**User Action**: Enters "E417", "999", and "3", clicks Analyze

**What Happens**:
1. Button click triggers `analyze_wrapper("E417", 3, "999")`
2. Validates inputs:
   - EDIT code present? ✓
   - VIP present? ✓
   - FREE_SLOTS >= 1? ✓
3. Calls `analyzer.analyze_gaps("E417", 3, "999")`
4. Finds all rows with EDIT="E417" AND VIP="999"
5. Sorts by SEQ: [1, 2, 100, 105]
6. Checks gaps:
   - Gap between 1 and 2: 0 (not enough)
   - Gap between 2 and 100: 97 (sufficient! ✓)
7. Returns `format_gap_found()` with rows 2 and 100
8. Displays HTML result in output area

---

## Key Algorithm: Gap Calculation

**Formula**: `gap = next_seq - current_seq - 1`

**Why subtract 1?**
- Between SEQ 0001 and 0005:
  - Available slots: 0002, 0003, 0004
  - That's 3 slots
  - Calculation: 5 - 1 - 1 = 3 ✓

**Example**:
- SEQ values: [1, 5, 100]
- Gap 1: 5 - 1 - 1 = 3 slots (2, 3, 4)
- Gap 2: 100 - 5 - 1 = 94 slots (6, 7, ..., 99)

---

## Summary

The script:
1. **Parses** EBYPTABL.TXT using fixed-width column positions
2. **Filters** data to only SUB_PLN=780 and SVC_PLN=780 rows
3. **Finds** all rows matching input EDIT code AND VIP value
4. **Calculates** gaps between consecutive SEQ values
5. **Recommends** where to insert new entries
6. **Displays** results in a user-friendly web interface with required field validation

**Column Positions (Fixed-Width Format)**:
- SUB PLN: 0-2 (3 characters)
- SVC PLN: 4-6 (3 characters)
- NETWORK ID: 8-14 (7 characters)
- VIP: 16-19 (4 characters)
- SEQ: 21-24 (4 characters)
- EDIT: 26-30 (5 characters)

**Important Notes**:
- File uses fixed-width format, not tab-delimited
- First 4 lines are headers and must be skipped
- Data filtering: Only SUB_PLN=780 and SVC_PLN=780 rows are analyzed
- **All three fields are required**: EDIT Code, VIP, and FREE_SLOTS
- VIP field is mandatory for accurate matching and filtering
- Asterisks (*) in field labels indicate required fields