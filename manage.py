from certificates.certificate_creator import Certificate, TEMPLATE_DIR
from project.utils import paths


if __name__ == '__main__':
    certificate = Certificate(TEMPLATE_DIR, paths.CERTIFICATES_DIR)
    certificate.handle_certificate('Vitor Barbon', '04/05/2025', '4', 'Empresa LTDA')