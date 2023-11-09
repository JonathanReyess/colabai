import pandas as pd
from fpdf import FPDF

# Load CSV data
csv_file_path = 'colab copilot/data/all_modules.csv'
df = pd.read_csv(csv_file_path)

# Create PDF with UTF-8 encoding
pdf = FPDF()
pdf.add_page()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.set_font("Arial", size=12)

# Add data to PDF
for index, row in df.iterrows():
    # Encode each row to UTF-8 to handle non-Latin-1 characters
    pdf.cell(200, 10, txt=row.to_string().encode('latin-1', 'replace').decode('latin-1'), ln=True)

# Save PDF
pdf_output_path = 'colab copilot/data/all_modules.pdf'
pdf.output(pdf_output_path)
