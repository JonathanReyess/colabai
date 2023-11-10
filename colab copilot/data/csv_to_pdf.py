import pandas as pd
from fpdf import FPDF

csv_file_path = 'colab copilot/data/all_modules.csv'
df = pd.read_csv(csv_file_path)

pdf = FPDF()
pdf.add_page()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.set_font("Arial", size=12)

for index, row in df.iterrows():
    pdf.cell(200, 10, txt=row.to_string().encode('latin-1', 'replace').decode('latin-1'), ln=True)

pdf_output_path = 'colab copilot/data/all_modules.pdf'
pdf.output(pdf_output_path)
