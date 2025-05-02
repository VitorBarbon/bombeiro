from docx import Document
import datetime
import locale
from docx.shared import Inches
from docx.enum.section import WD_ORIENT
from docx2pdf import convert
# import os
from pathlib import Path
# import pandas as pd

# Colocando o Idioma em PT-BR
locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')


class CertificateGenerator:
    def __init__(self, output_dir):
        self.output_dir = Path(output_dir)
        self.docx_dir = self.output_dir / 'docx'
        self.pdf_dir = self.output_dir / 'pdf'
        self._create_folders()

    def _create_folders(self):
        self.output_dir.mkdir(exist_ok=True)
        self.docx_dir.mkdir(exist_ok=True)
        self.pdf_dir.mkdir(exist_ok=True)

    def generate_certificate(self, name, date, company, workload):
        print(f"Generating certificate for {name} in {self.output_dir}")
        doc = Document('template.docx')
        section = doc.sections[-1]
        section.orientation = WD_ORIENT.LANDSCAPE
        section.page_width = Inches(11.69291)
        section.page_height = Inches(8.26772)

        current_day = datetime.datetime.now()
        formatted_date = current_day.strftime("%d de %B de %Y")

        for paragraph in doc.paragraphs:
            if 'REPLACE' in paragraph.text:
                inline = paragraph.runs
                for run in inline:
                    run.text = run.text.replace('REPLACE_name', name.title())
                    run.text = run.text.replace('REPLACE_date', date)
                    run.text = run.text.replace('REPLACE_workload', str(workload))
                    run.text = run.text.replace('REPLACE_company', company.upper())
                    run.text = run.text.replace('REPLACE_current_date', '28 de abril de 2025')

        name_file = f'Certificado {name.title()}'
        docx_file = self.docx_dir / f'{name_file}.docx'
        pdf_file = self.pdf_dir / f'{name_file}.pdf'
        doc.save(docx_file)
        convert(docx_file, pdf_file)


# class ExcelReader:
#     def __init__(self, path):
#         self.path = path

#     def read_data(self):
#         df = pd.read_excel(self.path)
#         company = df.iloc[0, 1]
#         workload = df.iloc[1, 1]
#         date = df.iloc[2, 1]
#         formatted_date = date.strftime("%d de %B de %Y")

#         df_names = pd.read_excel(self.path, skiprows=5)
#         names = df_names.iloc[:, 0].tolist()

#         return names, formatted_date, company, workload

def descompact_data():
    names = [
        'Maikel Fernando da Silva',
        'Élcio Pereira da Silva Filho',
        'Paulo Victor Viana do Nascimento',
        'Wesley Ferreira da Silva',
        'Elvis Junio Chiuderoli',
        'Paulo Cesar dos Reis'
    ]
    date = '21 de março de 2025'
    company = 'SAINT-GOBAIN'
    workload = '4'
    
    return names, date, company, workload
    
def main():
    # path_folder = input('Qual o nome da pasta/caminho: ')
    # path_file_excel = input('Qual o local do arquivo: ')
    # excel_path = Path(f'../{path_folder}/{path_file_excel}.xlsx')

    # excel_reader = ExcelReader(excel_path)
    names, date, company, workload = descompact_data()

    generator = CertificateGenerator('./Certificados')
    for name in names:
        generator.generate_certificate(name.title(), date, company, workload)


if __name__ == '__main__':
    main()
