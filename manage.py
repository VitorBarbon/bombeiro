from certificates.certificate_creator import Certificate, TEMPLATE_DIR
from certificates.create_template_xlsx import create_template
from certificates.extract_data_xlsx import extract_data_from_xlsx
from project.utils import paths



if __name__ == '__main__':
    # create_template()
    client, participants = extract_data_from_xlsx(paths.CERTIFICATES_DIR / 'templates' / 'template.xlsx')
# 
    for participant in participants:
        
        workload = None
        if participant['nivel'].lower() == 'básico':
            workload = '4'
        elif participant['nivel'].lower() == 'intermediário':
            workload = '8'
        else:
            workload = '16'
        
        print(participant['names'], client[0]['date'], workload, client[0]['company'])
        certificate = Certificate(TEMPLATE_DIR, paths.CERTIFICATES_DIR)
        certificate.handle_certificate(participant['names'], client[0]['date'], workload, client[0]['company'])