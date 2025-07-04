from fpdf import FPDF
import os

def export_pdf(text: str, output_path: str = "investment_report.pdf"):
    pdf = FPDF()
    pdf.add_page()

    font_path = os.path.join("fonts", "NanumGothic.ttf")
    if not os.path.exists(font_path):
        raise RuntimeError(f"TTF Font file not found: {font_path}")

    pdf.add_font('Nanum', '', font_path, uni=True)  # ✅ 꼭 유니코드 설정
    pdf.set_font("Nanum", size=12)

    for line in text.split('\n'):
        pdf.multi_cell(0, 10, line)

    pdf.output(output_path)
