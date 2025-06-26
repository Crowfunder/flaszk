from PyPDF2 import PdfReader

from _parser import Parser

class PdfParser(Parser):
    def get_ext(self):
        return 'pdf'
    def parse(self, file_path):
        reader = PdfReader(file_path)
        metadata = reader.metadata
        return self.publish_results(metadata['/Title'], metadata['/Author'])
    