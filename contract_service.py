"""
Yapay Zeka Destekli Almanca Öğrenme Projesi
Developer: Betül Altınkaynak Demirel
Document Processing & PDF Export Service
"""

import os
import io
from typing import Dict, Any, Optional

try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None

try:
    import docx
except ImportError:
    docx = None

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable


class ContractService:
    def __init__(self, upload_dir: Optional[str] = None):
        self.upload_dir = upload_dir or os.path.join(os.path.dirname(__file__), "uploads")
        os.makedirs(self.upload_dir, exist_ok=True)

    def extract_text_from_file(self, file_bytes: bytes, filename: str) -> str:
        """PDF veya DOCX dosyasından metin içeriğini çıkarır."""
        ext = os.path.splitext(filename)[1].lower()

        if ext == ".pdf":
            if not fitz:
                raise RuntimeError("PyMuPDF (fitz) kütüphanesi yüklü değil.")
            doc = fitz.open(stream=file_bytes, filetype="pdf")
            text = ""
            for page in doc:
                text += page.get_text() + "\n"
            return text.strip()

        elif ext in [".docx", ".doc"]:
            if not docx:
                raise RuntimeError("python-docx kütüphanesi yüklü değil.")
            file_stream = io.BytesIO(file_bytes)
            doc = docx.Document(file_stream)
            full_text = [para.text for para in doc.paragraphs]
            return "\n".join(full_text).strip()

        elif ext in [".txt", ".md"]:
            return file_bytes.decode("utf-8", errors="ignore").strip()

        else:
            raise ValueError(f"Desteklenmeyen dosya türü: {ext}")

    def generate_pdf_report(
        self,
        title: str,
        content_markdown: str,
        author: str = "Betül Altınkaynak Demirel",
        subtitle: str = "Yapay Zeka Destekli Almanca Öğrenme Raporu"
    ) -> bytes:
        """ReportLab kullanarak profesyonel PDF analiz raporu oluşturur."""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36
        )

        styles = getSampleStyleSheet()
        
        # Özel Stil Tanımlamaları
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=22,
            leading=26,
            textColor=colors.HexColor('#1E293B'),
            alignment=0, # Left
            spaceAfter=6
        )
        
        subtitle_style = ParagraphStyle(
            'CustomSubTitle',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=11,
            leading=14,
            textColor=colors.HexColor('#475569'),
            spaceAfter=15
        )

        heading2_style = ParagraphStyle(
            'CustomH2',
            parent=styles['Heading2'],
            fontName='Helvetica-Bold',
            fontSize=14,
            leading=18,
            textColor=colors.HexColor('#2563EB'),
            spaceBefore=12,
            spaceAfter=6
        )

        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['BodyText'],
            fontName='Helvetica',
            fontSize=10,
            leading=14,
            textColor=colors.HexColor('#334155'),
            spaceAfter=6
        )

        story = []

        # Başlık ve Üst Bilgi
        story.append(Paragraph(title, title_style))
        story.append(Paragraph(f"<b>Geliştirici:</b> {author} | {subtitle}", subtitle_style))
        story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#2563EB'), spaceAfter=15))

        # İçerik İşleme (Satır Satır)
        lines = content_markdown.split('\n')
        for line in lines:
            line_str = line.strip()
            if not line_str:
                story.append(Spacer(1, 4))
                continue

            if line_str.startswith('# '):
                story.append(Paragraph(line_str[2:], title_style))
            elif line_str.startswith('## '):
                story.append(Paragraph(line_str[3:], heading2_style))
            elif line_str.startswith('### '):
                story.append(Paragraph(f"<b>{line_str[4:]}</b>", heading2_style))
            elif line_str.startswith('- ') or line_str.startswith('* '):
                bullet_text = f"• {line_str[2:]}"
                story.append(Paragraph(bullet_text, body_style))
            else:
                story.append(Paragraph(line_str, body_style))

        # Alt Bilgi Notu
        story.append(Spacer(1, 20))
        story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#CBD5E1'), spaceAfter=10))
        footer_text = "Bu rapor Yapay Zeka Destekli Almanca Öğrenme Projesi tarafından otomatik oluşturulmuştur."
        story.append(Paragraph(f"<font color='#94A3B8' size=8>{footer_text}</font>", body_style))

        doc.build(story)
        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes
