import pandas as pd
from project.utils import paths
# Create a dictionary with sample data

TEMPLATE_XLSX = paths.CERTIFICATES_DIR / 'templates'

def create_template() -> None:
    data_participants = {
    'names': ['Alice', 'Bob', 'Charlie'],
    'CPF': ['111.111.111-11', '222.222.222-22', '333.333.333-33'],
    'nivel': ['Básico', 'Intermediário', 'Avançado']
    }

    data_client = {
        'company': ['Empresa LTDA'],
        'date': ['30/04/2025'],
    }
    
    # Create a Pandas Excel writer using XlsxWriter as the engine
    with pd.ExcelWriter(f'{TEMPLATE_XLSX}/template.xlsx', engine='xlsxwriter') as writer:
        # Create the first sheet
        df1 = pd.DataFrame(data_client)
        df1.to_excel(writer, sheet_name='client', index=False)
        
        # Access the workbook and worksheet objects
        workbook = writer.book
        worksheet_client = writer.sheets['client']
        
        # Set the column width for the 'client' sheet
        worksheet_client.set_column('A:A', 40)  # Adjust column A width
        worksheet_client.set_column('B:B', 18)  # Adjust column B width
        
        # Add borders to the 'client' sheet
        for row_num, row_data in enumerate(df1.values, start=1):
            for col_num, _ in enumerate(row_data, start=0):
                cell_format = workbook.add_format({'border': 1})
                worksheet_client.write(row_num, col_num, df1.iloc[row_num - 1, col_num], cell_format)
        
        # Create the second sheet
        df2 = pd.DataFrame(data_participants)
        df2.to_excel(writer, sheet_name='participants', index=False)
        
        # Access the worksheet for 'participants'
        worksheet_participants = writer.sheets['participants']
        
        # Set the column width for the 'participants' sheet
        worksheet_participants.set_column('A:A', 50)  # Adjust column A width
        worksheet_participants.set_column('B:B', 18)  # Adjust column B width
        worksheet_participants.set_column('C:C', 18)  # Adjust column C width
        
        # Add borders to the 'participants' sheet
        for row_num, row_data in enumerate(df2.values, start=1):
            for col_num, _ in enumerate(row_data, start=0):
                cell_format = workbook.add_format({'border': 1})
                worksheet_participants.write(row_num, col_num, df2.iloc[row_num - 1, col_num], cell_format)

        print(f"Table created and saved to '{TEMPLATE_XLSX}/template.xlsx'")
