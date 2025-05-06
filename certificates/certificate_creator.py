from docx import Document
import pandas as pd
from datetime import datetime
from docx2pdf import convert
import locale
from pathlib import Path
from project.utils import paths

TEMPLATE_DIR = paths.CERTIFICATES_DIR / 'templates' / 'brigada_de_incendio.docx'  
locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

class Certificate:
    def __init__(self, template_dir: str, output_dir: str) -> None:
        self.template_dir = template_dir
        self.output_dir = Path(output_dir)
        self.docx_dir = self.output_dir / 'docx'
        self.pdf_dir = self.output_dir / 'pdf'
        self.docx: Document | None = None
        self._created_date: str = datetime.now().strftime("%d de %B de %Y")
    
    
    def __repr__(self):
        return f'Certificate({self.template_dir})'
        
    def _create_document(self) -> None:
        doc = Document(self.template_dir)
        self.docx = doc
    
    def _create_folders(self) -> None:
        self.output_dir.mkdir(exist_ok=True)
        self.docx_dir.mkdir(exist_ok=True)
        self.pdf_dir.mkdir(exist_ok=True)        
        
    def handle_certificate(
        self,
        name: str,
        date: str,
        workload: str,
        company: str,
        ) -> None:
        self._create_document()
        self._create_folders()
        for paragraph in self.docx.paragraphs:
            if 'REPLACE' in paragraph.text:
                inline = paragraph.runs
                for run in inline:
                    run.text = run.text.replace('REPLACE_name', name.title())
                    run.text = run.text.replace('REPLACE_date', date)
                    run.text = run.text.replace('REPLACE_workload', workload)
                    run.text = run.text.replace('REPLACE_company', company.upper())
                    run.text = run.text.replace('REPLACE_current_date', self._created_date)


        name_file = f'Certificado de {name.title()}'
        docx_file = self.docx_dir / f'{name_file}.docx'
        pdf_file = self.pdf_dir / f'{name_file}.pdf'
        self.docx.save(docx_file)
        convert(docx_file, pdf_file)
