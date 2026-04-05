import gradio as gr
from typing import List

class EBYPTABLAnalyzer:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data = []
        self.parse_file()
    
    def parse_file(self):
        """Parse the EBYPTABL.TXT file and extract the 6 columns using fixed-width positions."""
        print(f"📂 Reading file: {self.file_path}")
        try:
            with open(self.file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            
            print(f"📄 Total lines in file: {len(lines)}")
            total_rows = 0
            filtered_rows = 0
            
            # Skip header lines (first 4 lines)
            for line in lines[4:]:
                if line.strip():
                    # Parse fixed-width columns
                    # Positions: SUB_PLN(0-2), SVC_PLN(4-6), NETWORK_ID(8-14), VIP(16-19), SEQ(21-24), EDIT(26-30)
                    try:
                        sub_pln = line[0:3].strip()
                        svc_pln = line[4:7].strip()
                        network_id = line[8:15].strip()
                        vip = line[16:20].strip()
                        seq = line[21:25].strip()
                        edit = line[26:31].strip()
                        
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
                    except Exception as e:
                        continue  # Skip malformed lines
            
            print(f"✅ Parsing complete!")
            print(f"   Total rows parsed: {total_rows}")
            print(f"   Rows matching SUB_PLN=780 & SVC_PLN=780: {filtered_rows}")
            
        except Exception as e:
            print(f"❌ Error reading file: {str(e)}")
            raise Exception(f"Error reading file: {str(e)}")
    
    def find_edit_rows(self, edit_code: str, vip: str) -> List[dict]:
        """Find all rows matching the EDIT code and VIP."""
        return [row for row in self.data if row['EDIT'] == edit_code and row['VIP'] == vip]
    
    def get_unique_edits(self) -> List[str]:
        """Get list of unique EDIT codes in the data."""
        return sorted(list(set(row['EDIT'] for row in self.data)))
    
    def analyze_gaps(self, edit_code: str, free_slots: int, vip: str) -> str:
        """Analyze gaps for the given EDIT code, FREE_SLOTS requirement, and VIP."""
        
        # Find all rows with matching EDIT and VIP
        matching_rows = self.find_edit_rows(edit_code, vip)
        
        # Case 2: EDIT not found
        if not matching_rows:
            return self.format_not_found(edit_code, free_slots, vip)
        
        # Sort by SEQ
        matching_rows.sort(key=lambda x: int(x['SEQ']))
        
        # Extract SEQ values
        seq_values = [int(row['SEQ']) for row in matching_rows]
        
        # Check for gaps between consecutive SEQ values
        for i in range(len(seq_values) - 1):
            current_seq = seq_values[i]
            next_seq = seq_values[i + 1]
            gap = next_seq - current_seq - 1
            
            if gap >= free_slots:
                # Case 1A: Gap found
                return self.format_gap_found(
                    edit_code,
                    free_slots,
                    matching_rows[i],
                    matching_rows[i + 1],
                    gap,
                    vip
                )
        
        # Case 1B: No sufficient gap found
        return self.format_no_gap(edit_code, free_slots, matching_rows[-1], vip)
    
    def format_gap_found(self, edit_code: str, free_slots: int,
                        row_before: dict, row_after: dict, gap: int, vip: str) -> str:
        """Format output when gap is found."""
        output = f"""<div style='font-family: monospace;'>
<h3 style='color: green;'>✓ Sufficient Gap Found</h3>

<b>Search Parameters:</b><br>
• EDIT: {edit_code}<br>
• VIP: {vip}<br>
• FREE_SLOTS Required: {free_slots}
<br>
<b>Result:</b><br>
Gap of {gap} slots found between SEQ {row_before['SEQ']} and {row_after['SEQ']}

<hr>

<b>New entries can be inserted between these rows:</b>

<div style='background-color: #e8f5e9; padding: 10px; margin: 10px 0; border-left: 4px solid green;'>
<b>Row before gap:</b>
• SUB PLN: {row_before['SUB_PLN']}
• SVC PLN: {row_before['SVC_PLN']}
• NETWORK ID: {row_before['NETWORK_ID'] if row_before['NETWORK_ID'] else '(empty)'}
• VIP: {row_before['VIP']}
• SEQ: {row_before['SEQ']}
• EDIT: {row_before['EDIT']}
</div>

<div style='background-color: #e3f2fd; padding: 10px; margin: 10px 0; border-left: 4px solid blue;'>
<b>Row after gap:</b>
• SUB PLN: {row_after['SUB_PLN']}
• SVC PLN: {row_after['SVC_PLN']}
• NETWORK ID: {row_after['NETWORK_ID'] if row_after['NETWORK_ID'] else '(empty)'}
• VIP: {row_after['VIP']}
• SEQ: {row_after['SEQ']}
• EDIT: {row_after['EDIT']}
</div>

<b>Available slots:</b> {int(row_before['SEQ']) + 1:04d} through {int(row_after['SEQ']) - 1:04d} ({gap} slots available)
</div>"""
        return output
    
    def format_no_gap(self, edit_code: str, free_slots: int, last_row: dict, vip: str) -> str:
        """Format output when no sufficient gap is found."""
        output = f"""<div style='font-family: monospace;'>
<h3 style='color: orange;'>⚠ No Sufficient Gap Found</h3>

<b>Search Parameters:</b><br>
• EDIT: {edit_code}<br>
• VIP: {vip}<br>
• FREE_SLOTS Required: {free_slots}
<br>
<b>Result:</b><br>
No gap between existing entries has {free_slots} or more available slots.

<hr>

<div style='background-color: #fff3e0; padding: 10px; margin: 10px 0; border-left: 4px solid orange;'>
<b>Last row for EDIT {edit_code}:</b>
• SUB PLN: {last_row['SUB_PLN']}
• SVC PLN: {last_row['SVC_PLN']}
• NETWORK ID: {last_row['NETWORK_ID'] if last_row['NETWORK_ID'] else '(empty)'}
• VIP: {last_row['VIP']}
• SEQ: {last_row['SEQ']}
• EDIT: {last_row['EDIT']}
</div>

<b>Recommendation:</b> Code after SEQ {last_row['SEQ']}
</div>"""
        return output
    
    def format_not_found(self, edit_code: str, free_slots: int, vip: str) -> str:
        """Format output when EDIT is not found."""
        unique_edits = self.get_unique_edits()
        edit_list = ', '.join(unique_edits[:20])  # Show first 20
        total_edits = len(unique_edits)
        
        output = f"""<div style='font-family: monospace;'>
<h3 style='color: red;'>✗ EDIT Not Found</h3>

<b>Search Parameters:</b><br>
• EDIT: {edit_code}<br>
• VIP: {vip}<br>
• FREE_SLOTS Required: {free_slots}

<hr>

<div style='background-color: #ffebee; padding: 10px; margin: 10px 0; border-left: 4px solid red;'>
<b>Result:</b><br>
INPUT {edit_code} not present in the table (SUB_PLN=780 & SVC_PLN=780 & VIP={vip} filter applied)
</div>

<b>Recommendation:</b> Start with SEQ 0001

<hr>

<b>Available EDIT codes in filtered data ({total_edits} unique):</b><br>
<small>{edit_list}{'...' if total_edits > 20 else ''}</small>
</div>"""
        return output


def create_gradio_interface():
    """Create and launch the Gradio interface."""
    
    # Initialize analyzer with the file
    try:
        analyzer = EBYPTABLAnalyzer('EBYPTABL.TXT')
        file_status = f"✓ File loaded successfully: {len(analyzer.data)} rows parsed (SUB_PLN=780 & SVC_PLN=780 only)"
    except Exception as e:
        file_status = f"✗ Error loading file: {str(e)}"
        analyzer = None
    
    def analyze_wrapper(edit_code: str, free_slots: int, vip: str):
        """Wrapper function for Gradio interface."""
        if analyzer is None:
            return "<div style='color: red;'>Error: File not loaded. Please ensure EBYPTABL.TXT exists in the current directory.</div>"
        
        if not edit_code or not edit_code.strip():
            return "<div style='color: red;'>Error: Please enter an EDIT code.</div>"
        
        if not vip or not vip.strip():
            return "<div style='color: red;'>Error: VIP is required. Please enter a VIP value.</div>"
        
        if free_slots < 1:
            return "<div style='color: red;'>Error: FREE_SLOTS must be at least 1.</div>"
        
        return analyzer.analyze_gaps(edit_code.strip().upper(), free_slots, vip.strip())
    
    # Create Gradio interface
    with gr.Blocks(title="EBYPTABL Analyzer") as demo:
        gr.Markdown("""
        # 🔍 EBYPTABL Sequence Analyzer
        
        This tool analyzes the Error Bypass Table (EBYPTABL.TXT) to find available sequence slots for inserting new entries.
        
        **Filter:** Only analyzing rows with SUB_PLN = 780 and SVC_PLN = 780
        """)
        
        gr.Markdown(f"**File Status:** {file_status}")
        
        with gr.Row():
            with gr.Column(scale=1):
                edit_input = gr.Textbox(
                    label="EDIT Code *",
                    placeholder="e.g., E417, F956, E433",
                    info="Enter the edit code to search for (Required)",
                    interactive=True
                )
                
                vip_input = gr.Textbox(
                    label="VIP *",
                    placeholder="e.g., 256, 413, 858",
                    info="Enter VIP value (Required)",
                    interactive=True
                )
                
                slots_input = gr.Number(
                    label="FREE_SLOTS *",
                    value=1,
                    minimum=1,
                    precision=0,
                    info="Number of consecutive slots needed (Required)",
                    interactive=True
                )
                
                analyze_btn = gr.Button("🔍 Analyze", variant="primary", size="lg")
            
            with gr.Column(scale=2):
                output = gr.HTML(label="Analysis Result")
        
        # Example inputs
        gr.Markdown("### 📝 Example Inputs")
        gr.Examples(
            examples=[
                ["E998", "256", 1],
                ["E998", "413", 1],
                ["E417", "999", 3],
                ["F956", "256", 5],
            ],
            inputs=[edit_input, vip_input, slots_input],
        )
        
        # Connect button to function
        analyze_btn.click(
            fn=analyze_wrapper,
            inputs=[edit_input, slots_input, vip_input],
            outputs=output
        )
        
        gr.Markdown("""
        ---
        ### 📖 How it works:
        1. **Enter EDIT code**: The edit code you want to analyze (e.g., E417, F956, E998)
        2. **Enter VIP (Required)**: Specify the VIP value to filter by (e.g., 256, 413, 858, 999)
        3. **Enter FREE_SLOTS**: Number of consecutive sequence slots you need
        4. **Click Analyze**: The tool will:
           - Find all rows with matching EDIT code and VIP
           - Calculate gaps between consecutive SEQ values
           - Recommend where to insert new entries
        
        ### 📊 Output Scenarios:
        - **✓ Gap Found**: Shows two boundary rows where you can insert entries
        - **⚠ No Gap Found**: Shows the last row and recommends coding after it
        - **✗ EDIT Not Found**: Indicates the EDIT/VIP combination doesn't exist in the table
        """)
    
    return demo


if __name__ == "__main__":
    demo = create_gradio_interface()
    demo.launch(share=False, server_name="127.0.0.1", server_port=7860)

# Made with Bob
